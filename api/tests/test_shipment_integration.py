"""
Integration tests for shipment endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from shipments.models import Shipment


@pytest.mark.integration
@pytest.mark.shipment
class TestShipmentCreation:
    """Test shipment creation endpoint."""

    def test_create_shipment_customer(self, authenticated_client, test_shipment_data):
        """Test customer creating a new shipment."""
        client, customer = authenticated_client
        url = reverse('shipment-list')
        
        response = client.post(url, test_shipment_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Shipment.objects.filter(
            customer=customer,
            pickup_location=test_shipment_data['pickup_location']
        ).exists()
        
        shipment = Shipment.objects.get(id=response.data['id'])
        assert shipment.status == 'pending'

    def test_create_shipment_unauthenticated(self, api_client, test_shipment_data):
        """Test unauthenticated user cannot create shipment."""
        url = reverse('shipment-list')
        
        response = api_client.post(url, test_shipment_data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_shipment_missing_fields(self, authenticated_client):
        """Test creating shipment with missing required fields."""
        client, _ = authenticated_client
        url = reverse('shipment-list')
        data = {
            'pickup_location': '123 Main St',
            # Missing dropoff_location
        }
        
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_shipment_invalid_weight(self, authenticated_client):
        """Test creating shipment with invalid weight."""
        client, _ = authenticated_client
        url = reverse('shipment-list')
        data = {
            'pickup_location': '123 Main St',
            'dropoff_location': '456 Oak Ave',
            'weight': -5,  # Invalid negative weight
            'package_type': 'parcel'
        }
        
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
@pytest.mark.shipment
class TestShipmentRetrieval:
    """Test shipment retrieval endpoints."""

    def test_list_shipments(self, authenticated_client, test_shipment):
        """Test listing shipments for customer."""
        client, customer = authenticated_client
        url = reverse('shipment-list')
        
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data or 'count' in response.data

    def test_retrieve_shipment_own(self, authenticated_client, test_shipment):
        """Test retrieving own shipment."""
        client, customer = authenticated_client
        test_shipment.customer = customer
        test_shipment.save()
        
        url = reverse('shipment-detail', kwargs={'pk': test_shipment.id})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == test_shipment.id

    def test_retrieve_shipment_not_own(self, authenticated_client, test_shipment):
        """Test customer cannot retrieve other's shipment."""
        client, customer = authenticated_client
        # test_shipment belongs to different customer
        
        url = reverse('shipment-detail', kwargs={'pk': test_shipment.id})
        response = client.get(url)
        
        # Should be forbidden or return empty
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_retrieve_nonexistent_shipment(self, authenticated_client):
        """Test retrieving non-existent shipment."""
        client, _ = authenticated_client
        url = reverse('shipment-detail', kwargs={'pk': 99999})
        
        response = client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
@pytest.mark.shipment
class TestShipmentUpdate:
    """Test shipment update endpoints."""

    def test_update_shipment_own(self, authenticated_client, test_user):
        """Test updating own shipment."""
        client, customer = authenticated_client
        shipment = Shipment.objects.create(
            customer=customer,
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave',
            special_instructions='Original instructions'
        )
        
        url = reverse('shipment-detail', kwargs={'pk': shipment.id})
        data = {'special_instructions': 'Updated instructions'}
        
        response = client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        shipment.refresh_from_db()
        assert shipment.special_instructions == 'Updated instructions'

    def test_update_shipment_not_own(self, authenticated_client, test_shipment):
        """Test cannot update other's shipment."""
        client, _ = authenticated_client
        
        url = reverse('shipment-detail', kwargs={'pk': test_shipment.id})
        data = {'special_instructions': 'Hacked'}
        
        response = client.patch(url, data, format='json')
        
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_update_completed_shipment(self, authenticated_client, test_user):
        """Test cannot update completed shipment."""
        client, customer = authenticated_client
        shipment = Shipment.objects.create(
            customer=customer,
            status='completed',
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        
        url = reverse('shipment-detail', kwargs={'pk': shipment.id})
        data = {'pickup_location': '789 New St'}
        
        response = client.patch(url, data, format='json')
        
        # Should prevent update
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN
        ]


@pytest.mark.integration
@pytest.mark.shipment
class TestShipmentActions:
    """Test shipment action endpoints."""

    def test_cancel_shipment_pending(self, authenticated_client, test_user):
        """Test canceling pending shipment."""
        client, customer = authenticated_client
        shipment = Shipment.objects.create(
            customer=customer,
            status='pending',
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        
        url = reverse('shipment-cancel', kwargs={'pk': shipment.id})
        response = client.post(url, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        shipment.refresh_from_db()
        assert shipment.status == 'cancelled'

    def test_cancel_shipment_in_transit(self, authenticated_client, test_user):
        """Test cannot cancel in-transit shipment."""
        client, customer = authenticated_client
        shipment = Shipment.objects.create(
            customer=customer,
            status='in_transit',
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        
        url = reverse('shipment-cancel', kwargs={'pk': shipment.id})
        response = client.post(url, format='json')
        
        # Should prevent cancellation
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rate_delivery(self, authenticated_client, test_user):
        """Test rating a completed delivery."""
        client, customer = authenticated_client
        shipment = Shipment.objects.create(
            customer=customer,
            status='completed',
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        
        url = reverse('shipment-rate', kwargs={'pk': shipment.id})
        data = {
            'rating': 5,
            'comment': 'Excellent service!'
        }
        
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert shipment.rating == 5


@pytest.mark.integration
@pytest.mark.shipment
class TestShipmentTracking:
    """Test shipment tracking endpoint."""

    def test_get_tracking_info(self, authenticated_client, test_shipment):
        """Test getting tracking information."""
        client, _ = authenticated_client
        test_shipment.status = 'in_transit'
        test_shipment.save()
        
        url = reverse('shipment-tracking', kwargs={'pk': test_shipment.id})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'status' in response.data
        assert 'location' in response.data or 'estimated_delivery' in response.data

    def test_tracking_nonexistent_shipment(self, authenticated_client):
        """Test tracking non-existent shipment."""
        client, _ = authenticated_client
        
        url = reverse('shipment-tracking', kwargs={'pk': 99999})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
@pytest.mark.shipment
class TestShipmentFiltering:
    """Test shipment list filtering and search."""

    def test_filter_by_status(self, authenticated_client, test_user):
        """Test filtering shipments by status."""
        client, customer = authenticated_client
        
        # Create shipments with different statuses
        Shipment.objects.create(
            customer=customer,
            status='pending',
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        Shipment.objects.create(
            customer=customer,
            status='completed',
            pickup_location='789 New St',
            dropoff_location='101 Another Ave'
        )
        
        url = reverse('shipment-list') + '?status=pending'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Check all returned items have status=pending
        for item in response.data.get('results', []):
            assert item['status'] == 'pending'

    def test_search_by_location(self, authenticated_client, test_user):
        """Test searching shipments by location."""
        client, customer = authenticated_client
        
        Shipment.objects.create(
            customer=customer,
            pickup_location='123 Main Street, Lagos',
            dropoff_location='456 Oak Avenue, Lagos'
        )
        
        url = reverse('shipment-list') + '?search=Main'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK

    def test_pagination(self, authenticated_client, test_user):
        """Test pagination of shipment list."""
        client, customer = authenticated_client
        
        # Create multiple shipments
        for i in range(15):
            Shipment.objects.create(
                customer=customer,
                pickup_location=f'Location {i}',
                dropoff_location=f'Destination {i}'
            )
        
        url = reverse('shipment-list') + '?page=1&page_size=10'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'count' in response.data
        assert response.data['count'] >= 15
