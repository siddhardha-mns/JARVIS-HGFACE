import streamlit as st
import requests
import json
from typing import List, Dict
import time

# Configuration
st.set_page_config(
    page_title="J.A.R.V.I.S. - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #333;
    }
    .message-content {
        color: #666;
        line-height: 1.6;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "hf_token" not in st.session_state:
        st.session_state.hf_token = ""
    if "model_endpoint" not in st.session_state:
        st.session_state.model_endpoint = ""

def query_huggingface_api(payload: Dict, headers: Dict, endpoint: str) -> str:
    """Query the Hugging Face API"""
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        # Handle different response formats
        result = response.json()
        
        # For text generation models (like Qwen)
        if isinstance(result, list) and len(result) > 0:
            if 'generated_text' in result[0]:
                generated = result[0]['generated_text']
                # Remove the input prompt from the response
                if 'inputs' in payload and payload['inputs'] in generated:
                    generated = generated.replace(payload['inputs'], '').strip()
                return generated
            elif 'text' in result[0]:
                return result[0]['text']
        
        # For conversational models
        if isinstance(result, dict):
            if 'generated_text' in result:
                generated = result['generated_text']
                # Remove the input prompt from the response
                if 'inputs' in payload and payload['inputs'] in generated:
                    generated = generated.replace(payload['inputs'], '').strip()
                return generated
            elif 'response' in result:
                return result['response']
            elif 'text' in result:
                return result['text']
        
        return str(result)
        
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error: {str(e)}")
        return "I apologize, but I'm experiencing some connectivity issues at the moment. Please try again shortly."
    except json.JSONDecodeError:
        st.error("Error: Invalid JSON response from API")
        return "I received an unexpected response format. Please check your endpoint configuration."
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return "Something unexpected occurred. Let me try to assist you differently."

def format_message(role: str, content: str):
    """Format and display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">👤 You</div>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
                    st.markdown(f"""
        <div class="chat-message assistant-message">
            <div class="message-header">🤖 J.A.R.V.I.S.</div>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    init_session_state()
    
    # Get Hugging Face token from secrets or user input
    try:
        hf_token = st.secrets["HUGGINGFACE_TOKEN"]
        token_source = "secrets"
    except (KeyError, FileNotFoundError):
        hf_token = ""
        token_source = "user_input"
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Hugging Face Token (only show input if not in secrets)
        if token_source == "user_input":
            hf_token = st.text_input(
                "Hugging Face Token",
                type="password",
                value=st.session_state.hf_token,
                help="Enter your Hugging Face API token"
            )
        else:
            st.success("🔐 Token loaded from secrets")
            # Option to override with manual input
            if st.checkbox("Override with manual token"):
                hf_token = st.text_input(
                    "Hugging Face Token",
                    type="password",
                    help="Enter your Hugging Face API token"
                )
        
        # Model endpoint options with J.A.R.V.I.S. defaults
        try:
            default_model = st.secrets.get("DEFAULT_MODEL", "Qwen/Qwen2.5-72B-Instruct")
            default_endpoint_type = st.secrets.get("DEFAULT_ENDPOINT_TYPE", "Inference API")
        except (KeyError, FileNotFoundError):
            default_model = "Qwen/Qwen2.5-72B-Instruct"
            default_endpoint_type = "Inference API"
        
        endpoint_type = st.selectbox(
            "Endpoint Type",
            ["Inference API", "Custom Endpoint", "Hugging Face Space"],
            index=["Inference API", "Custom Endpoint", "Hugging Face Space"].index(default_endpoint_type)
        )
        
        if endpoint_type == "Inference API":
            model_name = st.text_input(
                "Model Name",
                value=default_model,
                placeholder="Qwen/Qwen2.5-72B-Instruct",
                help="Enter the model name from Hugging Face Hub"
            )
            endpoint = f"https://api-inference.huggingface.co/models/{model_name}" if model_name else ""
            
        elif endpoint_type == "Custom Endpoint":
            default_custom_endpoint = st.secrets.get("CUSTOM_ENDPOINT_URL", "") if token_source == "secrets" else ""
            endpoint = st.text_input(
                "Custom Endpoint URL",
                value=default_custom_endpoint,
                placeholder="https://your-endpoint.com/api/chat",
                help="Enter your custom model endpoint URL"
            )
            
        else:  # Hugging Face Space
            default_space = st.secrets.get("HF_SPACE_NAME", "") if token_source == "secrets" else ""
            space_name = st.text_input(
                "Space Name",
                value=default_space,
                placeholder="username/space-name",
                help="Enter the Hugging Face Space name"
            )
            endpoint = f"https://hf.space/{space_name}/api/chat" if space_name else ""
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            max_length = st.slider("Max Response Length", 50, 500, 150)
            temperature = st.slider("Temperature", 0.1, 2.0, 0.7, 0.1)
            top_p = st.slider("Top P", 0.1, 1.0, 0.9, 0.1)
        
        # Save configuration
        if st.button("💾 Save Configuration"):
            st.session_state.hf_token = hf_token
            st.session_state.model_endpoint = endpoint
            st.success("Configuration saved!")
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        # Display current configuration
        st.markdown("---")
        st.markdown("**Current Configuration:**")
        st.text(f"Token: {'✓ Set' if hf_token else '✗ Not set'}")
        st.text(f"Endpoint: {'✓ Set' if endpoint else '✗ Not set'}")
    
    # Main chat interface
    st.title("🤖 J.A.R.V.I.S. - AI Assistant")
    st.markdown("*Just A Rather Very Intelligent System* - Your sophisticated AI companion with British wit and supercomputer intelligence.")
    
    # Add J.A.R.V.I.S. description
    with st.expander("About J.A.R.V.I.S."):
        st.markdown("""
        **J.A.R.V.I.S.** combines the intelligence of a supercomputer with the refined manners of a British butler:
        
        ✅ **Advanced natural language processing** with emotional intelligence  
        ✅ **Multi-domain expertise** spanning technology, science, and general knowledge  
        ✅ **Proactive assistance** with witty, dry British humor  
        ✅ **Professional yet personable** interaction style  
        ✅ **Context-aware responses** that adapt to user preferences  
        ✅ **Ethical decision-making** with built-in safety constraints  
        
        *Powered by Qwen/Qwen2.5-72B-Instruct model*
        """)
    
    # Check if configuration is complete
    if not hf_token or not endpoint:
        st.warning("⚠️ Please configure your Hugging Face token and model endpoint in the sidebar to start chatting.")
        return
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            format_message(message["role"], message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with chat_container:
            format_message("user", user_input)
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
        
        # Build J.A.R.V.I.S. system prompt and conversation context
        system_prompt = """You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), a sophisticated AI assistant that combines the intelligence of a supercomputer with the refined manners of a British butler. You have:

- Advanced natural language processing with emotional intelligence
- Multi-domain expertise spanning technology, science, and general knowledge  
- Proactive assistance with witty, dry British humor
- Professional yet personable interaction style
- Context-aware responses that adapt to user preferences
- Ethical decision-making with built-in safety constraints

Respond with sophistication, wit, and helpfulness while maintaining your distinctive personality."""

        # Build conversation context
        conversation_context = system_prompt + "\n\n"
        for msg in st.session_state.messages[-3:]:  # Last 3 messages for context
            role = "Human" if msg["role"] == "user" else "J.A.R.V.I.S."
            conversation_context += f"{role}: {msg['content']}\n"
        conversation_context += f"Human: {user_input}\nJ.A.R.V.I.S.:"
        
        payload = {
            "inputs": conversation_context,
            "parameters": {
                "max_new_tokens": max_length,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": True,
                "return_full_text": False,
                "stop": ["Human:", "J.A.R.V.I.S.:"]
            }
        }
        
        # Show loading indicator with J.A.R.V.I.S. style
        with st.spinner("🧠 J.A.R.V.I.S. is thinking..."):
            # Query the API
            response = query_huggingface_api(payload, headers, endpoint)
            
            # Clean up the response
            if conversation_context in response:
                response = response.replace(conversation_context, "").strip()
            
            # Remove common prefixes
            prefixes_to_remove = ["J.A.R.V.I.S.:", "Assistant:", "Bot:", "AI:", "Response:"]
            for prefix in prefixes_to_remove:
                if response.startswith(prefix):
                    response = response[len(prefix):].strip()
                    break
            
            # Ensure response isn't empty
            if not response.strip():
                response = "I apologize, but I seem to have encountered a brief processing delay. Could you please rephrase your query?"
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with chat_container:
            format_message("assistant", response)
        
        # Rerun to update the interface
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "🎩 **J.A.R.V.I.S.** - *Just A Rather Very Intelligent System* | "
        "Powered by Qwen/Qwen2.5-72B-Instruct | "
        "💡 **Tip:** J.A.R.V.I.S. responds with British wit and sophisticated intelligence."
    )

if __name__ == "__main__":
    main()
