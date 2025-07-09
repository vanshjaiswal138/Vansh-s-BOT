import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError as e:
    GRAPHVIZ_AVAILABLE = False
    GRAPHVIZ_IMPORT_ERROR = str(e)
import io
from streamlit_mermaid import st_mermaid

# Set page config as the first Streamlit command
st.set_page_config(
    page_title="AI Chat Bot",
    page_icon="🤖",
    layout="centered"
)

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

# Helper to check if prompt requests an image or ER diagram
def is_image_request(prompt):
    keywords = ["show image", "display image", "image of", "picture of"]
    return any(k in prompt.lower() for k in keywords)

def is_er_request(prompt):
    keywords = ["er diagram", "entity relationship diagram", "draw er"]
    return any(k in prompt.lower() for k in keywords)

# Helper to generate a sample image (placeholder, can be replaced with real logic)
def generate_sample_image():
    img = Image.new('RGB', (200, 200), color = (73, 109, 137))
    return img

# Helper to generate a sample ER diagram (placeholder, can be replaced with real logic)
def generate_mermaid_er():
    # Example ER diagram in Mermaid syntax
    mermaid_code = '''
    erDiagram
        CUSTOMER ||--o{ ORDER : places
        ORDER ||--|{ LINE_ITEM : contains
        CUSTOMER }|..|{ DELIVERY_ADDRESS : uses
    '''
    return mermaid_code

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
            # Check for image or ER requests
            if is_image_request(prompt):
                img = generate_sample_image()
                message_placeholder.image(img, caption="Generated Image", use_column_width=True)
                st.session_state.messages.append({"role": "assistant", "content": "[Image generated]"})
            elif is_er_request(prompt):
                mermaid_code = generate_mermaid_er()
                st_mermaid(mermaid_code)
                st.session_state.messages.append({"role": "assistant", "content": "[ER diagram generated with Mermaid]"})
            else:
                # Get response from Groq
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="meta-llama/llama-4-maverick-17b-128e-instruct",
                )
                # Display the response
                response = chat_completion.choices[0].message.content
                message_placeholder.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_message = f"Error: {str(e)}"
            message_placeholder.error(error_message) 