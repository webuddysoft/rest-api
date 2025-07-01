import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_authentication_flow():
    """Test the complete authentication flow"""
    
    print("🔐 Testing Authentication Flow\n")
    
    # 1. Create a new user (no authentication required)
    print("1. Creating a new user...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "nickname": "Test User",
        "about_me": "This is a test user"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code == 201:
        print("✅ User created successfully!")
        user = response.json()
        print(f"   User ID: {user['id']}")
    else:
        print(f"❌ Failed to create user: {response.text}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 2. Login to get access token
    print("2. Logging in to get access token...")
    login_data = {
        "username": "testuser",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        print("✅ Login successful!")
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"   Access Token: {access_token[:50]}...")
        print(f"   Token Type: {token_data['token_type']}")
        print(f"   User ID: {token_data['user_id']}")
    else:
        print(f"❌ Login failed: {response.text}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 3. Try to update user profile without token (should fail)
    print("3. Trying to update profile without token (should fail)...")
    update_data = {
        "nickname": "Updated Test User",
        "about_me": "This profile has been updated"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user['id']}", json=update_data)
    if response.status_code == 401:
        print("✅ Correctly rejected - authentication required!")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. Update user profile with token (should succeed)
    print("4. Updating profile with Bearer token...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user['id']}", json=update_data, headers=headers)
    if response.status_code == 200:
        print("✅ Profile updated successfully!")
        updated_user = response.json()
        print(f"   New nickname: {updated_user['nickname']}")
        print(f"   New about_me: {updated_user['about_me']}")
    else:
        print(f"❌ Failed to update profile: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. Try to update another user's profile (should fail)
    print("5. Trying to update another user's profile (should fail)...")
    response = requests.put(f"{BASE_URL}/users/999", json=update_data, headers=headers)
    if response.status_code == 403:
        print("✅ Correctly rejected - can only update own profile!")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
    
    print("\n" + "="*50 + "\n")
    
    # 6. Get user profile (no authentication required)
    print("6. Getting user profile (no auth required)...")
    response = requests.get(f"{BASE_URL}/users/{user['id']}")
    if response.status_code == 200:
        print("✅ Profile retrieved successfully!")
        profile = response.json()
        print(f"   Username: {profile['username']}")
        print(f"   Email: {profile['email']}")
        print(f"   Nickname: {profile['nickname']}")
    else:
        print(f"❌ Failed to get profile: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 7. Logout
    print("7. Logging out...")
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    if response.status_code == 200:
        print("✅ Logout successful!")
    else:
        print(f"❌ Logout failed: {response.text}")

if __name__ == "__main__":
    print("🚀 Starting Authentication Test")
    print("Make sure your API is running on http://localhost:8000")
    print("="*50)
    
    try:
        test_authentication_flow()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    print("\n" + "="*50)
    print("🏁 Test completed!") 