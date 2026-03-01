import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. SETUP & CONFIG
st.set_page_config(
    page_title="Nainital AI Guide", 
    page_icon="🏔️",
    layout="wide"
)

# Custom CSS for UI
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

# Get API key
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("⚠️ API key not found! Please ensure your .env file is set up correctly.")
    st.stop()

# Configure the Gemini API
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except Exception as e:
    st.error(f"Failed to configure Gemini API: {str(e)}")
    st.stop()

# 2. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("ℹ️ About This Guide")
    st.info("Your local AI expert for Nainital, Uttarakhand.")
    st.subheader("📌 Popular Topics")
    
    topics = {
        "🏞️ Places": "Give me a list of hidden gems and viewpoints in Nainital.",
        "🍽️ Food": "What are some must-try local dishes in Nainital?",
        "🏨 Stay": "What are the best areas for a family stay in Nainital?",
        "🚗 Travel": "What is the best way to travel around Nainital locally?"
    }
    
    for label, query in topics.items():
        if st.button(label, use_container_width=True):
            # Update session state and trigger a rerun immediately
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

# 3. UI LAYOUT & CHAT
st.markdown('<div class="main-header"><h1>🏔️ Nainital Local AI Guide</h1></div>', unsafe_allow_html=True)

# Initialize history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 🙏 Ask me about Nainital travel tips, food, or hidden gems!"}
    ]

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---
# We do NOT use 'value=' here to avoid the TypeError on older Streamlit versions
if prompt := st.chat_input("Ask your Nainital travel question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- AI RESPONSE LOGIC ---
# This block triggers automatically whenever the last message is from the user
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🧠"):
            try:
                # Build context
                conversation_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                full_prompt = f"You are a friendly local expert from Nainital. Answer the user's question clearly.\n\n{conversation_context}\nassistant:"
                
                response = model.generate_content(full_prompt)
                msg_content = response.text if response else "I couldn't generate a response."
                
                # Append response and rerun to update the UI
                st.session_state.messages.append({"role": "assistant", "content": msg_content})
                st.rerun()
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

# Footer (Kept exactly as requested)
st.markdown("---")
st.markdown("""
<div class="footer">
<p>⚠️ Always verify details before planning your trip.</p>
<p>Made with ❤️ for Nainital travelers</p>
</div>
""", unsafe_allow_html=True)
