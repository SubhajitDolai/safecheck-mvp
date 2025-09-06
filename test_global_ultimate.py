#!/usr/bin/env python3
"""
ULTIMATE GLOBAL TEST: Test our world-class fraud detector
Testing against global fraud patterns from every major country
"""

import joblib
import pandas as pd

# Load our ULTIMATE model
model = joblib.load('models/email_clf.joblib')

def test_global_fraud_detection():
    """Test our model against global fraud examples"""
    
    print("🌍🔥 ULTIMATE GLOBAL FRAUD DETECTION TEST")
    print("Testing world-class accuracy across all countries!")
    print("=" * 60)
    
    # Global test cases - Real fraud patterns from around the world
    global_tests = [
        # USA Banking
        ("URGENT: Your JPMorgan account will be suspended! Verify immediately at verify-jpmorgan.scam", "🇺🇸 USA Banking Scam"),
        ("Your JPMorgan statement for December 2024 is ready", "🇺🇸 USA Legitimate"),
        
        # UK Payment
        ("CRITICAL: Your Revolut account is compromised! Secure now at secure-revolut.phish", "🇬🇧 UK Payment Scam"),
        ("£500 received in your Revolut from Emma_Johnson", "🇬🇧 UK Legitimate"),
        
        # Germany Government
        ("Finanzamt NOTICE: Pay €2,500 penalty immediately or face legal action", "🇩🇪 Germany Gov Scam"),
        ("Your Finanzamt application APP123456 has been approved", "🇩🇪 Germany Legitimate"),
        
        # China Payment
        ("Alipay will charge fees! Pay ¥500 to continue free service", "🇨🇳 China Payment Scam"),
        ("¥1,000 received in your Alipay from Li_Wei", "🇨🇳 China Legitimate"),
        
        # Japan Investment
        ("STOCK TIP: Toyota will rise 150%! Invest ¥500,000 now for guaranteed returns", "🇯🇵 Japan Investment Scam"),
        ("Your investment portfolio summary for December 2024", "🇯🇵 Japan Legitimate"),
        
        # India UPI
        ("PhonePe account will be deleted! Save ₹50,000 now before midnight deadline", "🇮🇳 India UPI Scam"),
        ("₹5,000 received in your PhonePe from Priya_Sharma", "🇮🇳 India Legitimate"),
        
        # Brazil Banking
        ("FINAL NOTICE: Update your Itau details or face closure immediately", "🇧🇷 Brazil Banking Scam"),
        ("Fixed deposit of R$12,500 has matured in your Itau account", "🇧🇷 Brazil Legitimate"),
        
        # UAE Government
        ("Emirates_ID SUSPENDED! Reactivate within 24 hours or lose benefits", "🇦🇪 UAE Gov Scam"),
        ("Your Emirates_ID renewal reminder for document ending 1234", "🇦🇪 UAE Legitimate"),
        
        # Singapore Banking
        ("SECURITY BREACH: DBS customer data compromised! Secure your account immediately", "🇸🇬 Singapore Banking Scam"),
        ("Interest of S$250 credited to your DBS account", "🇸🇬 Singapore Legitimate"),
        
        # Russia Payment
        ("Sberbank_Online AUDIT: Submit transaction history or face ₽75,000 penalty", "🇷🇺 Russia Banking Scam"),
        ("Your Sberbank_Online mobile banking PIN changed successfully", "🇷🇺 Russia Legitimate"),
        
        # Australia Tech
        ("VIRUS DETECTED: Your computer is infected! Clean immediately or lose data", "🇦🇺 Australia Tech Scam"),
        ("Software update available for Mobile_App", "🇦🇺 Australia Legitimate"),
        
        # Mexico Investment
        ("CRYPTO BOOM: Turn MX$25,000 into MX$125,000 guaranteed in 30 days", "🇲🇽 Mexico Investment Scam"),
        ("Dividend of MX$1,500 credited to your account", "🇲🇽 Mexico Legitimate"),
        
        # South Africa Government
        ("SARS NOTICE: Pay R15,000 penalty immediately or face court action", "🇿🇦 South Africa Gov Scam"),
        ("Your SARS application REF789012 has been approved", "🇿🇦 South Africa Legitimate"),
        
        # Switzerland Banking
        ("UBS LICENSE VIOLATION: Pay CHF5,000 fine or face legal consequences", "🇨🇭 Switzerland Banking Scam"),
        ("Your UBS loan EMI of CHF2,500 has been processed", "🇨🇭 Switzerland Legitimate"),
        
        # Canada Payment
        ("Interac e-Transfer will charge fees! Pay C$500 to continue service", "🇨🇦 Canada Payment Scam"),
        ("Bill payment of C$250 successful via Interac", "🇨🇦 Canada Legitimate"),
        
        # France Government
        ("CAF benefits CANCELLED! Restore within 48 hours or lose eligibility", "🇫🇷 France Gov Scam"),
        ("Your CAF statement for Q4 2024 is now available", "🇫🇷 France Legitimate")
    ]
    
    total_tests = len(global_tests)
    correct_predictions = 0
    
    for text, description in global_tests:
        # Predict
        prob = model.predict_proba([text])[0][1]  # Probability of phishing
        prediction = "PHISHING" if prob > 0.5 else "LEGITIMATE"
        
        # Check if correct
        expected = "PHISHING" if "Scam" in description else "LEGITIMATE"
        is_correct = prediction == expected
        correct_predictions += is_correct
        
        # Display result
        confidence = prob if prediction == "PHISHING" else (1 - prob)
        status = "✅ CORRECT" if is_correct else "❌ WRONG"
        print(f"{status} | {description}")
        print(f"   📧 Text: {text[:80]}...")
        print(f"   🎯 Prediction: {prediction} ({confidence:.1%} confidence)")
        print(f"   📊 Phishing Probability: {prob:.3f}")
        print()
    
    # Final accuracy
    accuracy = (correct_predictions / total_tests) * 100
    print("=" * 60)
    print(f"🏆 ULTIMATE GLOBAL TEST RESULTS:")
    print(f"   📊 Total Tests: {total_tests}")
    print(f"   ✅ Correct: {correct_predictions}")
    print(f"   🎯 Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 95:
        print(f"   🌟 WORLD-CLASS PERFORMANCE!")
        print(f"   🚀 READY FOR GLOBAL DEPLOYMENT!")
        print(f"   💥 ULTIMATE FRAUD DETECTOR ACHIEVED!")
    elif accuracy >= 90:
        print(f"   🔥 EXCELLENT GLOBAL PERFORMANCE!")
    else:
        print(f"   📈 Good performance, room for improvement")

if __name__ == "__main__":
    test_global_fraud_detection()
