---
title: Gradio Chat
emoji: 💬
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
short_description: Multi-Provider LLM Chatbot powered by LangGraph
---

# 🤖 LangGraph AI Chatbot

A powerful, multi-provider AI chatbot application built with **LangGraph** and **Gradio**, supporting multiple LLM providers including Groq, Gemini, OpenAI, and Ollama.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Gradio](https://img.shields.io/badge/gradio-5.49.1-orange.svg)
![LangGraph](https://img.shields.io/badge/langgraph-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🔄 **Multi-Provider Support**: Switch between Groq, Gemini, OpenAI, and Ollama
- 🧠 **Multiple Models**: Choose from various models for each provider
- 💬 **Full Conversation History**: Maintains context across messages
- 🔑 **Flexible API Configuration**: Enter keys via UI or use environment variables
- 🎨 **Clean UI**: Simple, intuitive Gradio interface
- ⚡ **Real-time Responses**: Fast inference with provider-optimized models

## 🚀 Supported Providers & Models

### Groq
- OpenAI GPT OSS 20B
- Llama 3.1 8B Instant
- GPT OSS 120B
- Llama 3.3 70B Versatile

### OpenAI
- GPT-5 Nano
- GPT-4o Mini
- GPT-5 Mini

### Gemini
- Gemini 2.5 Flash
- Gemini 1.5 Flash

### Ollama (Local)
- Gemma3 1B
- GPT OSS 20B
- DeepSeek R1 8B
- Llama 3.1 8B

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Gradio-Chat.git
cd Gradio-Chat
```

### Install Dependencies

**Using uv (recommended):**
```bash
uv add -r requirements.txt
```

**Using pip:**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Option 1: Environment Variables (for local development)

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
```

### Option 2: UI Configuration (for Hugging Face Spaces)

When running the app, expand the **"🔑 API Keys Configuration"** accordion and enter your API keys directly in the interface. This is perfect for Hugging Face Spaces deployment.

## 🏃 Running the App

### Local Development

```bash
# Activate virtual environment (if using uv)
source .venv/bin/activate

# Run the app
python app.py
```

The app will be available at `http://127.0.0.1:7860`

### Hugging Face Spaces

This app is ready to deploy on Hugging Face Spaces. Simply:

1. Create a new Space on Hugging Face
2. Push this repository to the Space
3. Users can enter their own API keys via the UI

## 📁 Project Structure

```
Gradio-Chat/
├── app.py                          # Main Gradio application
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (not in repo)
├── .gitignore                     # Git ignore file
├── langgraph_agent/               # LangGraph agent implementation
│   ├── graphs/                    # Graph builders
│   │   ├── graph_builder.py       # Main graph builder
│   │   └── basic_chatbot_graph.py # Basic chatbot graph
│   ├── llms/                      # LLM integrations
│   │   ├── groq_llm.py           # Groq integration
│   │   ├── gemini_llm.py         # Gemini integration
│   │   ├── openai_llm.py         # OpenAI integration
│   │   └── ollama_llm.py         # Ollama integration
│   ├── nodes/                     # Graph nodes
│   │   └── basic_chatbot_node.py # Basic chatbot node
│   └── states/                    # State definitions
│       └── chatbotState.py       # Chatbot state
└── README.md                      # This file
```

## 🛠️ Technologies Used

- **[Gradio](https://gradio.app/)** - Web UI framework
- **[LangGraph](https://python.langchain.com/docs/langgraph)** - Graph-based agent orchestration
- **[LangChain](https://python.langchain.com/)** - LLM framework
- **[Groq](https://groq.com/)** - Ultra-fast LLM inference
- **[Google Gemini](https://ai.google.dev/)** - Google's AI models
- **[OpenAI](https://openai.com/)** - GPT models
- **[Ollama](https://ollama.ai/)** - Local LLM runtime

## 🔧 Development

### Adding a New LLM Provider

1. Create a new file in `langgraph_agent/llms/` (e.g., `new_provider_llm.py`)
2. Implement the provider class with `get_base_llm()` method
3. Add model options to `MODEL_OPTIONS` in `app.py`
4. Update the `initialize_graph()` function to handle the new provider
5. Add the provider to the dropdown choices

### Modifying the Graph

The chatbot logic is defined in `langgraph_agent/graphs/basic_chatbot_graph.py`. You can:
- Add new nodes
- Modify conversation flow
- Add tools and function calling
- Implement RAG (Retrieval-Augmented Generation)

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built with [LangGraph](https://python.langchain.com/docs/langgraph)
- UI powered by [Gradio](https://gradio.app/)
- Multi-provider LLM support

## 🔗 Links

- **Hugging Face Space**: [View Demo](https://huggingface.co/spaces/sshibinthomass/Gradio-Chat)
- **GitHub Repository**: [Source Code](https://github.com/YOUR_USERNAME/Gradio-Chat)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ using LangGraph and Gradio
