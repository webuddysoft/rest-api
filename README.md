# User Management REST API

A simple Python REST API built with FastAPI for user management with JWT authentication, designed to be deployed on Vercel with MySQL.

## Features

- **User Management**: Full CRUD operations for users
- **JWT Authentication**: Token-based authentication with Bearer tokens
- **Database**: MySQL with SQLAlchemy ORM
- **Validation**: Pydantic models with input validation
- **Security**: Password hashing with bcrypt, JWT tokens
- **API Documentation**: Auto-generated with FastAPI
- **CORS Support**: Cross-origin resource sharing enabled
- **Vercel Ready**: Configured for deployment on Vercel

## Authentication System

### Overview
- **Account Creation**: No authentication required
- **Profile Updates/Deletion**: Requires Bearer token authentication
- **Token Expiration**: 30 minutes by default
- **Password Security**: bcrypt hashing (more secure than SHA-256)

### Authentication Flow
1. **Create Account**: `POST /users/` (no auth required)
2. **Login**: `POST /auth/login` → receive Bearer token
3. **Use Token**: Include `Authorization: Bearer <token>` in protected requests
4. **Logout**: `POST /auth/logout` (optional token blacklisting)

## User Model Fields

- `id` (Primary Key)
- `username` (Unique, required)
- `email` (Unique, required)
- `nickname` (Optional)
- `password` (Required, hashed with bcrypt)
- `about_me` (Optional)
- `gender` (Optional)
- `birthdate` (Optional, Date)
- `favorites` (Optional, Text)
- `created_at` (Auto-generated timestamp)
- `updated_at` (Auto-updated timestamp)

## API Endpoints

### Base URL
- **Root**: `GET /` - API status
- **Health Check**: `GET /health` - Health status

### Authentication Endpoints
- **Login**: `POST /auth/login` - Get access token
- **Logout**: `POST /auth/logout` - Logout (requires authentication)

### User Endpoints
- **Create User**: `POST /users/` - Create a new user (no auth required)
- **Get All Users**: `GET /users/` - Get all users with pagination (no auth required)
- **Get User**: `GET /users/{user_id}` - Get specific user by ID (no auth required)
- **Update User**: `PUT /users/{user_id}` - Full update of user (requires auth, own profile only)
- **Patch User**: `PATCH /users/{user_id}` - Partial update of user (requires auth, own profile only)
- **Delete User**: `DELETE /users/{user_id}` - Delete user (requires auth, own profile only)

## Local Development

### Prerequisites
- Python 3.8+
- MySQL database

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd rest-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file
MYSQL_URL=mysql+pymysql://username:password@localhost/database_name
SECRET_KEY=your-super-secret-key-change-this-in-production
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Deployment to Vercel

### Prerequisites
- Vercel account
- Vercel CLI installed
- MySQL database (e.g., PlanetScale, AWS RDS, or your own server)

### Steps

1. **Install Vercel CLI** (if not already installed):
```bash
npm i -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Set up MySQL**:
   - Create a MySQL database (PlanetScale, AWS RDS, etc.)
   - Copy the connection string

4. **Configure Environment Variables**:
   - In your Vercel project settings
   - Add environment variables:
     - `MYSQL_URL` with your MySQL connection string
     - `SECRET_KEY` with a secure secret key for JWT signing

5. **Deploy**:
```bash
vercel --prod
```

### Vercel Configuration

The project includes `vercel.json` which configures:
- Python runtime
- Build settings
- Route handling

## API Usage Examples

### 1. Create a User (No Authentication Required)
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "nickname": "John",
    "about_me": "Software developer",
    "gender": "male",
    "birthdate": "1990-01-01",
    "favorites": "coding,reading,gaming"
  }'
```

### 2. Login to Get Access Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "john_doe"
}
```

### 3. Update User Profile (Requires Authentication)
```bash
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "username": "john_doe_updated",
    "email": "john.updated@example.com",
    "nickname": "Johnny",
    "about_me": "Senior Software Developer",
    "gender": "male",
    "birthdate": "1990-01-01",
    "favorites": "coding,reading,gaming,traveling"
  }'
```

### 4. Patch User Profile (Partial Update)
```bash
curl -X PATCH "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "nickname": "Johnny Boy"
  }'
```

### 5. Delete User (Requires Authentication)
```bash
curl -X DELETE "http://localhost:8000/users/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 6. Get User Profile (No Authentication Required)
```bash
curl -X GET "http://localhost:8000/users/1"
```

### 7. Logout (Optional)
```bash
curl -X POST "http://localhost:8000/auth/logout" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Testing the Authentication

Run the included test script to verify the authentication flow:

```bash
python test_auth.py
```

This script will:
1. Create a test user
2. Login to get a token
3. Test protected endpoints
4. Verify authorization rules

## Project Structure

```
rest-api/
├── main.py          # FastAPI application and routes
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic request/response models
├── crud.py          # Database CRUD operations
├── auth.py          # JWT authentication functions
├── database.py      # Database configuration
├── requirements.txt # Python dependencies
├── test_auth.py     # Authentication test script
├── vercel.json      # Vercel deployment configuration
└── README.md        # This file
```

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid input data or constraint violations
- **401 Unauthorized**: Invalid or missing authentication token
- **403 Forbidden**: User trying to modify another user's profile
- **404 Not Found**: User not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server errors

## Security Features

- **Password Security**: bcrypt hashing (industry standard)
- **JWT Tokens**: Secure token-based authentication
- **Token Expiration**: Automatic token expiration (30 minutes)
- **Authorization**: Users can only modify their own profiles
- **Input Validation**: Pydantic validation for all inputs
- **Token Blacklisting**: Support for token invalidation (logout)

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MYSQL_URL` | MySQL connection string | Yes | - |
| `SECRET_KEY` | JWT signing secret key | Yes | "your-secret-key-change-this-in-production" |

## Security Best Practices

1. **Change the SECRET_KEY** in production
2. **Use HTTPS** in production
3. **Set appropriate token expiration** times
4. **Implement rate limiting** for login attempts
5. **Use strong passwords** (enforced by validation)
6. **Regular security audits** of dependencies 