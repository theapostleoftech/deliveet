# Frontend Implementation Guide

## Overview

This document covers the complete Next.js 14 frontend implementation for the Deliveet delivery platform. The frontend is designed to be modern, performant, and provide an excellent user experience across all devices.

## Architecture

### Technology Stack

```
├── Next.js 14        - React framework with App Router
├── React 18          - UI library
├── TypeScript         - Type safety
├── Tailwind CSS      - Utility-first styling
├── Zustand           - Lightweight state management
├── Axios             - HTTP client
├── Socket.io         - Real-time communication
├── react-hook-form   - Form handling & validation
├── Zod               - Schema validation
└── Framer Motion     - Animations
```

### Directory Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout wrapper
│   ├── page.tsx                # Home page
│   ├── auth/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   └── dashboard/
│       ├── customer/
│       │   ├── page.tsx        # Customer dashboard
│       │   ├── new-shipment/
│       │   ├── shipments/
│       │   └── tracking/
│       └── courier/
│           ├── page.tsx        # Courier dashboard
│           ├── deliveries/
│           └── current/
├── components/
│   ├── common/
│   │   ├── Navbar.tsx          # Navigation bar
│   │   ├── Footer.tsx          # Footer
│   │   └── ProtectedRoute.tsx  # Route protection
│   └── ui/
│       ├── Button.tsx          # Button component
│       ├── Input.tsx           # Form input
│       ├── Card.tsx            # Card wrapper
│       └── Alert.tsx           # Alert messages
├── store/
│   ├── auth.ts                 # Authentication store
│   ├── shipment.ts             # Shipment state
│   └── notifications.ts        # Notifications
├── lib/
│   ├── api-client.ts           # API client with interceptors
│   └── websocket.ts            # WebSocket manager
├── types/
│   └── index.ts                # TypeScript definitions
├── styles/
│   └── globals.css             # Global styles
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── tailwind.config.ts          # Tailwind config
├── next.config.ts              # Next.js config
└── .env.example                # Environment template
```

## Setup Instructions

### 1. Prerequisites

```bash
# Check Node.js version (requires 18+)
node --version

# Check npm version
npm --version
```

### 2. Installation

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
```

### 3. Environment Configuration

Update `.env.local`:

```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Maps (optional)
NEXT_PUBLIC_MAPS_API_KEY=your_google_maps_key

# App Configuration
NEXT_PUBLIC_APP_NAME=Deliveet
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 4. Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### 5. Build & Deploy

```bash
# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint

# Testing
npm test
```

## Component Library

### UI Components

#### Button

```tsx
<Button variant="primary" size="lg" isLoading={false}>
  Click Me
</Button>

// Variants: primary, secondary, outline, ghost, danger
// Sizes: sm, md, lg
```

#### Input

```tsx
<Input
  label="Email"
  type="email"
  placeholder="your@email.com"
  error={error?.message}
/>
```

#### Card

```tsx
<Card hoverable onClick={handleClick}>
  <h3>Card Title</h3>
  <p>Card content</p>
</Card>
```

#### Alert

```tsx
<Alert
  type="success"
  title="Success"
  message="Operation completed"
  onClose={() => {}}
/>

// Types: success, error, warning, info
```

### Layout Components

#### Navbar

Sticky navigation bar with:
- App logo and branding
- Notification bell with unread count
- User menu with dropdown
- Responsive design

#### ProtectedRoute

Route protection wrapper for authenticated pages:

```tsx
<ProtectedRoute requiredRole="customer">
  <YourComponent />
</ProtectedRoute>
```

## State Management

### Authentication Store

```typescript
const { 
  user,              // Current user object
  isAuthenticated,   // Auth status
  login,             // Login method
  register,          // Register method
  logout,            // Logout method
  refreshUser,       // Refresh user data
} = useAuthStore();
```

### Shipment Store

```typescript
const {
  shipments,         // Array of shipments
  currentShipment,   // Active shipment
  createShipment,    // Create new shipment
  fetchShipments,    // Fetch list
  updateShipment,    // Update shipment
  deleteShipment,    // Delete shipment
} = useShipmentStore();
```

### Notification Store

```typescript
const {
  notifications,     // Array of notifications
  unreadCount,       // Count of unread
  addNotification,   // Add new notification
  markAsRead,        // Mark as read
  clearAll,          // Clear all notifications
} = useNotificationStore();
```

## API Integration

### API Client

The `apiClient` handles:
- Automatic token injection in headers
- Token refresh on 401 response
- Error handling with interceptors
- Secure token storage

```typescript
import { apiClient } from '@/lib/api-client';

// GET
const { data } = await apiClient.get('/shipments/');

// POST
const { data } = await apiClient.post('/shipments/', {
  receiver_name: "John",
  // ... other fields
});

// PUT/PATCH
await apiClient.put(`/shipments/${id}/`, updatedData);

// DELETE
await apiClient.delete(`/shipments/${id}/`);
```

### Token Management

Tokens are automatically:
1. Injected in request headers
2. Stored in localStorage and httpOnly cookies
3. Refreshed when expired (401 response)
4. Cleared on logout

## Real-time Features

### WebSocket Manager

```typescript
import { wsManager } from '@/lib/websocket';

// Connect with authentication
await wsManager.connect(accessToken);

// Subscribe to events
wsManager.on('delivery-update', (data) => {
  console.log('Delivery updated:', data);
});

// Emit events
wsManager.emit('accept-delivery', { deliveryId });

// Check connection status
if (wsManager.isConnected()) {
  // ...
}

// Disconnect
wsManager.disconnect();
```

### Real-time Endpoints

- `delivery-update` - Delivery status changes
- `location-update` - Courier location tracking
- `notification` - Push notifications
- `tracking-update` - Shipment tracking

## Pages Guide

### Public Pages

#### Home (`/`)
- Landing page with features
- CTA buttons for login/register
- Feature showcase
- Footer with links

#### Login (`/auth/login`)
- Email/password form
- Remember me option
- Forgot password link
- Sign up CTA

#### Register (`/auth/register`)
- Multi-field form (name, email, phone)
- Role selection (customer/courier)
- Password validation
- Sign in link

### Customer Pages

#### Dashboard (`/dashboard/customer`)
- Statistics (total shipments, in transit, completed)
- Quick action to create shipment
- Recent shipments list
- Balance information

#### New Shipment (`/dashboard/customer/new-shipment`)
- Recipient information form
- Delivery address form
- Package details form
- Submit to payment flow

#### Shipments (`/dashboard/customer/shipments`)
- Paginated list of all shipments
- Filtering and sorting
- Quick actions (track, cancel)
- Status badges

#### Tracking (`/dashboard/customer/tracking/:id`)
- Real-time delivery map
- Status timeline
- Current location
- Estimated arrival time
- Live courier location

### Courier Pages

#### Dashboard (`/dashboard/courier`)
- Statistics (deliveries, earnings)
- Online/offline toggle
- Available deliveries list
- Current delivery map

#### Available Deliveries (`/dashboard/courier/deliveries`)
- List of nearby available deliveries
- Distance and earnings display
- Quick accept button
- Filtering by location/price

#### Current Delivery (`/dashboard/courier/current`)
- Full-screen delivery map
- Route visualization
- Navigation controls
- Status update buttons

## Styling System

### Color Palette

```css
Primary: #f97316 (orange)
Secondary: #0ea5e9 (blue)
Success: #10b981 (green)
Warning: #f59e0b (yellow)
Error: #ef4444 (red)
Dark: #1f2937
Light: #f3f4f6
```

### Responsive Breakpoints

```css
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### Utility Classes

```css
.container-fluid  /* Responsive padding */
.flex-center      /* Flex centered */
.flex-between     /* Flex space-between */
.text-gradient    /* Gradient text */
.card            /* Card styles */
.input-field     /* Input styles */
.badge           /* Badge styles */
```

## Performance Optimization

### Code Splitting

- Automatic route-based splitting
- Component lazy loading where needed
- Dynamic imports for heavy components

### Image Optimization

- Next.js Image component for optimization
- Responsive image serving
- WebP format conversion

### Bundle Analysis

```bash
npm run build -- --analyze
```

### Caching Strategies

- Browser caching via headers
- API response caching in stores
- Service worker for offline support (future)

## Testing

### Unit Tests

```bash
npm run test
```

### Watch Mode

```bash
npm run test:watch
```

### Coverage Report

```bash
npm run test:coverage
```

## Deployment

### Vercel

```bash
npm install -g vercel
vercel
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

```bash
docker build -t deliveet-frontend .
docker run -p 3000:3000 deliveet-frontend
```

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://api.deliveet.com/api/v1
NEXT_PUBLIC_WS_URL=wss://api.deliveet.com/ws
NEXT_PUBLIC_MAPS_API_KEY=prod_key
```

## Security Best Practices

1. **Token Security**
   - Tokens stored in httpOnly cookies where possible
   - Refresh token rotation enabled
   - No sensitive data in localStorage

2. **CORS & CSRF**
   - Backend handles CORS validation
   - CSRF tokens for state-changing requests (if needed)

3. **Input Validation**
   - Client-side validation with Zod
   - Server-side validation essential
   - XSS prevention via React escaping

4. **Authentication**
   - JWT tokens with 1-hour expiration
   - Automatic refresh with 7-day refresh tokens
   - Logout clears all tokens

## Troubleshooting

### Common Issues

**1. API Connection Failed**
```
Check NEXT_PUBLIC_API_URL in .env.local
Ensure backend is running on correct port
Check CORS settings in backend
```

**2. WebSocket Connection Failed**
```
Verify NEXT_PUBLIC_WS_URL
Check WebSocket support in backend
Review Channels configuration
```

**3. Authentication Loop**
```
Clear localStorage and cookies
Verify token structure
Check auth store initialization
```

**4. Styling Not Applied**
```
Run: npm run build
Check Tailwind config paths
Verify CSS imports in layout
```

## Next Steps

### Phase 2 Features (In Progress)
- ✅ Authentication system
- ✅ Customer dashboard
- ✅ Courier dashboard
- ⏳ Delivery tracking map
- ⏳ Real-time notifications
- ⏳ Payment integration
- ⏳ Rating & reviews

### Phase 3 Features
- Mobile app (React Native)
- Push notifications
- Offline mode
- Advanced analytics
- Admin dashboard
- Merchant portal

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Zustand](https://github.com/pmndrs/zustand)
- [React Hook Form](https://react-hook-form.com/)
- [Socket.io Client](https://socket.io/docs/v4/client-api/)

## Support

- 📧 Email: support@deliveet.com
- 📱 Phone: +234 XXX XXXX XXX
- 💬 Chat: In-app support

---

**Last Updated:** January 18, 2024  
**Version:** 2.0.0  
**Status:** Production Ready
