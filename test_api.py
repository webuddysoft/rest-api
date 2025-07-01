#!/usr/bin/env python3
"""
Simple test script to verify the API functionality
Run this after starting the API server
"""

import requests
import json
from datetime import date

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing User Management API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Create user
    print("\n2. Testing user creation...")
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "securepassword123",
        "nickname": "TestUser",
        "about_me": "This is a test user",
        "gender": "other",
        "birthdate": "1990-01-01",
        "favorites": "coding,reading,gaming"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 201:
            created_user = response.json()
            user_id = created_user['id']
            print(f"✅ User created: ID {user_id}")
        else:
            print(f"❌ User creation failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return
    
    # Test 3: Get all users
    print("\n3. Testing get all users...")
    try:
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users")
        else:
            print(f"❌ Get users failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get users failed: {e}")
    
    # Test 4: Get specific user
    print(f"\n4. Testing get user {user_id}...")
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User retrieved: {user['username']}")
        else:
            print(f"❌ Get user failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get user failed: {e}")
    
    # Test 5: Update user (PUT)
    print(f"\n5. Testing update user {user_id} (PUT)...")
    update_data = {
        "username": "updated_test_user",
        "email": "updated@example.com",
        "nickname": "UpdatedUser",
        "about_me": "This is an updated test user",
        "gender": "other",
        "birthdate": "1990-01-01",
        "favorites": "coding,reading,gaming,traveling"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        if response.status_code == 200:
            updated_user = response.json()
            print(f"✅ User updated: {updated_user['username']}")
        else:
            print(f"❌ Update user failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Update user failed: {e}")
    
    # Test 6: Patch user (PATCH)
    print(f"\n6. Testing patch user {user_id} (PATCH)...")
    patch_data = {
        "nickname": "PatchedUser",
        "favorites": "coding,reading,gaming,traveling,cooking"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/users/{user_id}", json=patch_data)
        if response.status_code == 200:
            patched_user = response.json()
            print(f"✅ User patched: {patched_user['nickname']}")
        else:
            print(f"❌ Patch user failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Patch user failed: {e}")
    
    # Test 7: Delete user
    print(f"\n7. Testing delete user {user_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 204:
            print(f"✅ User deleted successfully")
        else:
            print(f"❌ Delete user failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Delete user failed: {e}")
    
    # Test 8: Verify user is deleted
    print(f"\n8. Verifying user {user_id} is deleted...")
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 404:
            print(f"✅ User deletion verified (404 Not Found)")
        else:
            print(f"❌ User still exists: {response.status_code}")
    except Exception as e:
        print(f"❌ Verification failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")

if __name__ == "__main__":
    test_api() 