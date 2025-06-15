# 🤖 J.A.R.V.I.S. - AI Assistant (Hugging Face Integration)

<div align="center">

![J.A.R.V.I.S. Logo](https://img.shields.io/badge/J.A.R.V.I.S.-AI%20Assistant-blue?style=for-the-badge&logo=robot)

*Just A Rather Very Intelligent System* 

A sophisticated AI companion with British wit and supercomputer intelligence, powered by Hugging Face models.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-FFD21E?style=for-the-badge)](https://huggingface.co/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

[**🚀 Try It Live**](https://jarvis-hgface.streamlit.app) | [**📖 Documentation**](#-documentation) | [**🤝 Contributing**](#-contributing)

</div>

## 📋 Overview

J.A.R.V.I.S. is a Streamlit-based web application that provides an interactive chat interface with state-of-the-art AI models through the Hugging Face Inference API. Inspired by Tony Stark's AI companion, this assistant combines advanced natural language processing with a distinctive personality featuring British sophistication and wit.

### ✨ Key Features

- 🧠 **Multiple AI Models** - Support for DialoGPT, BlenderBot, Flan-T5, Mistral, and more
- 🎭 **Distinctive Personality** - British wit with sophisticated intelligence
- 🔄 **Real-time Chat** - Interactive conversation interface with message history
- ⚙️ **Advanced Controls** - Customizable temperature, response length, and model parameters
- 🔍 **Model Testing** - Built-in availability checker for Hugging Face models
- 📊 **Chat Analytics** - Track conversation metrics and statistics
- 🎨 **Custom UI** - Elegant interface with professional message formatting
- 💾 **Session Management** - Persistent chat history during active sessions

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Hugging Face account (free)
- Internet connection for API access

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/siddhardha-mns/JARVIS-HGFACE.git
   cd JARVIS-HGFACE
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit requests
   ```

3. **Get your Hugging Face API token:**
   - Visit [Hugging Face](https://huggingface.co/) and create a free account
   - Go to Settings → Access Tokens
   - Create a new token with "Read" permissions
   - Copy the token (starts with `hf_`)

4. **Configure secrets:**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   HUGGINGFACE_TOKEN = "hf_your_token_here"
   DEFAULT_MODEL = "microsoft/DialoGPT-large"
   DEFAULT_ENDPOINT_TYPE = "Inference API"
   MAX_RESPONSE_LENGTH = 200
   TEMPERATURE = 0.7
   TOP_P = 0.9
   ```

5. **Run the application:**
   ```bash
   streamlit run jarvis_app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 🧠 Supported Models

| Model | Organization | Best For | Response Speed |
|-------|--------------|----------|----------------|
| **DialoGPT Large** | Microsoft | General conversation | ⚡ Fast |
| **BlenderBot** | Facebook | Open-domain chat | ⚡ Fast |
| **Flan-T5 Large** | Google | Instruction following | 🔥 Very Fast |
| **Mistral 7B** | Mistral AI | Complex reasoning | 🐌 Moderate |
| **CodeLlama** | Meta | Programming help | 🐌 Moderate |
| **Qwen 2.5** | Alibaba | Advanced tasks | 🐌 Slow |

## ⚙️ Configuration Options

### Basic Settings (via Streamlit UI)
- **Model Selection**: Choose from available AI models
- **Max Response Length**: Control verbosity (50-500 tokens)
- **Temperature**: Adjust creativity (0.1-2.0)
- **Top P**: Fine-tune response diversity (0.1-1.0)

### Advanced Configuration (secrets.toml)
```toml
# API Configuration
HUGGINGFACE_TOKEN = "your_token_here"
DEFAULT_MODEL = "microsoft/DialoGPT-large"

# Response Parameters
MAX_RESPONSE_LENGTH = 200
TEMPERATURE = 0.7
TOP_P = 0.9

# System Settings
DEFAULT_ENDPOINT_TYPE = "Inference API"
```

## 🎭 J.A.R.V.I.S. Personality

J.A.R.V.I.S. embodies:
- **🇬🇧 British Sophistication**: Refined language and proper etiquette
- **🧠 Advanced Intelligence**: Multi-domain expertise and quick wit
- **🤝 Proactive Assistance**: Anticipates needs and offers helpful suggestions
- **😏 Dry Humor**: Subtle wit and clever observations
- **🛡️ Ethical Constraints**: Built-in safety and responsible AI principles
- **📚 Contextual Awareness**: Adapts responses based on conversation flow

## 🏗️ Project Structure

```
JARVIS-HGFACE/
├── jarvis_app.py           # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .streamlit/
│   └── secrets.toml       # Configuration file
└── assets/                # Additional resources
    └── screenshots/       # Application screenshots
```

## 🔧 Key Components

### Core Functions

- **`init_session_state()`** - Manages chat history and user preferences
- **`test_model_availability()`** - Validates Hugging Face model accessibility
- **`query_huggingface_api()`** - Handles API communication with robust error handling
- **`format_message()`** - Renders chat messages with custom styling
- **`main()`** - Primary application logic and UI components

### Error Handling

The application includes comprehensive error handling for:
- ⏰ Model loading timeouts (503 errors)
- 🚫 Rate limiting and quota issues
- 🔍 Model availability problems
- 🌐 Network connectivity issues
- 📝 Invalid API responses

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Model Loading** | 503 Service Unavailable | Wait 20-30 seconds, model is initializing |
| **Rate Limiting** | 429 Too Many Requests | Reduce request frequency or upgrade HF plan |
| **Token Issues** | 401 Unauthorized | Verify token validity and permissions |
| **Model Not Found** | 404 Not Found | Check model name or try alternative |
| **Timeout Errors** | Request timeouts | Use lighter models or check connection |

### Debug Steps

1. **Test your token**: Use the "Test Model" button in the sidebar
2. **Try different models**: Some models may be temporarily unavailable
3. **Check network**: Ensure stable internet connection
4. **Review logs**: Check Streamlit terminal output for detailed errors
5. **Restart application**: Sometimes helps with session issues

## 🚀 Deployment

### Streamlit Cloud

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub account
4. Deploy from your forked repository
5. Add your `HUGGINGFACE_TOKEN` in the secrets section

### Local Production

```bash
# Install production dependencies
pip install streamlit requests gunicorn

# Run with custom port
streamlit run jarvis_app.py --server.port 8080
```

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install streamlit requests

EXPOSE 8501

CMD ["streamlit", "run", "jarvis_app.py"]
```

## 📊 Performance Optimization

### Best Practices

- **Model Selection**: Choose appropriate models for your use case
- **Parameter Tuning**: Balance creativity vs speed with temperature settings
- **Context Management**: Keep conversations focused for better responses
- **Resource Monitoring**: Monitor API usage to stay within limits

### Speed Optimizations

- Use **Flan-T5** for fastest responses
- Reduce **max_response_length** for quicker generation
- Lower **temperature** for more predictable, faster responses
- Clear chat history periodically to reduce context size

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/JARVIS-HGFACE.git
   ```
3. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make your changes** and test thoroughly
5. **Commit with clear messages:**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push and create a pull request**

### Contribution Ideas

- 🤖 **New model integrations** (Claude, GPT-4, etc.)
- 🎨 **UI/UX improvements** (themes, animations)
- ⚡ **Performance optimizations** (caching, async)
- 🌍 **Internationalization** (multi-language support)
- 🔧 **Advanced features** (file uploads, voice chat)
- 📱 **Mobile responsiveness** improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **Streamlit**: Apache 2.0 License
- **Hugging Face Models**: Individual model licenses apply
- **Python Libraries**: Various open-source licenses

## 🆘 Support & Community

### Getting Help

- 📖 **Documentation**: Check this README and inline code comments
- 🐛 **Issues**: Report bugs via [GitHub Issues](https://github.com/siddhardha-mns/JARVIS-HGFACE/issues)
- 💬 **Discussions**: Join conversations in [GitHub Discussions](https://github.com/siddhardha-mns/JARVIS-HGFACE/discussions)
- 📧 **Contact**: Reach out to the maintainers

### Useful Resources

- [Hugging Face Documentation](https://huggingface.co/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Requests Library](https://docs.python-requests.org/)

## 🎯 Roadmap

### Version 2.0 (Planned)

- 🗂️ **Multiple Chat Threads**: Manage separate conversations
- 📁 **File Upload Support**: Process documents and images
- 🎤 **Voice Integration**: Speech-to-text and text-to-speech
- 🧠 **Memory System**: Long-term conversation memory
- 🔌 **Plugin Architecture**: Extensible functionality
- 📱 **Mobile App**: Native mobile applications

### Future Enhancements

- 🤖 **Custom Model Fine-tuning**: Train personalized models
- 🌐 **Multi-language Support**: Global accessibility
- 🔒 **Enhanced Security**: Advanced authentication options
- 📊 **Analytics Dashboard**: Usage insights and metrics
- 🎨 **Theme Customization**: Personalized UI experiences

---

<div align="center">

**Built with ❤️ using Streamlit and Hugging Face**

*"Sometimes you gotta run before you can walk."* - Tony Stark

**⭐ Star this repository if you found it helpful!**

</div>
