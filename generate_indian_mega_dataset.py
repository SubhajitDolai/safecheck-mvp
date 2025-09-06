#!/usr/bin/env python3
"""
Generate MASSIVE 10,000 INDIA-SPECIFIC email dataset for Safecheck MVP
This will create highly realistic Indian phishing and legitimate emails
Focus on Indian banking, UPI, Aadhaar, PAN, GST, and regional scams
"""

import csv
import random

# Indian Banks and Financial Services
indian_banks = [
    "SBI", "HDFC", "ICICI", "Axis", "Kotak", "IndusInd", "YesBank", "BOB", "PNB", "Canara",
    "UnionBank", "IOB", "BOI", "CentralBank", "Syndicate", "Corporation", "Andhra", "Vijaya",
    "Dena", "Allahabad", "UCO", "IDBI", "Federal", "Karur", "Lakshmi", "Tamilnad", "CSB"
]

# UPI Apps
upi_apps = [
    "PhonePe", "Paytm", "GooglePay", "BHIM", "AmazonPay", "MobiKwik", "FreeCharge", 
    "PayU", "Airtel", "JioMoney", "SBI_Pay", "HDFC_PayZapp", "ICICI_Pockets", "Axis_Pay"
]

# Indian Government Services
gov_services = [
    "Aadhaar", "PAN", "GST", "EPF", "NPS", "DigiLocker", "CoWIN", "UMANG", "MyGov",
    "IncomeeTax", "RTI", "Passport", "DrivingLicense", "VoterID", "RationCard"
]

# Indian Cities
indian_cities = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad",
    "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
    "Visakhapatnam", "Pimpri", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik"
]

# Indian Companies and Services
indian_companies = [
    "TCS", "Infosys", "Wipro", "HCL", "TechMahindra", "Cognizant", "Accenture", "Capgemini",
    "Reliance", "Airtel", "Jio", "Vi", "BSNL", "BigBasket", "Grofers", "Swiggy", "Zomato",
    "Flipkart", "Myntra", "Nykaa", "PolicyBazaar", "BookMyShow", "MakeMyTrip", "OYO"
]

# Legitimate Indian Email Templates
indian_legit_templates = [
    # Banking & Financial
    ("Your {bank} account statement is ready for {month}", "netbanking.{bank}.co.in", "statements@{bank}.co.in", "pass"),
    ("Fixed Deposit of ₹{amount} has matured in your {bank} account", "banking.{bank}.com", "fd@{bank}.co.in", "pass"),
    ("Your {bank} credit card bill of ₹{amount} is due on {date}", "creditcard.{bank}.in", "bills@{bank}.co.in", "pass"),
    ("SIP of ₹{sip_amount} has been deducted from your {bank} account", "mutualfunds.{bank}.in", "sip@{bank}.co.in", "pass"),
    ("Your {bank} home loan EMI of ₹{emi} has been processed", "homeloans.{bank}.co.in", "loans@{bank}.co.in", "pass"),
    ("KYC update completed for your {bank} savings account", "kyc.{bank}.in", "kyc@{bank}.co.in", "pass"),
    ("Cheque book request approved for account ending {account_last4}", "cheques.{bank}.in", "cheques@{bank}.co.in", "pass"),
    ("Interest of ₹{interest} credited to your {bank} savings account", "interest.{bank}.co.in", "interest@{bank}.co.in", "pass"),
    
    # UPI & Digital Payments
    ("₹{amount} received in your {upi} wallet from {sender_name}", "{upi}.com", "transactions@{upi}.com", "pass"),
    ("Your {upi} UPI PIN has been changed successfully", "security.{upi}.in", "security@{upi}.com", "pass"),
    ("Bill payment of ₹{amount} successful via {upi}", "bills.{upi}.com", "bills@{upi}.com", "pass"),
    ("Cashback of ₹{cashback} credited to your {upi} wallet", "rewards.{upi}.in", "cashback@{upi}.com", "pass"),
    ("Your {upi} Gold purchase of ₹{amount} is confirmed", "gold.{upi}.com", "gold@{upi}.com", "pass"),
    ("Train ticket booking confirmed via {upi} for {route}", "travel.{upi}.in", "tickets@{upi}.com", "pass"),
    ("Electricity bill of ₹{amount} paid successfully through {upi}", "utilities.{upi}.com", "bills@{upi}.com", "pass"),
    
    # Government Services
    ("Your Aadhaar card has been updated with new address", "uidai.gov.in", "updates@uidai.gov.in", "pass"),
    ("PAN card application {pan_app_id} is under process", "incometaxindia.gov.in", "pan@incometax.gov.in", "pass"),
    ("GST return for {month} has been filed successfully", "gst.gov.in", "returns@gst.gov.in", "pass"),
    ("EPF balance statement for {financial_year} is ready", "epfindia.gov.in", "statements@epfindia.gov.in", "pass"),
    ("Your passport application {passport_app} is approved", "passportindia.gov.in", "applications@mea.gov.in", "pass"),
    ("Driving license renewal reminder for DL ending {dl_last4}", "parivahan.gov.in", "renewals@transport.gov.in", "pass"),
    ("Voter ID card is ready for collection at {address}", "eci.gov.in", "voterid@eci.gov.in", "pass"),
    ("CoWIN certificate for {vaccine_name} is available", "cowin.gov.in", "certificates@cowin.gov.in", "pass"),
    
    # E-commerce & Services
    ("Your Flipkart order {order_id} has been shipped", "flipkart.com", "orders@flipkart.com", "pass"),
    ("Swiggy order delivered - Rate your experience", "swiggy.com", "feedback@swiggy.com", "pass"),
    ("Your Zomato Gold membership has been activated", "zomato.com", "membership@zomato.com", "pass"),
    ("OYO booking confirmed for {hotel_name} in {city}", "oyorooms.com", "bookings@oyo.com", "pass"),
    ("MakeMyTrip flight booking confirmed for {route}", "makemytrip.com", "bookings@makemytrip.com", "pass"),
    ("BookMyShow tickets for {movie} at {theater} confirmed", "bookmyshow.com", "tickets@bookmyshow.com", "pass"),
    ("BigBasket grocery order delivered to {address}", "bigbasket.com", "delivery@bigbasket.com", "pass"),
    ("Myntra order {order_id} is out for delivery", "myntra.com", "shipping@myntra.com", "pass"),
    
    # Telecom & Utilities
    ("Your Airtel postpaid bill of ₹{amount} is generated", "airtel.in", "bills@airtel.in", "pass"),
    ("Jio recharge of ₹{amount} successful. Validity till {date}", "jio.com", "recharge@jio.com", "pass"),
    ("Vi data pack of {data}GB activated successfully", "vi.com", "services@vi.com", "pass"),
    ("BSNL broadband bill of ₹{amount} due on {date}", "bsnl.co.in", "broadband@bsnl.co.in", "pass"),
    ("BESCOM electricity bill for ₹{amount} generated", "bescom.co.in", "bills@bescom.org", "pass"),
    ("BMTC bus pass recharged with ₹{amount}", "mybmtc.com", "pass@bmtc.gov.in", "pass"),
    ("Gas cylinder booking confirmed for {date} delivery", "iocl.com", "lpg@iocl.co.in", "pass"),
    
    # Education & Professional
    ("CBSE Class {class} results declared on official website", "cbse.gov.in", "results@cbse.nic.in", "pass"),
    ("NEET {year} admit card available for download", "nta.ac.in", "neet@nta.nic.in", "pass"),
    ("JEE Main {year} result published on official portal", "jeemain.nta.nic.in", "jee@nta.nic.in", "pass"),
    ("Your MBA application to {college} has been shortlisted", "{college}.edu", "admissions@{college}.ac.in", "pass"),
    ("TCS offer letter for the position of {position}", "tcs.com", "careers@tcs.com", "pass"),
    ("Infosys joining date confirmed for {date} at {location}", "infosys.com", "onboarding@infosys.com", "pass"),
    ("EPFO UAN {uan} has been activated successfully", "epfindia.gov.in", "uan@epfindia.gov.in", "pass"),
]

# Indian Phishing Email Templates
indian_phishing_templates = [
    # Banking & UPI Scams
    ("URGENT: Your {bank} account will be blocked! Verify KYC immediately", "verify-{bank}.{fake_domain}", "security@fake-{bank}.com", "fail"),
    ("Your {upi} UPI PIN is compromised! Reset now or lose money", "reset-upi.{fake_domain}", "security@fake-{upi}.in", "fail"),
    ("₹{amount} debited from {bank} account! Dispute immediately", "dispute-{bank}.{fake_domain}", "disputes@fake-{bank}.co.in", "fail"),
    ("RBI Alert: Update your {bank} KYC or face penalty", "rbi-kyc.{fake_domain}", "rbi@fake-reserve.gov.in", "fail"),
    ("SEBI: Your trading account suspended! Activate now", "sebi-activate.{fake_domain}", "sebi@fake-securities.gov.in", "fail"),
    ("Income Tax Notice: Pay ₹{amount} penalty or face arrest", "it-penalty.{fake_domain}", "notices@fake-incometax.gov.in", "fail"),
    ("Your {bank} net banking will expire! Renew immediately", "netbank-renew.{fake_domain}", "netbanking@fake-{bank}.in", "fail"),
    ("ALERT: ₹{amount} transaction blocked! Verify identity", "transaction-verify.{fake_domain}", "alerts@fake-{bank}.co.in", "fail"),
    ("Your {upi} account is temporarily locked! Unlock now", "unlock-{upi}.{fake_domain}", "unlock@fake-{upi}.com", "fail"),
    ("FINAL NOTICE: Complete {bank} KYC or account closure", "final-kyc.{fake_domain}", "final@fake-{bank}.co.in", "fail"),
    
    # Government & Document Scams
    ("Aadhaar Card will be cancelled! Update details urgently", "aadhaar-update.{fake_domain}", "update@fake-uidai.gov.in", "fail"),
    ("Your PAN Card is deactivated! Reactivate immediately", "pan-reactivate.{fake_domain}", "pan@fake-incometax.gov.in", "fail"),
    ("GST registration suspended! Pay penalty of ₹{amount}", "gst-penalty.{fake_domain}", "penalty@fake-gst.gov.in", "fail"),
    ("EPF account blocked! Withdraw ₹{amount} before expiry", "epf-withdraw.{fake_domain}", "withdraw@fake-epf.gov.in", "fail"),
    ("Voter ID verification failed! Re-verify to avoid deletion", "voter-verify.{fake_domain}", "verify@fake-eci.gov.in", "fail"),
    ("Passport application rejected! Appeal within 24 hours", "passport-appeal.{fake_domain}", "appeals@fake-passport.gov.in", "fail"),
    ("Driving License expired! Renew online to avoid fine", "dl-renew.{fake_domain}", "renew@fake-transport.gov.in", "fail"),
    ("Ration Card cancelled due to Aadhaar mismatch", "ration-restore.{fake_domain}", "ration@fake-food.gov.in", "fail"),
    ("Property registration papers invalid! Verify ownership", "property-verify.{fake_domain}", "property@fake-revenue.gov.in", "fail"),
    ("Digital India account suspended! Restore access now", "digital-restore.{fake_domain}", "restore@fake-digitalindia.gov.in", "fail"),
    
    # Prize & Lottery Scams (India-specific)
    ("Congratulations! You won ₹{amount} in KBC lottery", "kbc-winner.{fake_domain}", "winner@fake-kbc.sony.in", "fail"),
    ("BCCI IPL contest winner! Claim ₹{amount} prize", "ipl-prize.{fake_domain}", "prizes@fake-bcci.tv", "fail"),
    ("You won ₹{amount} in Flipkart Big Billion Day", "flipkart-winner.{fake_domain}", "winner@fake-flipkart.com", "fail"),
    ("Jio lottery winner! Claim ₹{amount} before expiry", "jio-lottery.{fake_domain}", "lottery@fake-jio.com", "fail"),
    ("Tata Group selected you for ₹{amount} cash prize", "tata-prize.{fake_domain}", "prizes@fake-tata.com", "fail"),
    ("Modi Govt. scheme: Get ₹{amount} financial aid", "modi-scheme.{fake_domain}", "aid@fake-pmjay.gov.in", "fail"),
    ("Ambani Foundation grant of ₹{amount} approved", "ambani-grant.{fake_domain}", "grants@fake-reliance.org", "fail"),
    ("SBI Bank anniversary lottery: ₹{amount} won", "sbi-lottery.{fake_domain}", "lottery@fake-sbi.co.in", "fail"),
    ("Airtel lucky draw winner! Claim ₹{amount} now", "airtel-lucky.{fake_domain}", "lucky@fake-airtel.in", "fail"),
    ("COVID-19 compensation: ₹{amount} from PM CARES", "covid-compensation.{fake_domain}", "compensation@fake-pmcares.gov.in", "fail"),
    
    # Tech Support & App Scams
    ("Your Aadhaar data leaked! Secure now or face misuse", "aadhaar-secure.{fake_domain}", "security@fake-uidai.org", "fail"),
    ("WhatsApp will charge ₹{amount}/year! Pay to continue", "whatsapp-payment.{fake_domain}", "billing@fake-whatsapp.in", "fail"),
    ("Paytm KYC incomplete! Complete or lose ₹{amount}", "paytm-kyc.{fake_domain}", "kyc@fake-paytm.com", "fail"),
    ("Your Google Pay is hacked! Secure ₹{amount} wallet", "gpay-security.{fake_domain}", "security@fake-googlepay.in", "fail"),
    ("PhonePe security breach! Change PIN immediately", "phonepe-breach.{fake_domain}", "security@fake-phonepe.com", "fail"),
    ("BHIM UPI suspended by NPCI! Reactivate now", "bhim-reactivate.{fake_domain}", "npci@fake-bhim.gov.in", "fail"),
    ("Truecaller premium expired! Renew to avoid spam", "truecaller-renew.{fake_domain}", "premium@fake-truecaller.in", "fail"),
    ("Your mobile number will be disconnected! Verify KYC", "mobile-kyc.{fake_domain}", "verify@fake-telecom.in", "fail"),
    ("Swiggy account hacked! Secure your food wallet", "swiggy-security.{fake_domain}", "security@fake-swiggy.com", "fail"),
    ("Zomato Gold membership cancelled! Restore now", "zomato-restore.{fake_domain}", "restore@fake-zomato.com", "fail"),
    
    # Investment & Trading Scams
    ("Stock tip: {stock_name} will rise {percent}%! Invest now", "stock-tips.{fake_domain}", "tips@fake-advisory.com", "fail"),
    ("Zerodha account margin call! Deposit ₹{amount}", "zerodha-margin.{fake_domain}", "margin@fake-zerodha.com", "fail"),
    ("Crypto investment: Turn ₹{amount} into ₹{big_amount}", "crypto-invest.{fake_domain}", "invest@fake-crypto.in", "fail"),
    ("IPO allotment: Pay ₹{amount} to confirm shares", "ipo-payment.{fake_domain}", "allotment@fake-ipo.in", "fail"),
    ("Mutual fund NAV alert! Switch to high return funds", "mf-switch.{fake_domain}", "advisory@fake-mutual.com", "fail"),
    ("Gold rate prediction: Buy now, sell at ₹{gold_rate}", "gold-tips.{fake_domain}", "gold@fake-advisory.in", "fail"),
    ("Real estate investment: {percent}% returns guaranteed", "realestate-invest.{fake_domain}", "invest@fake-property.in", "fail"),
    ("FD interest rates dropping! Invest in our scheme", "fd-scheme.{fake_domain}", "schemes@fake-invest.com", "fail"),
    ("SIP returns poor? Switch to our ₹{amount} plan", "sip-switch.{fake_domain}", "switch@fake-advisory.in", "fail"),
    ("Insurance claim of ₹{amount} approved! Pay processing fee", "insurance-claim.{fake_domain}", "claims@fake-insurance.in", "fail"),
    
    # Job & Education Scams
    ("TCS job offer confirmed! Pay ₹{amount} processing fee", "tcs-job.{fake_domain}", "hiring@fake-tcs.com", "fail"),
    ("Work from home: Earn ₹{amount}/month guaranteed", "wfh-job.{fake_domain}", "jobs@fake-workfromhome.in", "fail"),
    ("IIT admission confirmed! Pay ₹{amount} seat fee", "iit-admission.{fake_domain}", "admissions@fake-iit.ac.in", "fail"),
    ("UPSC result out! Pay ₹{amount} for certificate", "upsc-result.{fake_domain}", "results@fake-upsc.gov.in", "fail"),
    ("Government job: Pay ₹{amount} bribe for selection", "govt-job.{fake_domain}", "selection@fake-ssc.gov.in", "fail"),
    ("MBA scholarship of ₹{amount} approved! Pay fees", "mba-scholarship.{fake_domain}", "scholarship@fake-mba.edu", "fail"),
    ("Online survey job: Earn ₹{amount} daily working part-time", "survey-job.{fake_domain}", "surveys@fake-earn.com", "fail"),
    ("Data entry job: ₹{amount}/month from home", "dataentry-job.{fake_domain}", "dataentry@fake-jobs.in", "fail"),
    ("Medical college admission: Pay ₹{amount} donation", "medical-admission.{fake_domain}", "donations@fake-medical.edu", "fail"),
    ("Engineering placement: Pay ₹{amount} for guaranteed job", "placement-guarantee.{fake_domain}", "placement@fake-engineering.edu", "fail"),
]

# Indian-specific data
indian_amounts = ["5000", "10000", "25000", "50000", "1,00,000", "2,50,000", "5,00,000", "10,00,000", "25,00,000", "50,00,000"]
sip_amounts = ["1000", "2000", "5000", "10000", "15000", "20000", "25000", "30000"]
emi_amounts = ["15000", "25000", "35000", "45000", "55000", "65000", "75000", "85000"]
interest_amounts = ["150", "250", "500", "750", "1000", "1500", "2000", "3000"]
cashback_amounts = ["10", "25", "50", "100", "150", "200", "250", "500"]
bill_amounts = ["150", "300", "500", "800", "1200", "1500", "2000", "2500"]

indian_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
indian_dates = ["15th Jan", "28th Feb", "31st Mar", "15th Apr", "30th Jun", "31st Jul", "15th Aug", "30th Sep", "31st Oct", "30th Nov", "31st Dec"]
financial_years = ["2022-23", "2023-24", "2024-25"]

# Names for UPI transactions
indian_names = [
    "Rahul Sharma", "Priya Singh", "Amit Kumar", "Sneha Patel", "Rajesh Gupta", "Anita Verma",
    "Vikash Yadav", "Pooja Agarwal", "Sanjay Joshi", "Kavita Reddy", "Deepak Mishra", "Sunita Shah",
    "Manoj Tiwari", "Ritu Bansal", "Ashok Pandey", "Neha Srivastava", "Suresh Nair", "Geeta Iyer"
]

# Stock names
indian_stocks = ["Reliance", "TCS", "HDFC Bank", "Infosys", "ITC", "Hindustan Unilever", "SBI", "Bharti Airtel", "Kotak Bank", "ICICI Bank"]

# Routes for travel
indian_routes = ["Delhi-Mumbai", "Bangalore-Chennai", "Hyderabad-Pune", "Kolkata-Guwahati", "Mumbai-Goa", "Delhi-Jaipur", "Chennai-Kochi", "Pune-Ahmedabad"]

# Hotels
indian_hotels = ["Taj Palace", "Oberoi Grand", "ITC Maurya", "Leela Palace", "JW Marriott", "Hyatt Regency", "Hilton Garden", "Radisson Blu"]

# Movies
indian_movies = ["RRR", "KGF Chapter 2", "Pushpa", "Sooryavanshi", "Gangubai Kathiawadi", "Jersey", "Brahmastra", "Vikram", "Laal Singh Chaddha"]

# Theaters
indian_theaters = ["PVR Cinemas", "INOX", "Cinepolis", "Carnival", "SPI Cinemas", "Miraj Cinemas", "Movie Time", "Fun Republic"]

# Fake domains for phishing
fake_domains = ["scam", "phish", "fraud", "fake", "malicious", "suspicious", "bogus", "deceptive", "illegit", "counterfeit", "evil", "bad"]

def generate_indian_email(template, is_phishing=False):
    """Generate a single Indian email from template"""
    text_template, url_template, sender_template, spf = template
    
    # Indian-specific replacements
    replacements = {
        'bank': random.choice(indian_banks),
        'upi': random.choice(upi_apps),
        'gov_service': random.choice(gov_services),
        'city': random.choice(indian_cities),
        'company': random.choice(indian_companies),
        'amount': random.choice(indian_amounts),
        'sip_amount': random.choice(sip_amounts),
        'emi': random.choice(emi_amounts),
        'interest': random.choice(interest_amounts),
        'cashback': random.choice(cashback_amounts),
        'month': random.choice(indian_months),
        'date': random.choice(indian_dates),
        'financial_year': random.choice(financial_years),
        'sender_name': random.choice(indian_names),
        'fake_domain': random.choice(fake_domains),
        'account_last4': str(random.randint(1000, 9999)),
        'pan_app_id': f"PAN{random.randint(100000, 999999)}",
        'passport_app': f"PP{random.randint(1000000, 9999999)}",
        'dl_last4': str(random.randint(1000, 9999)),
        'uan': str(random.randint(100000000000, 999999999999)),
        'order_id': f"OD{random.randint(1000000, 9999999)}",
        'route': random.choice(indian_routes),
        'hotel_name': random.choice(indian_hotels),
        'movie': random.choice(indian_movies),
        'theater': random.choice(indian_theaters),
        'address': f"{random.choice(indian_cities)}, India",
        'data': random.choice(["1.5", "2", "3", "5", "10", "20", "50", "100"]),
        'class': random.choice(["10", "12"]),
        'year': random.choice(["2024", "2025"]),
        'college': random.choice(["IIT Delhi", "IIM Bangalore", "IISc", "NIT Trichy"]),
        'position': random.choice(["Software Engineer", "Data Analyst", "Consultant", "Developer"]),
        'location': random.choice(indian_cities),
        'vaccine_name': random.choice(["Covishield", "Covaxin", "Sputnik V"]),
        'stock_name': random.choice(indian_stocks),
        'percent': str(random.randint(10, 50)),
        'big_amount': random.choice(["10,00,000", "25,00,000", "50,00,000", "1,00,00,000"]),
        'gold_rate': str(random.randint(5500, 6500))
    }
    
    # Apply replacements
    text = text_template
    for key, value in replacements.items():
        text = text.replace(f'{{{key}}}', str(value))
    
    url = url_template
    for key, value in replacements.items():
        url = url.replace(f'{{{key}}}', str(value)) if url != "none" else "none"
    
    sender = sender_template
    for key, value in replacements.items():
        sender = sender.replace(f'{{{key}}}', str(value))
    
    label = "phishing" if is_phishing else "legit"
    
    return [label, text, url, sender, spf]

def main():
    """Generate 10,000 India-specific email samples"""
    print("🇮🇳 Generating 10,000 INDIA-SPECIFIC email samples...")
    print("📍 Focus: Banking, UPI, Government, Regional scams")
    
    emails = []
    
    # Generate 5000 legitimate emails
    print("✅ Generating 5000 legitimate emails...")
    for i in range(5000):
        if i % 500 == 0:
            print(f"   📧 Generated {i} legitimate emails...")
        template = random.choice(indian_legit_templates)
        email = generate_indian_email(template, is_phishing=False)
        emails.append(email)
    
    # Generate 5000 phishing emails
    print("🚨 Generating 5000 phishing emails...")
    for i in range(5000):
        if i % 500 == 0:
            print(f"   ⚠️  Generated {i} phishing emails...")
        template = random.choice(indian_phishing_templates)
        email = generate_indian_email(template, is_phishing=True)
        emails.append(email)
    
    # Shuffle the dataset
    print("🔀 Shuffling dataset...")
    random.shuffle(emails)
    
    # Write to CSV
    print("💾 Writing to CSV file...")
    with open('/Users/swarajpatil/Developer/safecheck-mvp/data/emails_train.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['label', 'text', 'urls', 'sender', 'spfrecord'])
        writer.writerows(emails)
    
    print(f"\n🎉 DATASET GENERATION COMPLETE!")
    print(f"📊 Total samples: {len(emails):,}")
    print(f"   • Legitimate emails: {sum(1 for email in emails if email[0] == 'legit'):,}")
    print(f"   • Phishing emails: {sum(1 for email in emails if email[0] == 'phishing'):,}")
    print(f"\n🇮🇳 INDIA-SPECIFIC FEATURES:")
    print(f"   • {len(indian_banks)} Indian banks covered")
    print(f"   • {len(upi_apps)} UPI apps included") 
    print(f"   • {len(gov_services)} Government services")
    print(f"   • {len(indian_companies)} Indian companies")
    print(f"   • Regional scams and fraud patterns")
    print(f"\n🔥 YOUR MVP IS NOW ENTERPRISE-GRADE FOR INDIA!")

if __name__ == "__main__":
    main()
