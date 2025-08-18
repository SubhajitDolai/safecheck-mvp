import streamlit as st
import requests

st.title("Safecheck MVP Demo")

st.header("Check Email")
email_text = st.text_area("Paste email text here:")
if st.button("Check Email"):
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
