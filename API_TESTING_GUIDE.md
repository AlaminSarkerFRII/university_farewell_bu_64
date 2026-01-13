# API Testing Guide

## Quick Start

### 1. Start the Server
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

### 2. Store Access Token (for convenience)
```bash
export BASE_URL="http://localhost:8000/api"
export EMAIL="admin@farewell.local"
export PASSWORD="admin123"
```

---

## Authentication Tests

### Test 1: Login and Get Token
```bash
curl -X POST $BASE_URL/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$EMAIL'",
    "password": "'$PASSWORD'"
  }' | jq .

# Store the access token
export ACCESS_TOKEN=$(curl -s -X POST $BASE_URL/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$EMAIL'",
    "password": "'$PASSWORD'"
  }' | jq -r '.access')
  
echo "Access Token: $ACCESS_TOKEN"
```

### Test 2: Register New User
```bash
curl -X POST $BASE_URL/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@university.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User",
    "role": "student"
  }' | jq .
```

### Test 3: Verify Token Works
```bash
curl -X GET $BASE_URL/users/profile/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

---

## User Endpoints Tests

### Test 4: Get Current User Profile
```bash
curl -X GET $BASE_URL/users/profile/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 5: Update Profile
```bash
curl -X PUT $BASE_URL/users/update_profile/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "My new bio"
  }' | jq .
```

### Test 6: Change Password
```bash
curl -X POST $BASE_URL/users/change_password/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "'$PASSWORD'",
    "new_password": "newpass123",
    "new_password_confirm": "newpass123"
  }' | jq .
```

### Test 7: List All Users (Admin only)
```bash
curl -X GET "$BASE_URL/users/?page=1" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

---

## Timeline Endpoints Tests

### Test 8: List Timelines
```bash
curl -X GET "$BASE_URL/timelines/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 9: List Timelines with Filters
```bash
# Filter by category
curl -X GET "$BASE_URL/timelines/?category=events" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .

# Filter by published status
curl -X GET "$BASE_URL/timelines/?is_published=true" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .

# Search
curl -X GET "$BASE_URL/timelines/?search=ceremony" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 10: Create Timeline (Organizer/Admin only)
```bash
curl -X POST $BASE_URL/timelines/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Timeline",
    "description": "This is a test timeline",
    "category": "events",
    "start_date": "2024-02-01",
    "end_date": "2024-02-28",
    "is_published": true
  }' | jq .
```

### Test 11: Get Single Timeline
```bash
# Replace {id} with actual timeline ID
curl -X GET "$BASE_URL/timelines/{id}/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 12: Update Timeline
```bash
curl -X PATCH "$BASE_URL/timelines/{id}/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Timeline",
    "description": "Updated description"
  }' | jq .
```

### Test 13: Publish Timeline
```bash
curl -X POST "$BASE_URL/timelines/{id}/publish/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 14: Unpublish Timeline
```bash
curl -X POST "$BASE_URL/timelines/{id}/unpublish/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 15: Feature Timeline
```bash
curl -X POST "$BASE_URL/timelines/{id}/feature/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 16: Get Timeline Events
```bash
curl -X GET "$BASE_URL/timelines/{id}/events/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

---

## Timeline Events Tests

### Test 17: List Events
```bash
curl -X GET "$BASE_URL/timeline-events/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 18: Create Event
```bash
curl -X POST $BASE_URL/timeline-events/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "timeline": "{timeline-id}",
    "title": "Opening Ceremony",
    "description": "Official opening ceremony",
    "event_date": "2024-02-15",
    "location": "Main Auditorium",
    "attendees_count": 500
  }' | jq .
```

### Test 19: Update Event
```bash
curl -X PATCH "$BASE_URL/timeline-events/{id}/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Event Title",
    "attendees_count": 600
  }' | jq .
```

---

## Responsibility Endpoints Tests

### Test 20: List Responsibilities
```bash
curl -X GET "$BASE_URL/responsibilities/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 21: Filter by Status
```bash
curl -X GET "$BASE_URL/responsibilities/?status=pending" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 22: Filter by Priority
```bash
curl -X GET "$BASE_URL/responsibilities/?priority=urgent" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 23: Create Responsibility (Organizer/Admin only)
```bash
curl -X POST $BASE_URL/responsibilities/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Setup decorations",
    "description": "Arrange all decorations for event",
    "category": "{category-id}",
    "priority": "high",
    "status": "pending",
    "due_date": "2024-02-14"
  }' | jq .
```

### Test 24: Update Responsibility Status
```bash
curl -X PATCH "$BASE_URL/responsibilities/{id}/update_status/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }' | jq .
```

### Test 25: Assign Responsibility
```bash
curl -X POST "$BASE_URL/responsibilities/{id}/assign_to/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "{user-id}"
  }' | jq .
```

### Test 26: Get My Responsibilities
```bash
curl -X GET "$BASE_URL/responsibilities/my_responsibilities/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 27: Group by Status
```bash
curl -X GET "$BASE_URL/responsibilities/by_status/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 28: Group by Priority
```bash
curl -X GET "$BASE_URL/responsibilities/by_priority/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

---

## Responsibility Categories Tests

### Test 29: List Categories
```bash
curl -X GET "$BASE_URL/responsibility-categories/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

### Test 30: Create Category (Organizer/Admin only)
```bash
curl -X POST $BASE_URL/responsibility-categories/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Decoration",
    "description": "Event decoration tasks"
  }' | jq .
```

---

## Bash Script for Automated Testing

Create `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api"
EMAIL="admin@farewell.local"
PASSWORD="admin123"

echo "=== API Testing Suite ==="

# Login
echo "1. Testing Login..."
RESPONSE=$(curl -s -X POST $BASE_URL/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$EMAIL'",
    "password": "'$PASSWORD'"
  }')

ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access')
echo "✓ Login successful. Token: ${ACCESS_TOKEN:0:20}..."

# Get profile
echo "2. Testing Get Profile..."
curl -s -X GET $BASE_URL/users/profile/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq '.email'

# List timelines
echo "3. Testing List Timelines..."
curl -s -X GET $BASE_URL/timelines/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq '.count'

# List responsibilities
echo "4. Testing List Responsibilities..."
curl -s -X GET $BASE_URL/responsibilities/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq '.count'

echo "=== Tests Complete ==="
```

Run it:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## Python Testing Script

Create `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"
EMAIL = "admin@farewell.local"
PASSWORD = "admin123"

def test_login():
    """Test login endpoint"""
    print("Testing login...")
    response = requests.post(
        f"{BASE_URL}/auth/login/",
        json={"email": EMAIL, "password": PASSWORD}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Login successful. User: {data['user']['email']}")
    return data['access']

def test_get_profile(token):
    """Test get profile endpoint"""
    print("Testing get profile...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/users/profile/",
        headers=headers
    )
    assert response.status_code == 200
    print(f"✓ Profile retrieved: {response.json()['email']}")

def test_list_timelines(token):
    """Test list timelines"""
    print("Testing list timelines...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/timelines/",
        headers=headers
    )
    assert response.status_code == 200
    count = response.json()['count']
    print(f"✓ Found {count} timelines")

def test_list_responsibilities(token):
    """Test list responsibilities"""
    print("Testing list responsibilities...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/responsibilities/",
        headers=headers
    )
    assert response.status_code == 200
    count = response.json()['count']
    print(f"✓ Found {count} responsibilities")

if __name__ == "__main__":
    print("=== API Testing Suite ===\n")
    try:
        token = test_login()
        test_get_profile(token)
        test_list_timelines(token)
        test_list_responsibilities(token)
        print("\n=== All Tests Passed ===")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
```

Run it:
```bash
pip install requests
python test_api.py
```

---

## Postman Collection

Import this JSON into Postman as a collection:

```json
{
  "info": {
    "name": "Versity Farewell API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\"email\": \"admin@farewell.local\", \"password\": \"admin123\"}"
            },
            "url": {"raw": "{{base_url}}/api/auth/login/", "host": ["{{base_url}}"], "path": ["api", "auth", "login"]}
          }
        }
      ]
    },
    {
      "name": "Users",
      "item": [
        {
          "name": "Get Profile",
          "request": {
            "method": "GET",
            "header": [{"key": "Authorization", "value": "Bearer {{access_token}}"}],
            "url": {"raw": "{{base_url}}/api/users/profile/", "host": ["{{base_url}}"], "path": ["api", "users", "profile"]}
          }
        }
      ]
    }
  ],
  "variable": [
    {"key": "base_url", "value": "http://localhost:8000"},
    {"key": "access_token", "value": ""}
  ]
}
```

---

## Common Issues & Solutions

### Issue: 401 Unauthorized
**Solution**: Ensure your access token is valid and not expired. Get a new token using the login endpoint.

### Issue: 403 Forbidden
**Solution**: Check your user's role. Some endpoints require specific roles (organizer, admin, treasurer).

### Issue: 404 Not Found
**Solution**: Verify the endpoint path is correct and the resource ID exists.

### Issue: 400 Bad Request
**Solution**: Check your request body format. Use `jq .` in curl to pretty-print JSON errors.

### Issue: Server Not Responding
**Solution**: 
1. Ensure Django server is running: `ps aux | grep runserver`
2. Check if port 8000 is in use: `lsof -i :8000`
3. Restart server: `pkill -f runserver && python manage.py runserver 0.0.0.0:8000`

---

## Next Steps

1. ✅ Run all 30 tests above
2. ✅ Fix any failing tests
3. ✅ Document API with Swagger (drf-spectacular)
4. ✅ Add integration tests
5. ✅ Start frontend development

