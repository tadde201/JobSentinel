"""
Login Helper for JobSentinel
Step 1: Register a new user
Step 2: Login with credentials
Step 3: Get JWT token
"""

import json
import requests
from datetime import datetime

BASE_URL = "http://localhost:8002"

def register_user(email, full_name, password):
    """Register a new user"""
    print(f"\n[REGISTER] Creating user: {email}")
    url = f"{BASE_URL}/api/v1/auth/register"
    payload = {
        "email": email,
        "full_name": full_name,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            data = response.json()
            print(f"[SUCCESS] User registered!")
            print(f"  Token: {data['access_token'][:50]}...")
            return data
        else:
            print(f"[ERROR] Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None

def login_user(email, password):
    """Login with email and password"""
    print(f"\n[LOGIN] Logging in as: {email}")
    url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Login successful!")
            print(f"  Access Token: {data['access_token'][:50]}...")
            print(f"  Token Type: {data['token_type']}")
            return data['access_token']
        else:
            print(f"[ERROR] Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None

def get_current_user(token):
    """Get current logged-in user info"""
    print(f"\n[PROFILE] Getting current user info...")
    url = f"{BASE_URL}/api/v1/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] User profile:")
            print(f"  ID: {data.get('user_id')}")
            print(f"  Email: {data.get('email')}")
            print(f"  Name: {data.get('full_name')}")
            print(f"  Active: {data.get('is_active')}")
            return data
        else:
            print(f"[ERROR] Status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None

def main():
    """Complete login workflow"""
    print("\n" + "="*80)
    print("JobSentinel Login Workflow")
    print("="*80)
    
    # Generate unique email
    timestamp = datetime.now().timestamp()
    email = f"testuser_{int(timestamp)}@example.com"
    full_name = "Test User"
    password = "mypassword123"
    
    # Step 1: Register
    print("\n--- STEP 1: REGISTER NEW USER ---")
    register_result = register_user(email, full_name, password)
    if not register_result:
        print("Registration failed. Exiting.")
        return
    
    # Step 2: Login
    print("\n--- STEP 2: LOGIN ---")
    token = login_user(email, password)
    if not token:
        print("Login failed. Exiting.")
        return
    
    # Step 3: Get user profile
    print("\n--- STEP 3: GET USER PROFILE ---")
    user_profile = get_current_user(token)
    
    # Step 4: Show credentials
    print("\n" + "="*80)
    print("LOGIN CREDENTIALS")
    print("="*80)
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Token: {token}")
    print(f"Use this token in requests: Authorization: Bearer {token}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
