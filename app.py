import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. SETUP & CONFIG
# This loads the .env file where you store your API key
load_dotenv()

st.set_page_config(
    page_title="Nainital AI Guide", 
    page_icon="🏔️",
    layout="wide"
)

# Get API key securely from environment variable
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("⚠️ API key not found! Please ensure your .env file is set up correctly.")
    st.stop()

# Configure the Gemini API
try:
    genai.configure(api_key=api_key)
    # Using the stable 1.5-flash model
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Failed to configure Gemini API: {str(e)}")
    st.stop()

# 2. UI LAYOUT
st.markdown('<div class="main-header"><h1>🏔️ Nainital Local AI Guide</h1></div>', unsafe_allow_html=True)

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 🙏 I'm your local Nainital expert. Ask me about hidden gems, local food, or travel tips!"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask your Nainital travel question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🧠"):
            try:
                system_prompt = f"You are a friendly local expert from Nainital. Answer this: {prompt}"
                response = model.generate_content(system_prompt)
                msg_content = response.text if response else "I couldn't generate a response."
            except Exception as e:
                msg_content = f"⚠️ Sorry, I encountered an error: {str(e)}"
            
            st.markdown(msg_content)
            st.session_state.messages.append({"role": "assistant", "content": msg_content})
