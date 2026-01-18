# Deliveet Frontend

Modern, production-grade Next.js 14 frontend for the Deliveet delivery platform.

## Features

- ✨ **Next.js 14** with App Router
- 🎨 **Tailwind CSS** for styling
- 📱 **Responsive Design** optimized for mobile and desktop
- 🔐 **JWT Authentication** with secure token management
- 🔄 **Real-time Updates** via WebSocket
- 🗂️ **Zustand** state management
- 📦 **Type-safe** with TypeScript
- 🎯 **Reusable Components** library

## Project Structure

```
frontend/
├── app/                 # Next.js app directory
│   ├── auth/           # Login/Register pages
│   ├── dashboard/      # Customer & Courier dashboards
│   └── page.tsx        # Home page
├── components/         # Reusable React components
│   ├── common/        # Layout & navigation
│   └── ui/            # Base UI components
├── store/             # Zustand stores (auth, shipment, notifications)
├── lib/               # Utilities (API client, WebSocket)
├── types/             # TypeScript type definitions
└── styles/            # Global styles & CSS
```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update API URL if needed in .env.local
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

## API Integration

The frontend uses a custom API client with:
- Automatic JWT token injection
- Token refresh mechanism
- Axios interceptors for error handling
- Secure token storage (localStorage + httpOnly cookies)

## WebSocket Features

Real-time delivery tracking, notifications, and status updates via Socket.io.

## Available Pages

### Public
- `/` - Home page
- `/auth/login` - Login
- `/auth/register` - Registration

### Customer
- `/dashboard/customer` - Dashboard
- `/dashboard/customer/new-shipment` - Create shipment
- `/dashboard/customer/shipments` - All shipments
- `/dashboard/customer/tracking/:id` - Track delivery

### Courier
- `/dashboard/courier` - Dashboard
- `/dashboard/courier/deliveries` - Available deliveries
- `/dashboard/courier/current` - Current delivery

## State Management

### Auth Store
- User authentication
- Token management
- User profile

### Shipment Store
- Shipment CRUD operations
- Delivery tracking
- Status management

### Notification Store
- Real-time notifications
- Unread count tracking

## UI Components

- `Button` - Customizable button component
- `Input` - Form input with validation
- `Card` - Content container
- `Alert` - Success/error messages
- `ProtectedRoute` - Route protection wrapper
- `Navbar` - Navigation bar

## Environment Variables

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_MAPS_API_KEY=your_maps_api_key
NEXT_PUBLIC_APP_NAME=Deliveet
```

## Performance

- Code splitting with dynamic imports
- Image optimization
- CSS minification with Tailwind
- Tree shaking with Next.js
- Production builds: ~150KB gzipped

## Testing

```bash
npm run test
npm run test:watch
npm run test:coverage
```

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```bash
docker build -t deliveet-frontend .
docker run -p 3000:3000 deliveet-frontend
```

### Manual

```bash
npm run build
npm start
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Contributing

1. Create a feature branch
2. Make your changes
3. Run `npm run lint` and `npm run type-check`
4. Submit a pull request

## License

MIT

## Support

For issues and questions:
- 📧 Email: support@deliveet.com
- 💬 Chat: In-app support
- 📱 Phone: +234 XXX XXXX XXX
