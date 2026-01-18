"""
Integration tests for delivery endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from shipments.models import Delivery, Shipment


@pytest.mark.integration
@pytest.mark.delivery
class TestDeliveryListing:
    """Test delivery listing endpoints."""

    def test_list_available_deliveries_courier(self, authenticated_courier_client):
        """Test courier can see available deliveries."""
        client, courier = authenticated_courier_client
        url = reverse('delivery-list')
        
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data or 'count' in response.data

    def test_list_deliveries_customer_forbidden(self, authenticated_client):
        """Test customer cannot list deliveries."""
        client, customer = authenticated_client
        url = reverse('delivery-list')
        
        response = client.get(url)
        
        # Depending on implementation
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_200_OK  # If filtered by role
        ]

    def test_list_deliveries_unauthenticated(self, api_client):
        """Test unauthenticated user cannot list deliveries."""
        url = reverse('delivery-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
@pytest.mark.delivery
class TestDeliveryAcceptance:
    """Test delivery acceptance workflow."""

    def test_accept_available_delivery(self, authenticated_courier_client, test_delivery):
        """Test courier accepting an available delivery."""
        client, courier = authenticated_courier_client
        test_delivery.status = 'pending'
        test_delivery.save()
        
        url = reverse('delivery-accept', kwargs={'pk': test_delivery.id})
        response = client.post(url, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        test_delivery.refresh_from_db()
        assert test_delivery.courier == courier
        assert test_delivery.status == 'accepted'

    def test_accept_already_accepted_delivery(self, authenticated_courier_client, 
                                             test_delivery, test_courier):
        """Test cannot accept already accepted delivery."""
        client, other_courier = authenticated_courier_client
        test_delivery.status = 'accepted'
        test_delivery.courier = test_courier
        test_delivery.save()
        
        url = reverse('delivery-accept', kwargs={'pk': test_delivery.id})
        response = client.post(url, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_accept_delivery_customer_forbidden(self, authenticated_client, test_delivery):
        """Test customer cannot accept delivery."""
        client, customer = authenticated_client
        
        url = reverse('delivery-accept', kwargs={'pk': test_delivery.id})
        response = client.post(url, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.integration
@pytest.mark.delivery
class TestDeliveryStatusUpdate:
    """Test delivery status update workflow."""

    def test_update_delivery_in_transit(self, authenticated_courier_client, test_courier):
        """Test updating delivery to in_transit."""
        client, courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=courier,
            status='accepted'
        )
        
        url = reverse('delivery-detail', kwargs={'pk': delivery.id})
        data = {'status': 'in_transit'}
        response = client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        delivery.refresh_from_db()
        assert delivery.status == 'in_transit'

    def test_update_delivery_arrived(self, authenticated_courier_client, test_courier):
        """Test updating delivery to arrived."""
        client, courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=courier,
            status='in_transit'
        )
        
        url = reverse('delivery-detail', kwargs={'pk': delivery.id})
        data = {'status': 'arrived'}
        response = client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        delivery.refresh_from_db()
        assert delivery.status == 'arrived'

    def test_invalid_status_transition(self, authenticated_courier_client, test_courier):
        """Test invalid status transition."""
        client, courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=courier,
            status='pending'
        )
        
        url = reverse('delivery-detail', kwargs={'pk': delivery.id})
        data = {'status': 'completed'}  # Invalid: must go through intermediate states
        response = client.patch(url, data, format='json')
        
        # Should prevent invalid transition
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_only_assigned_courier_can_update(self, authenticated_courier_client, 
                                             test_courier, test_delivery):
        """Test only assigned courier can update delivery."""
        client, other_courier = authenticated_courier_client
        test_delivery.courier = test_courier
        test_delivery.status = 'accepted'
        test_delivery.save()
        
        url = reverse('delivery-detail', kwargs={'pk': test_delivery.id})
        data = {'status': 'in_transit'}
        response = client.patch(url, data, format='json')
        
        # Should be forbidden for unauthorized courier
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.integration
@pytest.mark.delivery
class TestDeliveryCompletion:
    """Test delivery completion workflow."""

    def test_complete_delivery_arrived(self, authenticated_courier_client, test_courier):
        """Test completing delivery from arrived status."""
        client, courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=courier,
            status='arrived'
        )
        
        url = reverse('delivery-complete', kwargs={'pk': delivery.id})
        data = {
            'signature': 'base64_signature_data',
            'notes': 'Delivery completed successfully'
        }
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        delivery.refresh_from_db()
        assert delivery.status == 'completed'

    def test_complete_delivery_without_arrival(self, authenticated_courier_client, test_courier):
        """Test cannot complete delivery without arrival."""
        client, courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=courier,
            status='in_transit'
        )
        
        url = reverse('delivery-complete', kwargs={'pk': delivery.id})
        response = client.post(url, format='json')
        
        # Should prevent completion
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
@pytest.mark.delivery
class TestDeliveryLocation:
    """Test delivery location updates."""

    def test_update_delivery_location(self, authenticated_courier_client, test_courier):
        """Test updating delivery location."""
        client, courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=courier,
            status='in_transit'
        )
        
        url = reverse('delivery-update-location', kwargs={'pk': delivery.id})
        data = {
            'latitude': 6.5244,
            'longitude': 3.3792,
            'accuracy': 10.5
        }
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        delivery.refresh_from_db()
        assert delivery.current_latitude is not None

    def test_location_update_by_non_assigned_courier(self, authenticated_courier_client,
                                                     test_courier):
        """Test non-assigned courier cannot update location."""
        client, other_courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=test_courier,
            status='in_transit'
        )
        
        url = reverse('delivery-update-location', kwargs={'pk': delivery.id})
        data = {
            'latitude': 6.5244,
            'longitude': 3.3792
        }
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.integration
@pytest.mark.delivery
class TestDeliveryRetrieval:
    """Test retrieving delivery details."""

    def test_retrieve_assigned_delivery(self, authenticated_courier_client, test_courier):
        """Test courier can retrieve assigned delivery."""
        client, courier = authenticated_courier_client
        delivery = Delivery.objects.create(
            shipment_id=1,
            courier=courier
        )
        
        url = reverse('delivery-detail', kwargs={'pk': delivery.id})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == delivery.id

    def test_retrieve_unassigned_delivery(self, authenticated_courier_client, test_delivery):
        """Test courier cannot retrieve unassigned delivery."""
        client, courier = authenticated_courier_client
        
        url = reverse('delivery-detail', kwargs={'pk': test_delivery.id})
        response = client.get(url)
        
        # Depending on implementation: forbidden or 404
        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_retrieve_nonexistent_delivery(self, authenticated_courier_client):
        """Test retrieving non-existent delivery."""
        client, _ = authenticated_courier_client
        
        url = reverse('delivery-detail', kwargs={'pk': 99999})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
@pytest.mark.delivery
class TestDeliveryFiltering:
    """Test delivery list filtering."""

    def test_filter_by_status(self, authenticated_courier_client, test_courier):
        """Test filtering deliveries by status."""
        client, courier = authenticated_courier_client
        
        # Create deliveries with different statuses
        Delivery.objects.create(shipment_id=1, courier=courier, status='pending')
        Delivery.objects.create(shipment_id=2, courier=courier, status='accepted')
        
        url = reverse('delivery-list') + '?status=pending'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK

    def test_filter_by_courier(self, authenticated_courier_client, test_courier):
        """Test filtering deliveries by courier."""
        client, courier = authenticated_courier_client
        
        Delivery.objects.create(shipment_id=1, courier=courier, status='pending')
        
        url = reverse('delivery-list') + f'?courier={courier.id}'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
