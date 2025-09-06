#!/usr/bin/env python3
"""
Generate a massive 1000-entry email dataset for Safecheck MVP
This will create realistic phishing and legitimate emails for enterprise-grade training
"""

import csv
import random

# Legitimate email templates
legit_templates = [
    # Business & Work
    ("Your meeting is scheduled for {time}", "none", "{company}@company.com", "pass"),
    ("Invoice #{invoice_num} is attached", "none", "billing@{company}.com", "pass"),
    ("Welcome to {service}! Your account is ready", "{service}.com", "welcome@{service}.com", "pass"),
    ("Your order #{order_num} has shipped", "{company}.com", "orders@{company}.com", "pass"),
    ("Password reset requested for your account", "none", "security@{service}.com", "pass"),
    ("Your subscription to {service} has been renewed", "{service}.com", "billing@{service}.com", "pass"),
    ("Reminder: {event} is tomorrow at {time}", "none", "events@{company}.com", "pass"),
    ("Your payment of ${amount} has been processed", "none", "payments@{company}.com", "pass"),
    ("Course enrollment confirmed for {course}", "{university}.edu", "registrar@{university}.edu", "pass"),
    ("Your appointment is scheduled for {date}", "none", "{service}@clinic.com", "pass"),
    
    # Services & Utilities
    ("Your {service} bill is now available", "{company}.com", "billing@{company}.com", "pass"),
    ("Service appointment confirmed for {date}", "none", "service@{company}.com", "pass"),
    ("Your warranty registration is complete", "{company}.com", "warranty@{company}.com", "pass"),
    ("Monthly statement is ready for review", "{bank}.com", "statements@{bank}.com", "pass"),
    ("Your refund of ${amount} is being processed", "none", "refunds@{company}.com", "pass"),
    ("Prescription ready for pickup", "none", "pharmacy@{clinic}.com", "pass"),
    ("Your insurance claim has been approved", "{insurance}.com", "claims@{insurance}.com", "pass"),
    ("Flight confirmation for {date}", "{airline}.com", "bookings@{airline}.com", "pass"),
    ("Hotel reservation confirmed", "{hotel}.com", "reservations@{hotel}.com", "pass"),
    ("Your rental car is ready for pickup", "{rental}.com", "pickup@{rental}.com", "pass"),
    
    # Technology & Software
    ("Software update available for {product}", "{company}.com", "updates@{company}.com", "pass"),
    ("Your backup completed successfully", "none", "backup@{service}.com", "pass"),
    ("Security scan completed - no threats found", "none", "security@{service}.com", "pass"),
    ("Your data export is ready for download", "{service}.com", "exports@{service}.com", "pass"),
    ("System maintenance scheduled for {date}", "none", "maintenance@{service}.com", "pass"),
    ("Your license has been renewed", "{software}.com", "licensing@{software}.com", "pass"),
    ("Cloud storage usage report", "{service}.com", "storage@{service}.com", "pass"),
    ("Your domain {domain} has been renewed", "{registrar}.com", "renewals@{registrar}.com", "pass"),
    ("SSL certificate installed successfully", "none", "ssl@{service}.com", "pass"),
    ("API key regenerated for security", "none", "api@{service}.com", "pass"),
]

# Phishing email templates
phishing_templates = [
    # Account suspension/verification scams
    ("URGENT: Your {service} account is suspended! Verify now", "verify-{service}.{fake_domain}", "security@fake-{service}.com", "fail"),
    ("Your {bank} account is locked. Click to unlock", "unlock-{bank}.{fake_domain}", "security@fake-{bank}.com", "fail"),
    ("Verify your {service} identity immediately or lose access", "verify-urgent.{fake_domain}", "urgent@fake-{service}.com", "fail"),
    ("Action required: {service} account will be closed", "action-required.{fake_domain}", "alerts@fake-{service}.com", "fail"),
    ("Your {bank} card is blocked. Unblock now", "unblock-card.{fake_domain}", "cards@fake-{bank}.com", "fail"),
    ("FINAL NOTICE: Verify your {service} account", "final-verify.{fake_domain}", "final@fake-{service}.com", "fail"),
    ("Your {service} subscription expired! Renew immediately", "renew-{service}.{fake_domain}", "billing@fake-{service}.com", "fail"),
    ("{bank} fraud alert! Secure your account now", "fraud-alert.{fake_domain}", "fraud@fake-{bank}.com", "fail"),
    ("Your {service} payment failed. Update card details", "payment-failed.{fake_domain}", "billing@fake-{service}.com", "fail"),
    ("Security breach detected! Change password now", "security-breach.{fake_domain}", "security@fake-{service}.com", "fail"),
    
    # Prize/lottery scams
    ("Congratulations! You won ${amount} in {lottery}", "claim-prize.{fake_domain}", "winner@fake-{lottery}.com", "fail"),
    ("You have unclaimed rewards worth ${amount}", "claim-rewards.{fake_domain}", "rewards@fake-company.com", "fail"),
    ("WINNER: Claim your ${amount} prize now!", "winner-claim.{fake_domain}", "prizes@fake-lottery.com", "fail"),
    ("You've won a {prize}! Claim before it expires", "claim-{prize}.{fake_domain}", "claims@fake-contest.com", "fail"),
    ("Lucky winner! ${amount} waiting for you", "lucky-winner.{fake_domain}", "lucky@fake-prize.com", "fail"),
    ("Exclusive offer: Free {product} - Limited time!", "free-{product}.{fake_domain}", "offers@fake-deals.com", "fail"),
    ("You're selected for ${amount} cash reward", "cash-reward.{fake_domain}", "cash@fake-rewards.com", "fail"),
    ("Claim your {brand} gift card worth ${amount}", "giftcard-{brand}.{fake_domain}", "gifts@fake-{brand}.com", "fail"),
    ("Mystery shopper opportunity - Earn ${amount}", "mystery-shop.{fake_domain}", "jobs@fake-mystery.com", "fail"),
    ("Government refund of ${amount} approved", "gov-refund.{fake_domain}", "refunds@fake-gov.org", "fail"),
    
    # Tech support scams
    ("Your computer is infected! Clean now", "virus-removal.{fake_domain}", "support@fake-antivirus.com", "fail"),
    ("Microsoft security alert - Take action now", "ms-security.{fake_domain}", "security@fake-microsoft.com", "fail"),
    ("Your {device} warranty expires today! Extend now", "warranty-{device}.{fake_domain}", "warranty@fake-support.com", "fail"),
    ("{software} license violation detected", "license-violation.{fake_domain}", "legal@fake-{software}.com", "fail"),
    ("System update required - Download immediately", "system-update.{fake_domain}", "updates@fake-system.com", "fail"),
    ("Your {browser} is outdated - Update for security", "browser-update.{fake_domain}", "updates@fake-{browser}.com", "fail"),
    ("Critical security patch available", "security-patch.{fake_domain}", "patches@fake-security.com", "fail"),
    ("Your {os} activation has expired", "activate-{os}.{fake_domain}", "activation@fake-{os}.com", "fail"),
    ("Virus detected on your device - Remove now", "remove-virus.{fake_domain}", "removal@fake-antivirus.com", "fail"),
    ("Your internet speed is slow - Optimize now", "speed-boost.{fake_domain}", "optimize@fake-isp.com", "fail"),
    
    # Financial scams
    ("IRS Notice: You owe ${amount} in back taxes", "irs-payment.{fake_domain}", "notices@fake-irs.gov", "fail"),
    ("Loan approved for ${amount} - Accept now", "loan-approved.{fake_domain}", "loans@fake-lender.com", "fail"),
    ("Credit score boost - Improve by {points} points", "credit-boost.{fake_domain}", "credit@fake-repair.com", "fail"),
    ("Debt forgiveness program - Qualify now", "debt-forgive.{fake_domain}", "forgiveness@fake-debt.com", "fail"),
    ("Stimulus payment of ${amount} unclaimed", "stimulus-claim.{fake_domain}", "stimulus@fake-gov.org", "fail"),
    ("Investment opportunity - {percent}% returns guaranteed", "invest-returns.{fake_domain}", "invest@fake-trading.com", "fail"),
    ("Mortgage rate dropped to {rate}% - Refinance now", "refi-rate.{fake_domain}", "mortgage@fake-lender.com", "fail"),
    ("Insurance claim of ${amount} ready for pickup", "claim-pickup.{fake_domain}", "claims@fake-insurance.com", "fail"),
    ("Social Security benefits increase - Claim now", "ss-benefits.{fake_domain}", "benefits@fake-ssa.gov", "fail"),
    ("Tax refund of ${amount} is processing", "tax-refund.{fake_domain}", "refunds@fake-irs.gov", "fail"),
]

# Data pools for randomization
companies = ["Amazon", "Google", "Microsoft", "Apple", "Netflix", "Spotify", "Adobe", "Zoom", "Slack", "Shopify"]
banks = ["Chase", "BankOfAmerica", "WellsFargo", "Citibank", "CapitalOne", "USBank", "PNC", "Regions"]
services = ["PayPal", "Venmo", "CashApp", "Zelle", "Discord", "WhatsApp", "Instagram", "Facebook", "Twitter", "LinkedIn"]
universities = ["Stanford", "Harvard", "MIT", "Berkeley", "UCLA", "NYU", "Columbia", "Princeton", "Yale", "Chicago"]
fake_domains = ["scam", "fake", "phish", "fraud", "malicious", "suspicious", "bogus", "deceptive", "illegit", "counterfeit"]
amounts = ["500", "1000", "2500", "5000", "10000", "25000", "50000", "100000"]
times = ["9:00 AM", "2:00 PM", "3:30 PM", "10:00 AM", "1:00 PM", "4:00 PM", "11:30 AM", "2:30 PM"]
dates = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "next week", "tomorrow", "next Monday"]

def generate_email(template, is_phishing=False):
    """Generate a single email from template"""
    text_template, url_template, sender_template, spf = template
    
    # Replace placeholders with random values
    replacements = {
        'service': random.choice(services),
        'company': random.choice(companies),
        'bank': random.choice(banks),
        'university': random.choice(universities),
        'amount': random.choice(amounts),
        'time': random.choice(times),
        'date': random.choice(dates),
        'fake_domain': random.choice(fake_domains),
        'invoice_num': str(random.randint(10000, 99999)),
        'order_num': str(random.randint(1000, 9999)),
        'event': random.choice(["team meeting", "quarterly review", "training session", "conference call"]),
        'course': random.choice(["Data Science 101", "Machine Learning", "Web Development", "AI Ethics"]),
        'clinic': random.choice(["MedCenter", "HealthPlus", "CareFirst", "WellnessCorp"]),
        'insurance': random.choice(["StateFarm", "Allstate", "Progressive", "GEICO"]),
        'airline': random.choice(["Delta", "United", "American", "Southwest"]),
        'hotel': random.choice(["Marriott", "Hilton", "Hyatt", "InterContinental"]),
        'rental': random.choice(["Enterprise", "Hertz", "Avis", "Budget"]),
        'product': random.choice(["iPhone", "laptop", "tablet", "smartwatch"]),
        'software': random.choice(["Windows", "Office", "Photoshop", "AutoCAD"]),
        'registrar': random.choice(["GoDaddy", "Namecheap", "Cloudflare", "Network Solutions"]),
        'domain': random.choice(["example.com", "mysite.org", "business.net", "startup.io"]),
        'lottery': random.choice(["PowerBall", "MegaMillions", "StateLottery", "EuroLotto"]),
        'prize': random.choice(["iPhone 15", "MacBook Pro", "Tesla Model 3", "vacation package"]),
        'brand': random.choice(["Amazon", "iTunes", "Google Play", "Walmart"]),
        'device': random.choice(["computer", "laptop", "smartphone", "tablet"]),
        'browser': random.choice(["Chrome", "Firefox", "Safari", "Edge"]),
        'os': random.choice(["Windows", "macOS", "iOS", "Android"]),
        'percent': str(random.randint(15, 50)),
        'rate': f"{random.uniform(2.5, 4.5):.2f}",
        'points': str(random.randint(100, 300))
    }
    
    # Apply replacements
    text = text_template.format(**{k: v for k, v in replacements.items() if k in text_template})
    url = url_template.format(**{k: v for k, v in replacements.items() if k in url_template}) if url_template != "none" else "none"
    sender = sender_template.format(**{k: v for k, v in replacements.items() if k in sender_template})
    
    label = "phishing" if is_phishing else "legit"
    
    return [label, text, url, sender, spf]

def main():
    """Generate 1000 email samples"""
    print("🚀 Generating 1000 email samples for enterprise-grade training...")
    
    emails = []
    
    # Generate 500 legitimate emails
    for i in range(500):
        template = random.choice(legit_templates)
        email = generate_email(template, is_phishing=False)
        emails.append(email)
    
    # Generate 500 phishing emails
    for i in range(500):
        template = random.choice(phishing_templates)
        email = generate_email(template, is_phishing=True)
        emails.append(email)
    
    # Shuffle the dataset
    random.shuffle(emails)
    
    # Write to CSV
    with open('/Users/swarajpatil/Developer/safecheck-mvp/data/emails_train.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['label', 'text', 'urls', 'sender', 'spfrecord'])
        writer.writerows(emails)
    
    print(f"✅ Generated {len(emails)} email samples!")
    print("📊 Dataset composition:")
    print(f"   • Legitimate emails: {sum(1 for email in emails if email[0] == 'legit')}")
    print(f"   • Phishing emails: {sum(1 for email in emails if email[0] == 'phishing')}")
    print("🔥 Your MVP is now ENTERPRISE-GRADE!")

if __name__ == "__main__":
    main()
