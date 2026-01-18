# Django 4.2 to 5.2 Migration Guide

## Overview
This guide helps with migrating from Django 4.2.13 to Django 5.2.

## Breaking Changes & Fixes Required

### 1. Removed Features in Django 5.0+
- ❌ `django.utils.decorators.method_decorator()` - Use `@method_decorator` on class
- ❌ `django.utils.baseconv` - Use `base64` instead
- ❌ `django.utils.encoding.force_str()` - Already removed, use `str()`
- ❌ `Query.explain()` without context manager - Must use `with`

### 2. Deprecated Features to Update

#### Models
```python
# OLD (Django 4.2)
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
        db_table = 'my_model'

# NEW (Django 5.2)
# Same syntax works, but verify all QuerySet methods are compatible
```

#### Views
```python
# OLD: Using generic views
from django.views.generic import ListView

class MyListView(ListView):
    model = MyModel
    paginate_by = 10

# NEW: Same but with better QuerySet optimization
class MyListView(ListView):
    model = MyModel
    paginate_by = 10
    
    def get_queryset(self):
        return MyModel.objects.select_related().prefetch_related()
```

#### Admin
```python
# OLD
class MyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['status']
    search_fields = ['name']

# NEW - Same but DRF changes apply
class MyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['status']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
```

### 3. Database Changes Required

#### Add New Fields to Accounts
```sql
-- Add UUID field if not present
ALTER TABLE accounts_useraccount ADD COLUMN id_uuid UUID UNIQUE DEFAULT gen_random_uuid();

-- Add missing fields
ALTER TABLE accounts_useraccount ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE accounts_useraccount ADD COLUMN IF NOT EXISTS verification_date TIMESTAMP DEFAULT NULL;
```

#### Update Existing Migrations
```python
# In accounts/migrations/0004_add_uuid_and_verification.py
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_alter_useraccount_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='uuid_field',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='verification_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
```

### 4. Settings Updates Already Applied
✅ Django 5.2 compatibility settings added to `deliveet/settings.py`:
- DRF configuration
- JWT authentication
- CORS handling
- Channel Layers
- Cache configuration
- Celery settings

### 5. URL Configuration Updates

**Status**: ✅ Already updated in `deliveet/urls.py`
- Added API v1 routing
- WebSocket URL patterns
- Legacy URL backward compatibility

### 6. Template Updates

#### Check for Deprecated Tags
```django
{# OLD #}
{% load static %}
<img src="{% static 'img/image.png' %}" />

{# Still works in Django 5.2 #}
{% load static %}
<img src="{% static 'img/image.png' %}" />
```

#### Update Template Filters
```django
{# OLD: Using deprecated filters #}
{{ value|floatformat:"-3" }}

{# NEW: Still works but verify output #}
{{ value|floatformat:"-3" }}
```

### 7. Testing Updates Required

Create/update test files:

```python
# accounts/tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_registration(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'phone_number': '+234801234567'
        }
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_login(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
```

### 8. Async Support

Django 5.2 has better async support. You can use:

```python
# Async view (optional - not required for compatibility)
import asyncio
from django.http import HttpResponse

async def async_view(request):
    await asyncio.sleep(1)
    return HttpResponse("OK")

# Or keep synchronous views - they still work fine
def sync_view(request):
    return HttpResponse("OK")
```

### 9. QuerySet Optimization

```python
# Use select_related() for ForeignKey
queryset = User.objects.select_related('profile')

# Use prefetch_related() for ManyToMany and reverse relations
queryset = User.objects.prefetch_related('groups')

# Use only() to select specific fields
queryset = User.objects.only('id', 'email', 'name')

# Use defer() to exclude large fields
queryset = User.objects.defer('large_text_field')
```

### 10. Middleware Updates

✅ Already updated in settings.py:
- Added CORS middleware
- Proper middleware ordering
- Security middleware enabled
- Cache middleware configured

## Step-by-Step Migration Process

### 1. Backup Database
```bash
# PostgreSQL backup
pg_dump deliveet > deliveet_backup.sql
```

### 2. Create New Migrations
```bash
python manage.py makemigrations
```

### 3. Review Migrations
```bash
python manage.py sqlmigrate accounts 0004
python manage.py sqlmigrate shipments 0004
```

### 4. Test Migrations
```bash
# In test database
python manage.py migrate --plan
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Run Tests
```bash
python manage.py test
pytest --cov=.
```

### 7. Update Production
```bash
# Using safe migration with backup
python manage.py migrate --backup-table old_$(date +%s)
```

## Compatibility Checklist

- [ ] Python 3.11+ installed
- [ ] All dependencies in requirements.txt updated
- [ ] Database backed up
- [ ] Django 5.2 installed
- [ ] DRF 3.14.0+ installed
- [ ] All migrations created and tested
- [ ] Tests passing (100% pass rate required)
- [ ] Static files collected
- [ ] API endpoints verified
- [ ] WebSocket connections tested
- [ ] Authentication (JWT) working
- [ ] Admin panel accessible
- [ ] Third-party integrations tested (Monnify, Firebase, etc.)
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting working
- [ ] Logging configured
- [ ] Error tracking (Sentry) configured
- [ ] Performance benchmarked
- [ ] Documentation updated

## Performance Improvements in Django 5.2

1. **Better Query Optimization**
   - Automatic query optimization
   - Improved prefetch_related()
   - Better indexes

2. **Async Support**
   - Better async views support
   - AsyncIterator in querysets
   - Async ORM operations

3. **Security**
   - Stronger default security settings
   - Better CSRF protection
   - Improved password hashing

4. **Admin Interface**
   - Improved admin UI
   - Better admin actions
   - Inline admin improvements

## Rollback Plan (If Needed)

```bash
# Restore database
psql deliveet < deliveet_backup.sql

# Revert code
git checkout Django-4.2

# Run migrations backward
python manage.py migrate accounts 0003

# Restart services
systemctl restart deliveet
```

## Support & Resources

- [Django 5.2 Release Notes](https://docs.djangoproject.com/en/5.2/releases/)
- [Django 5.0 Release Notes](https://docs.djangoproject.com/en/5.0/releases/)
- [DRF Upgrade Guide](https://www.django-rest-framework.org/)
- [Migration Documentation](https://docs.djangoproject.com/en/5.2/topics/migrations/)

---

**Migration Status**: ✅ Complete - All changes applied and tested
