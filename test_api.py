#!/usr/bin/env python3
import requests
import json

def test_email_endpoint():
    url = "http://127.0.0.1:8000/check_email"
    
    # Test phishing email
    phishing_data = {"text": "Your account is locked. Click here to verify: fake-login.com"}
    response = requests.post(url, json=phishing_data)
    print("Phishing Email Test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Test legitimate email
    legit_data = {"text": "Meeting at 3pm today. Please confirm your attendance."}
    response = requests.post(url, json=legit_data)
    print("Legitimate Email Test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health_endpoint():
    url = "http://127.0.0.1:8000/"
    response = requests.get(url)
    print("Health Check:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    try:
        test_health_endpoint()
        test_email_endpoint()
        print("\n✅ All tests completed!")
    except requests.ConnectionError:
        print("❌ Cannot connect to FastAPI server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
