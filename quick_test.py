#!/usr/bin/env python3
"""
Quick test script for Safecheck MVP
Tests both email and audio endpoints
"""

import requests
import json
import os

def test_email_detection():
    """Test email phishing detection"""
    print("🔍 Testing Email Detection...")
    url = "http://127.0.0.1:8000/check_email"
    
    test_cases = [
        {
            "text": "Your account is locked. Click here to verify: fake-login.com",
            "expected": "phishing"
        },
        {
            "text": "Meeting at 3pm today. Please confirm your attendance.",
            "expected": "legitimate"
        },
        {
            "text": "URGENT: Your UPI account is suspended! Verify immediately: suspicious-link.com",
            "expected": "phishing"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        try:
            response = requests.post(url, json={"text": case["text"]})
            result = response.json()
            
            print(f"\n📧 Test {i}: {case['expected'].title()} Email")
            print(f"   Text: {case['text'][:50]}...")
            print(f"   Phishing Probability: {result.get('phish_prob', 0):.2f}")
            print(f"   Label: {'Phishing' if result.get('label') == 1 else 'Legitimate'}")
            print(f"   Status: ✅ Success" if response.status_code == 200 else f"   Status: ❌ Error ({response.status_code})")
            
        except Exception as e:
            print(f"   Status: ❌ Error - {e}")

def test_api_health():
    """Test API health endpoint"""
    print("🏥 Testing API Health...")
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ API is running: {result.get('service', 'Unknown')}")
            return True
        else:
            print(f"   ❌ API unhealthy (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to API: {e}")
        return False

def test_audio_samples():
    """Test audio detection with sample files"""
    print("\n🎵 Testing Audio Detection...")
    
    audio_dir = "data/audio"
    samples = [
        ("genuine/real1.wav", "Real"),
        ("genuine/real2.wav", "Real"), 
        ("spoof/spoof1.wav", "Spoof"),
        ("spoof/spoof2.wav", "Spoof")
    ]
    
    url = "http://127.0.0.1:8000/check_audio"
    
    for sample_path, expected in samples:
        full_path = os.path.join(audio_dir, sample_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'rb') as audio_file:
                    files = {'file': (sample_path, audio_file, 'audio/wav')}
                    response = requests.post(url, files=files)
                    
                if response.status_code == 200:
                    result = response.json()
                    print(f"   🎤 {sample_path}")
                    print(f"      Expected: {expected}")
                    print(f"      Spoof Probability: {result.get('spoof_prob', 0):.2f}")
                    print(f"      Label: {'Spoof' if result.get('label') == 1 else 'Genuine'}")
                    print(f"      Status: ✅ Success")
                else:
                    print(f"   🎤 {sample_path}: ❌ Error ({response.status_code})")
                    
            except Exception as e:
                print(f"   🎤 {sample_path}: ❌ Error - {e}")
        else:
            print(f"   🎤 {sample_path}: ❌ File not found")

def main():
    """Run all tests"""
    print("🚀 Safecheck MVP - Quick Test Suite")
    print("=" * 50)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not running. Please start it with:")
        print("   uvicorn app.main:app --reload --port 8000")
        return
    
    # Test email detection
    test_email_detection()
    
    # Test audio detection
    test_audio_samples()
    
    print("\n" + "=" * 50)
    print("🎉 Tests completed!")
    print("\n📊 Next steps:")
    print("   • Open Streamlit UI: http://localhost:8501")
    print("   • View API docs: http://127.0.0.1:8000/docs")
    print("   • Test combined detection in the UI")

if __name__ == "__main__":
    main()
