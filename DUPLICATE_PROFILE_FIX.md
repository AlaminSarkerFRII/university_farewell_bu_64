# Duplicate UserProfile Fix

## Issue Summary

**Error:** `django.db.utils.IntegrityError: duplicate key value violates unique constraint "users_userprofile_user_id_key"`

This error occurred during user registration when attempting to create a new user account.

## Root Cause

The application had **duplicate UserProfile creation logic** in two places:

1. **Django Signal** (`backend/users/signals.py`):
   - The `create_user_profile` signal automatically creates a UserProfile whenever a CustomUser is created
   - Triggered by the `post_save` signal on CustomUser model

2. **Serializer** (`backend/users/serializers.py`):
   - The `UserRegisterSerializer.create()` method explicitly called `UserProfile.objects.create(user=user)`
   - This created a race condition where both the signal and serializer tried to create the same profile

### Why This Caused an Error

When a new user was created:
1. The serializer's `create()` method would call `CustomUser.objects.create_user()`
2. This triggered the `post_save` signal, which created a UserProfile
3. Then the serializer tried to create another UserProfile for the same user
4. PostgreSQL rejected the second insert due to the unique constraint on `user_id`

## Solution Applied

**Removed the explicit UserProfile creation from the serializer** since the Django signal already handles this automatically.

### Changes Made

**File:** `backend/users/serializers.py`

**Before:**
```python
def create(self, validated_data):
    """Create and return a new user."""
    password = validated_data.pop('password')
    user = CustomUser.objects.create_user(**validated_data, password=password)
    
    # Create user profile
    UserProfile.objects.create(user=user)  # ❌ DUPLICATE CREATION
    
    # Generate email verification token
    token = str(uuid.uuid4())
    expires_at = timezone.now() + timedelta(hours=24)
    EmailVerificationToken.objects.create(
        user=user,
        token=token,
        expires_at=expires_at
    )
    
    return user
```

**After:**
```python
def create(self, validated_data):
    """Create and return a new user."""
    password = validated_data.pop('password')
    user = CustomUser.objects.create_user(**validated_data, password=password)
    
    # UserProfile is automatically created by the post_save signal
    # No need to create it explicitly here ✅
    
    # Generate email verification token
    token = str(uuid.uuid4())
    expires_at = timezone.now() + timedelta(hours=24)
    EmailVerificationToken.objects.create(
        user=user,
        token=token,
        expires_at=expires_at
    )
    
    return user
```

## How the Signal Works

**File:** `backend/users/signals.py`

```python
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a CustomUser is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
```

This signal:
- Listens for the `post_save` event on CustomUser
- Only runs when a new user is created (`created=True`)
- Uses `get_or_create()` to safely create the profile (preventing duplicates)
- Automatically handles profile creation for ALL user creation methods (admin, API, management commands, etc.)

## Testing the Fix

### 1. Check Backend Status
```bash
docker compose ps
```

Expected output: `farewell_backend` should be running (Up)

### 2. Test User Registration via API

**Endpoint:** `POST /api/auth/register/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid-here",
    "email": "newuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "full_name": "Test User",
    "role": "student",
    "is_email_verified": false,
    "profile_picture": null,
    "bio": "",
    "profile": {
      "phone_number": "",
      "date_of_birth": null,
      "admission_year": null,
      "graduation_year": null,
      "branch": "",
      "roll_number": "",
      "notification_email": true,
      "notification_push": true
    },
    "created_at": "2026-01-13T..."
  },
  "access": "jwt-access-token",
  "refresh": "jwt-refresh-token"
}
```

### 3. Verify in Django Admin

1. Access admin panel: http://localhost:8000/admin/
2. Login with superuser credentials
3. Navigate to **Users** → **User Profiles**
4. Verify that each user has exactly ONE profile

### 4. Check Database Directly

```bash
docker compose exec backend python manage.py shell
```

Then run:
```python
from users.models import CustomUser, UserProfile

# Check that every user has a profile
users_count = CustomUser.objects.count()
profiles_count = UserProfile.objects.count()
print(f"Users: {users_count}, Profiles: {profiles_count}")

# They should be equal
assert users_count == profiles_count, "Mismatch between users and profiles!"
print("✅ All users have profiles!")
```

## Additional Benefits

By relying on the Django signal for profile creation:

1. **Consistency:** Profiles are created for ALL user creation methods (not just registration)
2. **DRY Principle:** No duplicate code across different user creation paths
3. **Maintainability:** Single source of truth for profile creation logic
4. **Safety:** `get_or_create()` prevents accidental duplicates

## Status

✅ **Fix Applied:** Backend restarted with corrected code  
✅ **Service Running:** Gunicorn workers started successfully  
✅ **Ready for Testing:** User registration should now work without errors

## Related Files

- `backend/users/serializers.py` - User registration serializer (MODIFIED)
- `backend/users/signals.py` - User profile creation signal (UNCHANGED)
- `backend/users/models.py` - User and UserProfile models (UNCHANGED)
- `backend/users/apps.py` - App configuration that loads signals (UNCHANGED)
