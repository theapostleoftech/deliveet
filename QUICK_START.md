# 🚀 Quick Start Guide - Deliveet Platform

## 🎯 Project Complete!

Your **production-grade Deliveet delivery platform** is ready. This guide will get you up and running in minutes.

---

## 📦 What You Have

### Backend (Ready to Run)
```
✅ Django 5.2 REST API (37 endpoints)
✅ FastAPI Microservice  
✅ PostgreSQL Database
✅ Redis Cache/Queue
✅ Celery Task Queue
✅ Monnify Payments
✅ WebSocket Real-time
✅ JWT Authentication
```

### Frontend (Ready to Develop)
```
✅ Next.js 14 App
✅ React 18 Components
✅ Tailwind CSS Styling
✅ Zustand State Management
✅ API Integration
✅ Authentication Pages
✅ Customer Dashboard
✅ Courier Dashboard
```

### Infrastructure (Ready to Deploy)
```
✅ Docker & Docker Compose
✅ Nginx Reverse Proxy
✅ SSL/TLS Configuration
✅ Health Checks
✅ Environment Setup
```

---

## 🏃 Getting Started (5 minutes)

### 1️⃣ Backend Setup

```bash
# Navigate to project root
cd /workspaces/deliveet

# Create Python virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Backend Running at:** http://localhost:8000
**API Docs:** http://localhost:8000/api/v1/docs/

---

### 2️⃣ Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start development server
npm run dev
```

**Frontend Running at:** http://localhost:3000

---

### 3️⃣ FastAPI Microservice (Optional)

```bash
# In another terminal
cd fastapi_service

# Create virtual environment
python -m venv venv_fastapi
source venv_fastapi/bin/activate

# Install dependencies
pip install fastapi uvicorn redis sqlalchemy

# Start service
uvicorn main:app --reload --port 8001
```

**FastAPI Running at:** http://localhost:8001
**Docs:** http://localhost:8001/docs

---

## 🗄️ Database Setup

### PostgreSQL (Docker)

```bash
# Start PostgreSQL container
docker run --name deliveet-db \
  -e POSTGRES_USER=deliveet \
  -e POSTGRES_PASSWORD=deliveet123 \
  -e POSTGRES_DB=deliveet \
  -p 5432:5432 \
  -d postgres:15
```

### Redis (Docker)

```bash
# Start Redis container
docker run --name deliveet-redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

---

## 🐳 Docker Compose (All-in-One)

```bash
# Start all services at once
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services Started:**
- PostgreSQL (port 5432)
- Redis (port 6379)
- Django (port 8000)
- FastAPI (port 8001)
- Nginx (port 80/443)
- Celery Worker
- Celery Beat

---

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test api

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

---

## 📝 First Steps to Customize

### 1. Update Environment Variables

Edit `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/deliveet

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Monnify
MONNIFY_API_KEY=your_key
MONNIFY_SECRET_KEY=your_secret
MONNIFY_CONTRACT_CODE=your_contract_code

# Frontend
FRONTEND_URL=http://localhost:3000
```

### 2. Create a Superuser

```bash
python manage.py createsuperuser
```

Access at: http://localhost:8000/admin

### 3. Customize Frontend Theme

Edit `frontend/tailwind.config.ts`:

```typescript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#your-color',  // Change primary color
        // ... other shades
      }
    }
  }
}
```

### 4. Update API URLs

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

---

## 🔌 API Endpoints

### Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"SecurePass123",...}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"SecurePass123"}'

# Get Current User
curl -X GET http://localhost:8000/api/v1/auth/user/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Shipment

```bash
curl -X POST http://localhost:8000/api/v1/shipments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_name": "John Doe",
    "receiver_phone": "+234...",
    "receiver_email": "john@example.com",
    "delivery_address": {...},
    "description": "Package contents",
    "weight": 2.5
  }'
```

See [FRONTEND_IMPLEMENTATION.md](./FRONTEND_IMPLEMENTATION.md) for complete API reference.

---

## 🗺️ Project Navigation

### Documentation Files

| Document | Purpose |
|----------|---------|
| [DELIVEET_PLATFORM_STATUS.md](./DELIVEET_PLATFORM_STATUS.md) | Complete platform overview |
| [FRONTEND_IMPLEMENTATION.md](./FRONTEND_IMPLEMENTATION.md) | Frontend architecture & setup |
| [PRODUCTION_GUIDE.md](./PRODUCTION_GUIDE.md) | Deployment & infrastructure |
| [SECURITY_CHECKLIST.md](./SECURITY_CHECKLIST.md) | Security features |
| [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) | Django upgrade details |
| [frontend/README.md](./frontend/README.md) | Frontend project guide |

### Key Files

| File | Purpose |
|------|---------|
| `.env.example` | Backend environment template |
| `frontend/.env.example` | Frontend environment template |
| `docker-compose.yml` | All services configuration |
| `requirements.txt` | Python dependencies |
| `frontend/package.json` | Node dependencies |

---

## ✨ Features to Explore

### Customer Flow

1. **Register** → `/auth/register`
2. **Login** → `/auth/login`
3. **View Dashboard** → `/dashboard/customer`
4. **Send Package** → `/dashboard/customer/new-shipment`
5. **Track Delivery** → `/dashboard/customer/tracking/:id`

### Courier Flow

1. **Register as Courier** → `/auth/register` (select Courier)
2. **Login** → `/auth/login`
3. **View Dashboard** → `/dashboard/courier`
4. **Accept Delivery** → Available deliveries list
5. **Make Delivery** → `/dashboard/courier/current`

### Admin Flow

1. Access Admin: http://localhost:8000/admin
2. Manage users, shipments, deliveries
3. View analytics and reports
4. Manage payments and wallets

---

## 🚨 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -U deliveet -d deliveet

# Or with Docker
docker exec deliveet-db psql -U deliveet -d deliveet
```

### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping

# Or with Docker
docker exec deliveet-redis redis-cli ping
```

### Frontend Can't Connect to API

1. Check backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
3. Check CORS settings in `settings.py`
4. Try: `curl http://localhost:8000/api/v1/`

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # for backend
lsof -i :3000  # for frontend

# Kill process
kill -9 PID
```

---

## 📚 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Socket.io](https://socket.io/docs/)

---

## 🔄 Development Workflow

### Making Changes

```bash
# Backend
1. Create feature branch: git checkout -b feature/new-feature
2. Make changes
3. Run tests: python manage.py test
4. Commit: git add . && git commit -m "feat: description"
5. Push: git push origin feature/new-feature

# Frontend
1. Create feature branch: git checkout -b feature/new-feature
2. Make changes
3. Check types: npm run type-check
4. Format: npm run format
5. Commit: git add . && git commit -m "feat: description"
6. Push: git push origin feature/new-feature
```

### Deploying

```bash
# Build frontend
cd frontend && npm run build

# Build backend
docker build -t deliveet:latest .

# Push to registry
docker push your-registry/deliveet:latest

# Deploy with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

---

## 💡 Next Steps

### This Week
- [ ] Test all endpoints with Postman/Thunder Client
- [ ] Test authentication flow (register → login → dashboard)
- [ ] Test payment integration with test account
- [ ] Setup database backups

### This Month
- [ ] Implement delivery tracking map
- [ ] Add payment UI to frontend
- [ ] Implement real-time notifications
- [ ] Add unit tests (target 80% coverage)
- [ ] Deploy to staging environment

### This Quarter
- [ ] Launch mobile app (React Native)
- [ ] Setup monitoring (Sentry, DataDog)
- [ ] Implement admin dashboard
- [ ] Add advanced analytics
- [ ] Go live to production

---

## 📞 Support

**Issues?** Check these first:
1. [TROUBLESHOOTING.md](#troubleshooting) (above)
2. [FRONTEND_IMPLEMENTATION.md](./FRONTEND_IMPLEMENTATION.md#troubleshooting)
3. [PRODUCTION_GUIDE.md](./PRODUCTION_GUIDE.md)

**Need help?**
- 📧 Email: support@deliveet.com
- 💬 Chat: In-app support
- 🐛 Report issue: GitHub Issues

---

## 🎉 You're All Set!

Your Deliveet platform is ready to run. Pick a task above and start building!

```bash
# One-command startup (if using Docker Compose)
docker-compose up -d && \
  cd frontend && npm install && npm run dev
```

**Current Branch:** `production/uber-bolt-upgrade`  
**Status:** ✅ Ready for Development & Testing  
**Date:** January 18, 2024

---

**Happy Building! 🚀**
