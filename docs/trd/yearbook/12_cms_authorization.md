# 12. CMS Authorization Documentation

## Overview

This document describes the authentication and authorization system for the Yearbook CMS (Content Management System). The CMS provides secure endpoints for managing yearbook content (teachers, classes, students, settings, and page sections) with role-based access control.

## 1. Authentication Architecture

### 1.1 Authentication Flow

```
User (Browser/Client)
    ↓
    │ POST /api/v1/auth/login
    │ { "username": "superadmin", "password": "superadmin123" }
    ↓
AuthService
    ├─ Verify username exists
    ├─ Verify user is active
    ├─ Verify password (SHA256 hash comparison)
    └─ Generate JWT Access Token (contains user_id, role, exp)
    ↓
    │ Response: { "access_token": "jwt_token...", "token_type": "bearer" }
    ↓
User stores token in localStorage/cookie
    ↓
    │ GET /api/v1/cms/teachers
    │ Header: Authorization: Bearer token...
    ↓
Auth Middleware (get_current_active_user)
    ├─ Extract token from header
    ├─ Decode and validate JWT (signature, expiration)
    ├─ Extract user_id from token payload
    └─ Fetch user from DB and return user object OR raise 401 error
    ↓
    │ ✅ Access granted / ❌ Access denied
    ↓
CMS Endpoint Handler → Response
```

### 1.2 Authentication Methods

#### Method 1: JWT Bearer Token (for CMS endpoints)
- **Location**: `Authorization` HTTP header
- **Format**: `Authorization: Bearer <token>`
- **Token Type**: JSON Web Token (JWT)
- **Token Lifespan**: 1 day (configurable)
- **Validation**: Stateless validation via cryptographic signature. The token payload contains an expiration claim (`exp`).

#### Method 2: Session Token (alternative, if needed)
- Could be implemented via cookies
- Not currently implemented

## 2. User Model & Roles

### 2.1 User Table Schema

```sql
CREATE TABLE users (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2.2 User Roles & Permissions

| Role | Description | Permissions |
|------|-------------|-------------|
| **superadmin** | Full system access | All CRUD operations on all resources |
| **admin** | Administrative access | All CRUD operations on all resources |
| **editor** | Content editing | Create/Update/Read, but not Delete |
| **viewer** | Read-only access | Read-only operations |

### 2.3 Superadmin Credentials

Default superadmin user created via seeder:
- **Username**: `superadmin`
- **Email**: `superadmin@example.com`
- **Password**: `superadmin123` (hashed with SHA256 + salt)
- **Role**: `superadmin`
- **Active**: `true`

⚠️ **Important**: Change default password immediately after first login.

## 3. Password Security

### 3.1 Password Hashing Algorithm

**Algorithm**: SHA256 with cryptographic salt
**Library Suggestion**: `passlib` for industry-standard hashing.
**Implementation**:
```python
# Using passlib (Recommended)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### 3.2 Password Requirements

- **Minimum length**: 6 characters
- **Maximum length**: 255 characters
- **Character set**: No restrictions (supports Unicode)
- **Special characters**: Allowed (recommended for security)

### 3.3 Password Best Practices

1. ✅ Use strong passwords (mixed case, numbers, symbols)
2. ✅ Change default password immediately after first login
3. ✅ Store passwords securely (hashed, never plaintext)
4. ✅ Use HTTPS for all authentication endpoints
5. ❌ Never share password with others
6. ❌ Never log password in application logs
7. ❌ Never send password via unencrypted channels

## 4. Token Management

### 4.1 Token Generation

**Method**: Secrets-based token generation
```python
def generate_token() -> str:
    return secrets.token_urlsafe(32)
```

- **Token Length**: ~43 characters (base64-url encoded 32 bytes)
- **Algorithm**: Cryptographically secure random
- **Entropy**: 256 bits

### 4.2 Token Lifecycle

| Stage | Duration | Description |
|-------|----------|-------------|
| **Generation** | T=0 | Token created after successful login |
| **Valid Usage** | T=0 to T=86400s | Token accepted in API requests |
| **Expired** | T > 86400s | Token rejected, user must re-login |

### 4.3 Token Usage

**Header Format**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Example cURL request**:
```bash
curl -X GET "http://localhost:8000/api/v1/cms/teachers" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4.4 Token Storage (Client-side)

**Recommended approach**:
```javascript
// After successful login
const response = await fetch('/api/v1/auth/login', {
  method: 'POST',
  body: JSON.stringify({
    username: 'superadmin',
    password: 'superadmin123'
  })
});

const data = await response.json();
const token = data.data.access_token;

// Store securely (httpOnly cookie for web, secure storage for mobile)
localStorage.setItem('access_token', token);  // ⚠️ Less secure
// OR preferably use httpOnly cookie via backend Set-Cookie

// Use in subsequent requests
fetch('/api/v1/cms/teachers', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

## 5. CMS Endpoints

### 5.1 Authentication Endpoints

#### 5.1.1 Login
- **Endpoint**: `POST /api/v1/auth/login`
- **Authentication**: None (public endpoint)
- **Request**:
  ```json
  {
    "username": "superadmin",
    "password": "superadmin123"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Login successful",
    "data": {
      "access_token": "Drmhze6EPcv0fN_81Bj-nA",
      "token_type": "bearer",
      "expires_in": 86400
    },
    "timestamp": "2025-01-25T10:30:00Z"
  }
  ```
- **Error Response (401 Unauthorized)**:
  ```json
  {
    "success": false,
    "message": "Invalid credentials",
    "error": "Username or password is incorrect",
    "timestamp": "2025-01-25T10:30:00Z"
  }
  ```

### 5.2 Protected CMS Endpoints

All CMS endpoints require valid Bearer token in `Authorization` header.

#### 5.2.1 Teachers Management
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/cms/teachers` | List all teachers | Bearer |
| GET | `/api/v1/cms/teachers/{id}` | Get teacher by ID | Bearer |
| POST | `/api/v1/cms/teachers` | Create new teacher | Bearer |
| PUT | `/api/v1/cms/teachers/{id}` | Update teacher | Bearer |
| DELETE | `/api/v1/cms/teachers/{id}` | Delete teacher | Bearer |

#### 5.2.2 Classes Management
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/cms/classes` | List all classes | Bearer |
| GET | `/api/v1/cms/classes/{id}` | Get class by ID | Bearer |
| POST | `/api/v1/cms/classes` | Create new class | Bearer |
| PUT | `/api/v1/cms/classes/{id}` | Update class | Bearer |
| DELETE | `/api/v1/cms/classes/{id}` | Delete class | Bearer |

#### 5.2.3 Students Management
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/cms/students` | List all students | Bearer |
| GET | `/api/v1/cms/students/{id}` | Get student by ID | Bearer |
| POST | `/api/v1/cms/students` | Create new student | Bearer |
| PUT | `/api/v1/cms/students/{id}` | Update student | Bearer |
| DELETE | `/api/v1/cms/students/{id}` | Delete student | Bearer |

#### 5.2.4 Settings Management
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/cms/settings` | List all settings | Bearer |
| GET | `/api/v1/cms/settings/{key}` | Get setting by key | Bearer |
| POST | `/api/v1/cms/settings` | Create new setting | Bearer |
| PUT | `/api/v1/cms/settings/{key}` | Update setting | Bearer |
| DELETE | `/api/v1/cms/settings/{key}` | Delete setting | Bearer |

#### 5.2.5 Page Sections Management
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/cms/page-sections` | List all page sections | Bearer |
| GET | `/api/v1/cms/page-sections/{id}` | Get page section by ID | Bearer |
| POST | `/api/v1/cms/page-sections` | Create new page section | Bearer |
| PUT | `/api/v1/cms/page-sections/{id}` | Update page section | Bearer |
| DELETE | `/api/v1/cms/page-sections/{id}` | Delete page section | Bearer |

## 6. HTTP Status Codes

### 6.1 Success Codes
| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request successful, no response body |

### 6.2 Client Error Codes
| Code | Meaning | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid request format or validation failed |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Authenticated but not authorized for resource |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists (e.g., duplicate username) |

### 6.3 Server Error Codes
| Code | Meaning | Description |
|------|---------|-------------|
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Server temporarily unavailable |

## 7. Error Handling

### 7.1 Error Response Format

All errors follow a consistent format:
```json
{
  "success": false,
  "message": "Human-readable error message",
  "error": "Detailed error description",
  "timestamp": "2025-01-25T10:30:00Z"
}
```

### 7.2 Common Error Scenarios

#### 7.2.1 Missing Authentication Header
**Scenario**: User forgets to send `Authorization` header
**Response (401)**:
```json
{
  "success": false,
  "message": "Authentication required",
  "error": "Missing Authorization header",
  "timestamp": "2025-01-25T10:30:00Z"
}
```

#### 7.2.2 Invalid Token
**Scenario**: User sent expired or malformed token
**Response (401)**:
```json
{
  "success": false,
  "message": "Invalid or expired token",
  "error": "Token validation failed",
  "timestamp": "2025-01-25T10:30:00Z"
}
```

#### 7.2.3 Wrong Credentials
**Scenario**: User entered incorrect username/password
**Response (401)**:
```json
{
  "success": false,
  "message": "Authentication failed",
  "error": "Invalid username or password",
  "timestamp": "2025-01-25T10:30:00Z"
}
```

#### 7.2.4 Inactive User
**Scenario**: User account is deactivated
**Response (401)**:
```json
{
  "success": false,
  "message": "Authentication denied",
  "error": "User account is inactive",
  "timestamp": "2025-01-25T10:30:00Z"
}
```

#### 7.2.5 Duplicate Username
**Scenario**: User registration with existing username
**Response (409)**:
```json
{
  "success": false,
  "message": "User registration failed",
  "error": "Username already exists",
  "timestamp": "2025-01-25T10:30:00Z"
}
```

## 8. Implementation Details

### 8.1 Dependencies & Services

#### AuthService (app/services/auth_service.py)
Handles authentication logic:
- `hash_password(password)` - Create SHA256+salt hash
- `verify_password(password, hash)` - Verify password against hash
- `generate_token()` - Create new bearer token
- `login(username, password)` - Authenticate user, return token
- `register_user(user_payload)` - Create new user account
- `get_user_by_uuid(uuid)` - Retrieve user by UUID

#### UserRepository (app/repositories/user_repository.py)
Database queries:
- `find_user_by_username(username)` - Query user by username
- `find_user_by_email(email)` - Query user by email
- `find_user_by_uuid(uuid)` - Query user by UUID
- `create_user(user_data)` - Insert new user
- `check_user_exists(username, email)` - Check if user exists

#### CMS Auth Middleware (app/dependencies/cms_auth.py)
Token validation for CMS endpoints:
- `get_cms_auth(token)` - Validate bearer token
- Returns authenticated user or raises 401 exception

### 8.2 Request/Response Schemas

#### UserLogin (app/schemas/user.py)
```python
class UserLogin(BaseModel):
    username: str  # 3-127 characters
    password: str  # 6+ characters
```

#### TokenResponse
```python
class TokenResponse(BaseModel):
    access_token: str  # Bearer token
    token_type: str  # "bearer"
    expires_in: int  # Seconds (86400 = 24 hours)
```

#### UserDetail
```python
class UserDetail(BaseModel):
    uuid: UUID
    username: str
    email: str
    full_name: str | None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

## 9. Database Seeding

### 9.1 Seeder Function (app/scripts/seed.py)

```python
async def seed_users():
    """Insert superadmin user for CMS access."""
    users_data = [
        {
            "username": "superadmin",
            "email": "superadmin@example.com",
            "password_hash": AuthService.hash_password("superadmin123"),
            "full_name": "Super Administrator",
            "role": "superadmin",
            "is_active": True,
        },
    ]
    # Insert via SQLAlchemy...
```

### 9.2 Running the Seeder

```bash
# Ensure database is migrated first
alembic upgrade head

# Run seeder
python -m app.scripts.seed
```

## 10. Testing

### 10.1 Manual Testing with cURL

#### Step 1: Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "superadmin",
    "password": "superadmin123"
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "YOUR_TOKEN_HERE",
    "token_type": "bearer",
    "expires_in": 86400
  },
  "timestamp": "2025-01-25T10:30:00Z"
}
```

#### Step 2: Use Token to Access CMS
```bash
curl -X GET "http://localhost:8000/api/v1/cms/teachers" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 10.2 Testing with Python

```python
import requests

# Login
login_response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "username": "superadmin",
        "password": "superadmin123"
    }
)

token = login_response.json()["data"]["access_token"]

# Use token
cms_response = requests.get(
    "http://localhost:8000/api/v1/cms/teachers",
    headers={"Authorization": f"Bearer {token}"}
)

print(cms_response.json())
```

## 11. Security Best Practices

### 11.1 Server-Side Security
1. ✅ Always use HTTPS in production
2. ✅ Validate all input data (user login, registration)
3. ✅ Hash passwords using strong algorithms (SHA256 minimum)
4. ✅ Store tokens securely (hashed in database if needed)
5. ✅ Rate-limit login attempts to prevent brute force
6. ✅ Log authentication events (success and failures)
7. ✅ Use environment variables for sensitive config
8. ✅ Implement CORS properly to prevent unauthorized cross-origin requests
9. ✅ Use secure cookies with HttpOnly, Secure, SameSite flags
10. ✅ Regularly update dependencies and apply security patches

### 11.2 Client-Side Security
1. ✅ Store tokens securely (preferably httpOnly cookies)
2. ✅ Implement token refresh mechanism (before expiry)
3. ✅ Clear tokens on logout
4. ✅ Validate SSL/TLS certificates
5. ✅ Use secure channels for password transmission
6. ✅ Don't expose bearer tokens in URLs or logs
7. ✅ Implement CSRF protection
8. ✅ Use Content Security Policy (CSP) headers

## 12. Migration Info

### 12.1 Migration File
- **File**: `alembic/versions/26af1b8d3c2e_create_users_table.py`
- **Description**: Creates users table with uuid, username, email, password_hash, full_name, role, is_active, and timestamps
- **Dependencies**: Previous migration `fc0c544630a4` (page_sections)

### 12.2 Applying Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Verify migration
alembic current
```

## 13. Future Enhancements

### 13.1 Planned Features
- [ ] Multi-factor authentication (MFA)
- [ ] OAuth2 integration
- [ ] Role-based permission matrix
- [ ] Token refresh endpoint
- [ ] User activity logging
- [ ] Password reset functionality
- [ ] Email verification for registration
- [ ] API key authentication for programmatic access
- [ ] Session management with concurrent login limit
- [ ] Device tracking and management

### 13.2 Performance Optimizations
- [ ] Cache authenticated users in Redis
- [ ] Implement token blacklist for logout
- [ ] Add database indexes on username/email/uuid
- [ ] Use connection pooling for database
- [ ] Implement rate limiting middleware

## 14. Troubleshooting

### 14.1 Common Issues

#### Issue: "Invalid credentials" on correct password
**Cause**: User account is inactive
**Solution**: Activate user in database with `UPDATE users SET is_active = true WHERE username = 'superadmin'`

#### Issue: "Missing Authorization header"
**Cause**: Client forgot to send token in request
**Solution**: Ensure Authorization header is sent: `Authorization: Bearer <token>`

#### Issue: "Token validation failed"
**Cause**: Token is expired or malformed
**Solution**: Login again to get new token

#### Issue: Seeder fails with "username already exists"
**Cause**: Superadmin already exists in database
**Solution**: Safe to ignore; seeder skips if users table is not empty

## 15. References

- SQLAlchemy Async Documentation
- FastAPI Dependency Injection Guide
- Python `secrets` module documentation
- OWASP Authentication Cheat Sheet
- RFC 6750 - Bearer Token Usage
