import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. SETUP & CONFIG
load_dotenv()

st.set_page_config(
    page_title="Nainital AI Guide", 
    page_icon="🏔️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .footer {
        text-align:center; color:#666; font-size:12px; padding:20px;
    }
    </style>
""", unsafe_allow_html=True)

# Get API key securely
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("⚠️ API key not found! Please ensure your .env file is set up correctly.")
    st.stop()

# Configure the Gemini API
try:
    genai.configure(api_key=api_key)
    # Using the model as requested
    model = genai.GenerativeModel('gemini-2.5-flash')
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
    # 1. Add user message to display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Build context for the AI
    # Combine history into a single string to maintain context
    conversation_context = ""
    for msg in st.session_state.messages:
        conversation_context += f"{msg['role']}: {msg['content']}\n"
    
    system_instruction = "You are a friendly local expert from Nainital. Answer the user's latest question based on the conversation history."
    full_prompt = f"{system_instruction}\n\n{conversation_context}assistant:"
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🧠"):
            try:
                response = model.generate_content(full_prompt)
                msg_content = response.text if response else "I couldn't generate a response."
            except Exception as e:
                msg_content = f"⚠️ Sorry, I encountered an error: {str(e)}"
            
            st.markdown(msg_content)
            # 3. Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": msg_content})

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
<p>⚠️ This AI guide provides general information. Always verify details before planning your trip.</p>
<p>Made with ❤️ for Nainital travelers</p>
</div>
""", unsafe_allow_html=True)
