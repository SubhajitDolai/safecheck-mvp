import streamlit as st
import requests

st.title("Safecheck MVP Demo")

# Add tabs for different analysis types
tab1, tab2, tab3, tab4 = st.tabs(["📧 Text Email", "📁 EML Files", "🎵 Audio", "🔄 Combined"])

with tab1:
    st.header("Check Email Text")
    st.write("Paste email content (loses hidden links and metadata)")
    email_text = st.text_area("Paste email text here:")
    if st.button("Check Email Text"):
        if email_text:
            resp = requests.post("http://127.0.0.1:8000/check_email", json={"text": email_text})
            if resp.ok:
                out = resp.json()
                st.write(f"Label: {'Suspicious ⚠️' if out['label'] else 'Safe ✅'}")
                st.write(f"Phishing Probability: {out['phish_prob']:.2f}")
            else:
                st.error("API error: " + resp.text)
        else:
            st.warning("Please enter email text.")

with tab2:
    st.header("Advanced EML File Analysis")
    st.write("🔥 **COMPLETE EMAIL ANALYSIS** - Upload .eml files for FULL detection including:")
    st.write("• 🔗 **Hidden links** in buttons and JavaScript")
    st.write("• 📋 **Email headers** and routing information") 
    st.write("• 🛡️ **SPF/DKIM** authentication status")
    st.write("• 🎭 **Obfuscated content** and CSS tricks")
    st.write("• 📧 **Sender spoofing** detection")
    
    st.markdown("---")
    
    eml_file = st.file_uploader(
        "📁 Drag & Drop EML File Here", 
        type=["eml"],
        help="Upload .eml files exported from your email client (Outlook, Gmail, etc.)"
    )
    
    if st.button("🔍 Analyze EML File", type="primary"):
        if eml_file:
            with st.spinner("🔍 Performing deep analysis..."):
                files = {"file": (eml_file.name, eml_file, "message/rfc822")}
                resp = requests.post("http://127.0.0.1:8000/check_eml", files=files)
                
                if resp.ok:
                    out = resp.json()
                    
                    # Main result
                    col1, col2 = st.columns(2)
                    with col1:
                        if out['label']:
                            st.error("🚨 **PHISHING DETECTED**")
                        else:
                            st.success("✅ **EMAIL APPEARS SAFE**")
                    
                    with col2:
                        st.metric("Phishing Probability", f"{out['phish_prob']:.1%}")
                    
                    # Detailed analysis
                    st.markdown("### 📊 Detailed Analysis")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**🔗 Link Analysis**")
                        link_data = out['advanced_analysis']['link_analysis']
                        st.write(f"Total Links: {link_data['total_links']}")
                        st.write(f"Suspicious Links: {link_data['suspicious_links']}")
                        st.write(f"Hidden Links: {link_data['hidden_links']}")
                    
                    with col2:
                        st.markdown("**📧 Header Analysis**")
                        header_data = out['advanced_analysis']['header_analysis']
                        st.write(f"SPF Status: {header_data['spf_status']}")
                        st.write(f"Sender Suspicious: {'Yes' if header_data['sender_suspicious'] else 'No'}")
                        st.write(f"Return Path Mismatch: {'Yes' if header_data['return_path_mismatch'] else 'No'}")
                    
                    with col3:
                        st.markdown("**🎭 Content Analysis**")
                        content_data = out['advanced_analysis']['content_analysis']
                        st.write(f"Has HTML: {'Yes' if content_data['has_html'] else 'No'}")
                        st.write(f"Suspicious Keywords: {content_data['suspicious_keywords']}")
                        st.write(f"JavaScript Redirects: {'Yes' if content_data['javascript_redirects'] else 'No'}")
                    
                    # Risk breakdown
                    st.markdown("### ⚡ Risk Breakdown")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Basic ML Score", f"{out['basic_ml_prob']:.1%}")
                    with col2:
                        st.metric("EML Risk Factors", f"{out['eml_risk_factors']:.1%}")
                    
                    # File info
                    st.markdown("### 📄 File Information")
                    file_info = out['file_info']
                    st.write(f"**Filename:** {file_info['filename']}")
                    st.write(f"**Size:** {file_info['size']:,} bytes")
                    st.write(f"**Parsed Successfully:** {'✅' if file_info['parsed_successfully'] else '❌'}")
                    
                else:
                    st.error("API error: " + resp.text)
        else:
            st.warning("Please upload an .eml file.")

with tab3:
    st.header("Check Audio")
    audio_file = st.file_uploader("Upload audio file (.wav)", type=["wav"])
    if st.button("Check Audio"):
        if audio_file:
            files = {"file": (audio_file.name, audio_file, "audio/wav")}
            resp = requests.post("http://127.0.0.1:8000/check_audio", files=files)
            if resp.ok:
                out = resp.json()
                st.write(f"Label: {'Spoof ⚠️' if out['label'] else 'Genuine ✅'}")
                st.write(f"Spoof Probability: {out['spoof_prob']:.2f}")
            else:
                st.error("API error: " + resp.text)
        else:
            st.warning("Please upload an audio file.")

with tab4:
    st.header("Check Combined")
    combo_email = st.text_area("Email text for combined check:")
    combo_audio = st.file_uploader("Audio file for combined check:", type=["wav"], key="combo_audio")
    if st.button("Check Combined"):
        if combo_email and combo_audio:
            files = {"file": (combo_audio.name, combo_audio, "audio/wav")}
            data = {"text": combo_email}
            resp = requests.post("http://127.0.0.1:8000/check_combined", data=data, files=files)
            if resp.ok:
                out = resp.json()
                st.write(f"Fraud Score: {out.get('fraud_score', 'N/A')}")
                st.write(f"Result: {out.get('result', 'N/A')}")
            else:
                st.error("API error: " + resp.text)
        else:
            st.warning("Please provide both email text and audio file.")
