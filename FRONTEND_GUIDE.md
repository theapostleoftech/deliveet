# Frontend Implementation Guide - Modern UI/UX for Deliveet

## 📱 Technology Stack

### Recommended Stack
- **Framework**: Next.js 14+ (React 18+)
- **Styling**: Tailwind CSS 3.4+
- **UI Components**: Shadcn/ui or Material-UI v5
- **State Management**: Zustand or Redux Toolkit
- **API Client**: Axios with interceptors
- **Real-time**: Socket.io client
- **Maps**: React-Leaflet or Google Maps React
- **Charts**: Recharts or Chart.js
- **Forms**: React Hook Form + Zod
- **Authentication**: JWT with localStorage
- **Testing**: Jest + React Testing Library
- **Build Tool**: Turbopack (integrated with Next.js)

## 🏗️ Project Structure

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── reset-password/
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── profile/
│   │   ├── orders/
│   │   └── settings/
│   ├── (courier)/
│   │   ├── layout.tsx
│   │   ├── dashboard/
│   │   ├── earnings/
│   │   ├── active-deliveries/
│   │   └── schedule/
│   ├── api/
│   │   ├── auth/
│   │   └── proxy/
│   └── page.tsx
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── AuthGuard.tsx
│   ├── dashboard/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ShipmentCard.tsx
│   │   └── StatsCard.tsx
│   ├── delivery/
│   │   ├── DeliveryMap.tsx
│   │   ├── DeliveryTracking.tsx
│   │   ├── CourierList.tsx
│   │   └── DeliveryForm.tsx
│   ├── common/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   └── Loading.tsx
│   └── ui/
│       ├── toast/
│       ├── dialog/
│       └── dropdown/
├── lib/
│   ├── api-client.ts
│   ├── auth.ts
│   ├── constants.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useDeliveries.ts
│   │   ├── useLocation.ts
│   │   └── useSocket.ts
│   └── utils.ts
├── store/
│   ├── authStore.ts
│   ├── shipmentStore.ts
│   ├── notificationStore.ts
│   └── index.ts
├── styles/
│   ├── globals.css
│   └── variables.css
├── types/
│   ├── index.ts
│   ├── api.ts
│   └── auth.ts
├── middleware.ts
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

## 🎨 UI Components Architecture

### Component Library Structure
```
components/
├── common/
│   └── Button/
│       ├── Button.tsx
│       ├── Button.module.css
│       ├── Button.types.ts
│       └── Button.test.tsx
├── layout/
│   ├── Header/
│   ├── Sidebar/
│   ├── Footer/
│   └── MainLayout/
├── forms/
│   ├── Input/
│   ├── Select/
│   ├── Checkbox/
│   ├── DatePicker/
│   └── FileUpload/
├── cards/
│   ├── ShipmentCard/
│   ├── CourierCard/
│   ├── ReviewCard/
│   └── TransactionCard/
└── modals/
    ├── ConfirmModal/
    ├── EditModal/
    └── ViewModal/
```

## 🔐 Authentication Flow

```
1. User Login
   ↓
2. Send credentials to /api/v1/auth/login/
   ↓
3. Receive access & refresh tokens
   ↓
4. Store tokens in localStorage/cookie
   ↓
5. Add access token to Authorization header
   ↓
6. Include token in all API requests
   ↓
7. On token expiry, use refresh token to get new access token
   ↓
8. Auto-redirect to login on 401
```

## 📍 Real-time Features

### WebSocket Integration
```typescript
// hooks/useSocket.ts
export const useSocket = () => {
  const [socket, setSocket] = useState(null);
  
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const ws = new WebSocket(
      `ws://localhost:8000/ws/tracker/${shipmentId}/${token}/`
    );
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Update location or status
    };
    
    return () => ws.close();
  }, [shipmentId]);
  
  return socket;
};
```

### Location Tracking
```typescript
// hooks/useLocation.ts
export const useLocation = (isTracking: boolean) => {
  const [location, setLocation] = useState(null);
  
  useEffect(() => {
    if (!isTracking) return;
    
    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude
        });
        // Send to backend
      },
      (error) => console.error(error),
      { enableHighAccuracy: true, maximumAge: 1000 }
    );
    
    return () => navigator.geolocation.clearWatch(watchId);
  }, [isTracking]);
  
  return location;
};
```

## 🎯 Page Structure

### Customer Dashboard
```
+─────────────────────────────────────────+
|  Logo          Search        User Menu  |
+─────────────────────────────────────────+
|                                         |
| Quick Stats:  Active Orders | Total     |
|               Saved | Earnings |        |
|                                         |
| Recent Orders                           |
| [Order 1] [Order 2] [Order 3]          |
|                                         |
| Quick Actions                           |
| [Schedule] [Track] [Request] [Support]  |
|                                         |
+─────────────────────────────────────────+
```

### Courier Dashboard
```
+─────────────────────────────────────────+
| Logo         Status: Online  Earnings   |
+─────────────────────────────────────────+
|                                         |
| Map with:                               |
| - My Location                           |
| - Available Orders                      |
| - Nearby Customers                      |
|                                         |
| Current Deliveries:                     |
| [In Progress] [Completed] [Cancelled]   |
|                                         |
| Quick Stats:                            |
| Today's Earnings | Deliveries | Rating |
|                                         |
+─────────────────────────────────────────+
```

### Tracking Page
```
+─────────────────────────────────────────+
|  Shipment #12345                        |
+─────────────────────────────────────────+
|                                         |
| Status: In Transit                      |
| Estimated: Today 3:00 PM                |
|                                         |
| [Map showing courier location]          |
|                                         |
| Timeline:                               |
| ✓ Order Placed      (1:30 PM)          |
| ✓ Order Confirmed   (1:35 PM)          |
| → Courier Picked Up (2:00 PM)          |
| ○ Out for Delivery  (2:15 PM)          |
| ○ Delivered         (3:00 PM)          |
|                                         |
| Courier Details:                        |
| [Profile] Rating: 4.8 | Distance: 2km  |
|                                         |
+─────────────────────────────────────────+
```

## 📦 Package.json Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "zustand": "^4.4.0",
    "axios": "^1.6.0",
    "zod": "^3.22.0",
    "react-hook-form": "^7.50.0",
    "react-leaflet": "^4.2.0",
    "leaflet": "^1.9.0",
    "recharts": "^2.10.0",
    "socket.io-client": "^4.7.0",
    "date-fns": "^3.0.0",
    "clsx": "^2.0.0",
    "tailwindcss": "^3.4.0",
    "@tailwindcss/forms": "^0.5.0",
    "@tailwindcss/typography": "^0.5.0",
    "lucide-react": "^0.296.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.10.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "jest": "^29.7.0",
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

## 🚀 Getting Started

### 1. Create Next.js Project
```bash
npx create-next-app@latest frontend --typescript --tailwind
cd frontend
```

### 2. Install Dependencies
```bash
npm install
npm install axios zustand react-hook-form zod
npm install react-leaflet leaflet
npm install recharts socket.io-client
npm install lucide-react
```

### 3. Setup Environment
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_MAPS_API_KEY=your_google_maps_api_key
```

### 4. Configure TypeScript
```typescript
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["./components/*"],
      "@/lib/*": ["./lib/*"],
      "@/types/*": ["./types/*"],
      "@/store/*": ["./store/*"]
    }
  }
}
```

### 5. Setup API Client
```typescript
// lib/api-client.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

const client: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
client.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default client;
```

## 📱 Mobile Responsive Design

### Breakpoints
- **Mobile**: < 640px (sm)
- **Tablet**: 640px - 1024px (md, lg)
- **Desktop**: > 1024px (xl, 2xl)

### Mobile-First Approach
```tsx
// Example responsive component
export default function Card() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {/* Cards automatically reflow */}
    </div>
  );
}
```

## 🧪 Testing Strategy

### Unit Tests
```typescript
// components/Button.test.tsx
import { render, screen } from '@testing-library/react';
import Button from './Button';

describe('Button Component', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### Integration Tests
```typescript
// Test user flow from login to dashboard
import { render, screen, waitFor } from '@testing-library/react';
import LoginPage from '@/app/(auth)/login/page';

describe('Login Flow', () => {
  it('should redirect to dashboard on successful login', async () => {
    // Test implementation
  });
});
```

## 🔄 State Management with Zustand

```typescript
// store/authStore.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  login: async (email, password) => {
    const response = await client.post('/auth/login/', { email, password });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    set({ user: response.data.user, token: response.data.access });
  },
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, token: null });
  },
  setUser: (user) => set({ user }),
}));
```

## 🎨 Design System

### Colors
```css
/* variables.css */
:root {
  --primary: #FF6B35;      /* Orange */
  --secondary: #004E89;    /* Blue */
  --success: #2ECC71;      /* Green */
  --warning: #F39C12;      /* Yellow */
  --error: #E74C3C;        /* Red */
  --dark: #2C3E50;         /* Dark */
  --light: #ECF0F1;        /* Light */
}
```

### Typography
- **Display**: 32px, 700 (headings)
- **Heading**: 24px, 600 (section titles)
- **Subheading**: 18px, 600 (subsections)
- **Body**: 16px, 400 (content)
- **Small**: 14px, 400 (labels, hints)
- **Tiny**: 12px, 400 (captions)

### Spacing Scale
- 0, 4, 8, 12, 16, 24, 32, 48, 64, 96px

## 📊 Performance Optimization

### Image Optimization
```tsx
import Image from 'next/image';

<Image
  src="/image.png"
  alt="Description"
  width={400}
  height={300}
  loading="lazy"
  quality={75}
/>
```

### Code Splitting
```tsx
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('@/components/Heavy'), {
  loading: () => <div>Loading...</div>,
});
```

### Performance Metrics
- **FCP**: < 1.8s
- **LCP**: < 2.5s
- **CLS**: < 0.1
- **FID**: < 100ms

---

**Frontend Status**: Architecture defined, ready for implementation
**Estimated Development Time**: 4-6 weeks
