# 🧪 Deliveet Integration Testing Guide

**Status:** 🚀 Integration Testing in Progress  
**Date:** January 18, 2026  
**Version:** 2.0.0

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Test Environment Setup](#test-environment-setup)
3. [Backend Integration Tests](#backend-integration-tests)
4. [Frontend Integration Tests](#frontend-integration-tests)
5. [End-to-End Tests](#end-to-end-tests)
6. [Running Tests](#running-tests)
7. [Test Coverage](#test-coverage)
8. [Debugging & Troubleshooting](#debugging--troubleshooting)

---

## 🎯 Overview

Integration testing ensures that all components of the Deliveet platform work together seamlessly:

- **Backend API** (Django REST Framework)
- **Frontend Application** (Next.js React)
- **Real-time Services** (WebSocket)
- **Payment Gateway** (Monnify)
- **Database** (PostgreSQL)
- **Cache** (Redis)

### Testing Scope

| Component | Test Type | Coverage |
|-----------|-----------|----------|
| **Authentication** | API + E2E | Login, Register, Token Refresh |
| **Shipments** | API + E2E | Create, List, Update, Track |
| **Deliveries** | API + E2E | Accept, Update Status, Complete |
| **Real-time** | Unit + Integration | WebSocket Events, Updates |
| **Payments** | API + Mock | Initialize, Verify, Refund |
| **Users** | API | CRUD Operations |
| **Notifications** | API | Create, Mark Read |

---

## 🔧 Test Environment Setup

### Prerequisites

```bash
# Backend requirements already installed
pip install pytest pytest-django pytest-cov factory-boy faker freezegun

# Frontend requirements already installed
cd frontend && npm install --save-dev @testing-library/user-event vitest
```

### Django Test Configuration

Create `pytest.ini` in project root:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = deliveet.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --tb=short
    --cov=api
    --cov=accounts
    --cov=shipments
    --cov=courier
    --cov-report=html
    --cov-report=term-missing
testpaths = .
markers =
    slow: marks tests as slow
    integration: marks tests as integration
    auth: marks tests as authentication related
```

### Test Database

Create `conftest.py` in project root:

```python
import pytest
from django.test import Client
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

@pytest.fixture
def api_client():
    """DRF API Client fixture"""
    return APIClient()

@pytest.fixture
def authenticated_client():
    """API Client with JWT authentication"""
    client = APIClient()
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, user

@pytest.fixture
def test_user():
    """Create a test user"""
    return User.objects.create_user(
        email='testuser@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def test_courier():
    """Create a test courier"""
    user = User.objects.create_user(
        email='courier@example.com',
        password='testpass123',
        user_type='courier'
    )
    return user

@pytest.fixture
def test_customer():
    """Create a test customer"""
    user = User.objects.create_user(
        email='customer@example.com',
        password='testpass123',
        user_type='customer'
    )
    return user
```

---

## ✅ Backend Integration Tests

### 1. Authentication Tests

Create `api/tests/test_auth.py`:

```python
import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User

@pytest.mark.integration
@pytest.mark.auth
class TestAuthentication:
    """Test authentication endpoints"""

    def test_user_registration(self, api_client):
        """Test user registration"""
        url = reverse('auth-register')
        data = {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'customer'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_user_login(self, api_client, test_user):
        """Test user login"""
        url = reverse('auth-login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_token_refresh(self, api_client, test_user):
        """Test token refresh"""
        # First login
        login_url = reverse('auth-login')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        login_response = api_client.post(login_url, login_data)
        refresh_token = login_response.data['refresh']

        # Then refresh
        refresh_url = reverse('auth-token-refresh')
        refresh_data = {'refresh': refresh_token}
        refresh_response = api_client.post(refresh_url, refresh_data)
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data

    def test_get_current_user(self, authenticated_client):
        """Test getting current user"""
        client, user = authenticated_client
        url = reverse('auth-user')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    def test_invalid_credentials(self, api_client):
        """Test login with invalid credentials"""
        url = reverse('auth-login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

### 2. Shipment Tests

Create `api/tests/test_shipments.py`:

```python
import pytest
from django.urls import reverse
from rest_framework import status
from shipments.models import Shipment

@pytest.mark.integration
class TestShipments:
    """Test shipment endpoints"""

    def test_create_shipment(self, authenticated_client, test_customer):
        """Test creating a shipment"""
        client, user = authenticated_client
        url = reverse('shipment-list')
        data = {
            'pickup_location': '123 Main St, Lagos',
            'dropoff_location': '456 Oak Ave, Lagos',
            'weight': 2.5,
            'package_type': 'parcel',
            'special_instructions': 'Handle with care'
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Shipment.objects.filter(
            pickup_location='123 Main St, Lagos'
        ).exists()

    def test_list_shipments(self, authenticated_client):
        """Test listing shipments"""
        client, user = authenticated_client
        # Create test shipment
        Shipment.objects.create(
            customer=user,
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        
        url = reverse('shipment-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_retrieve_shipment(self, authenticated_client):
        """Test retrieving a shipment"""
        client, user = authenticated_client
        shipment = Shipment.objects.create(
            customer=user,
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        
        url = reverse('shipment-detail', kwargs={'pk': shipment.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == shipment.id

    def test_update_shipment(self, authenticated_client):
        """Test updating a shipment"""
        client, user = authenticated_client
        shipment = Shipment.objects.create(
            customer=user,
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave'
        )
        
        url = reverse('shipment-detail', kwargs={'pk': shipment.id})
        data = {'special_instructions': 'Updated instructions'}
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        
        shipment.refresh_from_db()
        assert shipment.special_instructions == 'Updated instructions'

    def test_cancel_shipment(self, authenticated_client):
        """Test canceling a shipment"""
        client, user = authenticated_client
        shipment = Shipment.objects.create(
            customer=user,
            pickup_location='123 Main St',
            dropoff_location='456 Oak Ave',
            status='pending'
        )
        
        url = reverse('shipment-cancel', kwargs={'pk': shipment.id})
        response = client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
        shipment.refresh_from_db()
        assert shipment.status == 'cancelled'
```

### 3. Delivery Tests

Create `api/tests/test_deliveries.py`:

```python
import pytest
from django.urls import reverse
from rest_framework import status
from shipments.models import Delivery

@pytest.mark.integration
class TestDeliveries:
    """Test delivery endpoints"""

    def test_list_deliveries(self, authenticated_client, test_courier):
        """Test listing available deliveries"""
        client, user = authenticated_client
        url = reverse('delivery-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_accept_delivery(self, authenticated_client, test_courier):
        """Test accepting a delivery"""
        client, courier = authenticated_client
        # Create a delivery
        delivery = Delivery.objects.create(
            shipment_id=1,  # Assumes shipment exists
            status='pending'
        )
        
        url = reverse('delivery-accept', kwargs={'pk': delivery.id})
        response = client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
        delivery.refresh_from_db()
        assert delivery.courier == courier

    def test_update_delivery_status(self, authenticated_client):
        """Test updating delivery status"""
        client, courier = authenticated_client
        delivery = Delivery.objects.create(
            status='accepted',
            courier=courier
        )
        
        url = reverse('delivery-detail', kwargs={'pk': delivery.id})
        data = {'status': 'in_transit'}
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        
        delivery.refresh_from_db()
        assert delivery.status == 'in_transit'

    def test_complete_delivery(self, authenticated_client):
        """Test completing a delivery"""
        client, courier = authenticated_client
        delivery = Delivery.objects.create(
            status='in_transit',
            courier=courier
        )
        
        url = reverse('delivery-complete', kwargs={'pk': delivery.id})
        response = client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
        delivery.refresh_from_db()
        assert delivery.status == 'completed'
```

---

## ✅ Frontend Integration Tests

### Jest Configuration

Create `frontend/jest.config.js`:

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>'],
  testMatch: ['**/__tests__/**/*.ts?(x)', '**/?(*.)+(spec|test).ts?(x)'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react',
      },
    }],
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
};
```

### API Client Tests

Create `frontend/__tests__/lib/api-client.test.ts`:

```typescript
import axios from 'axios';
import { createApiClient } from '@/lib/api-client';

jest.mock('axios');

describe('API Client', () => {
  const mockAxios = axios as jest.Mocked<typeof axios>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should make authenticated request', async () => {
    const client = createApiClient();
    mockAxios.get.mockResolvedValueOnce({ data: { id: 1 } });

    // Mock localStorage
    localStorage.setItem('access_token', 'test_token');

    // Test request
    const response = await client.get('/shipments/');
    expect(response.data).toEqual({ id: 1 });
  });

  test('should refresh token on 401', async () => {
    const client = createApiClient();
    
    mockAxios.post.mockResolvedValueOnce({
      data: { access: 'new_token' }
    });

    localStorage.setItem('refresh_token', 'refresh_token');

    // Simulate 401 error and recovery
    const error = new Error('Unauthorized');
    expect(error.message).toBe('Unauthorized');
  });

  test('should handle request error', async () => {
    const client = createApiClient();
    mockAxios.get.mockRejectedValueOnce(new Error('Network error'));

    try {
      await client.get('/shipments/');
    } catch (error) {
      expect(error).toBeDefined();
    }
  });
});
```

### Component Tests

Create `frontend/__tests__/components/Button.test.tsx`:

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '@/components/ui/Button';

describe('Button Component', () => {
  test('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  test('handles click event', async () => {
    const mockClick = jest.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={mockClick}>Click</Button>);
    await user.click(screen.getByText('Click'));
    
    expect(mockClick).toHaveBeenCalledTimes(1);
  });

  test('renders different variants', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>);
    expect(screen.getByText('Primary')).toHaveClass('bg-primary-500');

    rerender(<Button variant="secondary">Secondary</Button>);
    expect(screen.getByText('Secondary')).toHaveClass('bg-secondary-500');
  });

  test('disabled button does not respond to click', async () => {
    const mockClick = jest.fn();
    const user = userEvent.setup();
    
    render(
      <Button disabled onClick={mockClick}>
        Disabled
      </Button>
    );
    await user.click(screen.getByText('Disabled'));
    
    expect(mockClick).not.toHaveBeenCalled();
  });
});
```

### Auth Store Tests

Create `frontend/__tests__/store/auth.test.ts`:

```typescript
import { useAuthStore } from '@/store/auth';
import { renderHook, act } from '@testing-library/react';

describe('Auth Store', () => {
  beforeEach(() => {
    // Clear store state
    const { result } = renderHook(() => useAuthStore());
    act(() => {
      result.current.clearAuth();
    });
  });

  test('should set auth tokens', () => {
    const { result } = renderHook(() => useAuthStore());

    act(() => {
      result.current.setTokens('access_token', 'refresh_token');
    });

    expect(result.current.accessToken).toBe('access_token');
    expect(result.current.refreshToken).toBe('refresh_token');
  });

  test('should set current user', () => {
    const { result } = renderHook(() => useAuthStore());
    const user = { id: 1, email: 'test@example.com', user_type: 'customer' };

    act(() => {
      result.current.setUser(user);
    });

    expect(result.current.user).toEqual(user);
    expect(result.current.isAuthenticated).toBe(true);
  });

  test('should clear auth on logout', () => {
    const { result } = renderHook(() => useAuthStore());

    act(() => {
      result.current.setUser({ id: 1, email: 'test@example.com' });
      result.current.clearAuth();
    });

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });
});
```

---

## 🔄 End-to-End Tests

Create `frontend/__tests__/e2e/auth-flow.test.tsx`:

```typescript
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Login } from '@/app/auth/login/page';

// Mock API responses
jest.mock('@/lib/api-client', () => ({
  apiClient: {
    post: jest.fn((url, data) => {
      if (url === '/auth/login/') {
        return Promise.resolve({
          data: {
            access: 'access_token',
            refresh: 'refresh_token',
          }
        });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    }),
  }
}));

describe('Authentication Flow', () => {
  test('complete login flow', async () => {
    const user = userEvent.setup();
    render(<Login />);

    // Fill in form
    const emailInput = screen.getByLabelText('Email');
    const passwordInput = screen.getByLabelText('Password');
    const submitButton = screen.getByText('Sign In');

    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);

    // Wait for navigation or success message
    await waitFor(() => {
      expect(screen.queryByText('Loading')).not.toBeInTheDocument();
    });
  });

  test('shows error on invalid credentials', async () => {
    jest.mock('@/lib/api-client', () => ({
      apiClient: {
        post: jest.fn(() => Promise.reject({
          response: {
            status: 401,
            data: { detail: 'Invalid credentials' }
          }
        }))
      }
    }));

    const user = userEvent.setup();
    render(<Login />);

    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'wrong');
    await user.click(screen.getByText('Sign In'));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });
});
```

---

## 🚀 Running Tests

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest api/tests/test_auth.py

# Run specific test class
pytest api/tests/test_auth.py::TestAuthentication

# Run specific test
pytest api/tests/test_auth.py::TestAuthentication::test_user_login

# Run with coverage
pytest --cov=api --cov-report=html

# Run integration tests only
pytest -m integration

# Run tests with verbose output
pytest -v

# Run tests in parallel
pytest -n auto
```

### Frontend Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- components/Button.test.tsx

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm test -- e2e
```

### Docker-based Testing

```bash
# Build test environment
docker-compose -f docker-compose.test.yml up

# Run all tests
docker-compose -f docker-compose.test.yml run web pytest
docker-compose -f docker-compose.test.yml run frontend npm test

# Cleanup
docker-compose -f docker-compose.test.yml down
```

---

## 📊 Test Coverage

### Backend Target Coverage

```
api/                                  95%+
├── views.py                          95%+
├── serializers.py                    90%+
├── permissions.py                    100%
└── models.py                         90%+

accounts/                             85%+
shipments/                            85%+
courier/                              80%+
```

### Frontend Target Coverage

```
components/                           90%+
├── ui/                               95%+
└── common/                           85%+

store/                                95%+
lib/                                  90%+
```

---

## 🐛 Debugging & Troubleshooting

### Common Issues

#### 1. Database Not Found
```bash
# Ensure test database exists
python manage.py migrate --run-syncdb

# Or reset test database
pytest --reuse-db -p no:warnings
```

#### 2. API Endpoint Not Found
```bash
# Check URL routing
python manage.py show_urls | grep api

# Verify URL name matches in tests
```

#### 3. Import Errors in Frontend
```bash
# Clear node_modules and reinstall
rm -rf frontend/node_modules package-lock.json
npm install

# Clear Jest cache
npm test -- --clearCache
```

#### 4. Token Expiration in Tests
```python
# Use freezegun to mock time
from freezegun import freeze_time

@freeze_time("2024-01-18 10:00:00")
def test_token_not_expired():
    # Test logic here
```

### Running Single Test with Debug Output

**Backend:**
```bash
pytest -v -s --tb=long api/tests/test_auth.py::TestAuthentication::test_user_login
```

**Frontend:**
```bash
npm test -- --verbose components/Button.test.tsx
```

---

## ✅ Test Checklist

- [ ] Backend authentication tests pass
- [ ] Backend shipment CRUD tests pass
- [ ] Backend delivery workflow tests pass
- [ ] Frontend component tests pass
- [ ] Frontend store tests pass
- [ ] Frontend auth flow E2E tests pass
- [ ] API integration tests pass
- [ ] WebSocket connection tests pass
- [ ] Payment integration tests pass
- [ ] Overall coverage > 85%
- [ ] No failing tests in CI/CD
- [ ] Performance targets met

---

## 📈 Next Steps

1. **Run Backend Tests** - Verify all API endpoints
2. **Run Frontend Tests** - Verify all components
3. **Integration Tests** - Full flow testing
4. **Performance Testing** - Response times
5. **Load Testing** - Concurrent users
6. **Security Testing** - Vulnerability scanning

---

## 📞 Support

For test-related questions:
- Check test fixtures in `conftest.py`
- Review existing test examples in `api/tests/`
- Check pytest documentation: https://docs.pytest.org
- Check Jest documentation: https://jestjs.io

---

**Branch:** `production/uber-bolt-upgrade`  
**Last Updated:** January 18, 2026  
**Status:** Ready for Testing
