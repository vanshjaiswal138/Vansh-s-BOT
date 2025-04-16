import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable or Streamlit secrets
def get_api_key():
    # First try to get from Streamlit secrets (for cloud deployment)
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        # If not in Streamlit secrets, try environment variable (for local development)
        return os.getenv("GROQ_API_KEY")

# Initialize Groq client with error handling
try:
    api_key = get_api_key()
    if not api_key:
        st.error("No API key found. Please set the GROQ_API_KEY in your environment or Streamlit secrets.")
        st.stop()
    
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing Groq client: {str(e)}")
    st.stop()

# Set page config
st.set_page_config(
    page_title="AI Chat Bot",
    page_icon="🤖",
    layout="centered"
)

# Add title and description
st.title("🤖 AI Chat Bot")
st.markdown("""
    This is an AI-powered chat bot using Groq's API. Ask me anything!
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Get response from Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="deepseek-r1-distill-llama-70b",
            )
            
            # Display the response
            response = chat_completion.choices[0].message.content
            message_placeholder.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_message = f"Error: {str(e)}"
            message_placeholder.error(error_message) 