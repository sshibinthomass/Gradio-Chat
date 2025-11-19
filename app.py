import gradio as gr
import os
from pathlib import Path
import sys
from dotenv import load_dotenv

# Add project root to path
current_file = Path(__file__).resolve()
project_root = current_file.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from langgraph_agent.graphs.graph_builder import GraphBuilder
from langgraph_agent.llms.groq_llm import GroqLLM
from langgraph_agent.llms.gemini_llm import GeminiLLM
from langgraph_agent.llms.openai_llm import OpenAiLLM
from langgraph_agent.llms.ollama_llm import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Load environment variables
load_dotenv()

# Global variables to store graph and configuration
graph = None
current_llm_provider = None

# Model options for each provider
MODEL_OPTIONS = {
    "Groq": [
        ("OpenAI GPT OSS 20B", "openai/gpt-oss-20b"),
        ("Llama 3.1 8B Instant", "llama-3.1-8b-instant"),
        ("GPT OSS 120B", "openai/gpt-oss-120b"),
        ("Llama 3.3 70B Versatile", "llama-3.3-70b-versatile"),
    ],
    "OpenAI": [
        ("GPT-5 Nano", "gpt-5-nano"),
        ("GPT-4o Mini", "gpt-4o-mini"),
        ("GPT-5 Mini", "gpt-5-mini"),
    ],
    "Gemini": [
        ("Gemini 2.5 Flash", "gemini-2.5-flash"),
        ("Gemini 1.5 Flash", "gemini-1.5-flash"),
    ],
    "Ollama": [
        ("Gemma3 1B", "gemma3:1b"),
        ("GPT OSS 20B", "gpt-oss:20b"),
        ("DeepSeek R1 8B", "deepseek-r1:8b"),
        ("Llama 3.1 8B", "llama3.1:latest"),
    ],
}


def get_model_choices(provider):
    """Get model choices for the selected provider"""
    return gr.Dropdown(
        choices=MODEL_OPTIONS.get(provider, []),
        value=MODEL_OPTIONS.get(provider, [("", "")])[0][1] if MODEL_OPTIONS.get(provider) else "",
        label="Model",
        interactive=True
    )


def initialize_graph(llm_provider, model_name, groq_key="", gemini_key="", openai_key="", ollama_url=""):
    """Initialize the LangGraph chatbot with the selected LLM provider"""
    global graph, current_llm_provider
    
    try:
        user_controls_input = {}
        
        if llm_provider == "Groq":
            # Use UI input if provided, otherwise fall back to .env
            api_key = groq_key.strip() if groq_key.strip() else os.getenv("GROQ_API_KEY")
            if not api_key:
                return "❌ Error: GROQ_API_KEY is required. Please enter it above or set it in .env file."
            
            user_controls_input = {
                "GROQ_API_KEY": api_key,
                "selected_llm": model_name or "openai/gpt-oss-20b",
            }
            llm_instance = GroqLLM(user_controls_input)
        elif llm_provider == "Gemini":
            # Use UI input if provided, otherwise fall back to .env
            api_key = gemini_key.strip() if gemini_key.strip() else os.getenv("GEMINI_API_KEY")
            if not api_key:
                return "❌ Error: GEMINI_API_KEY is required. Please enter it above or set it in .env file."
            
            user_controls_input = {
                "GEMINI_API_KEY": api_key,
                "selected_llm": model_name or "gemini-2.5-flash",
            }
            llm_instance = GeminiLLM(user_controls_input)
        elif llm_provider == "OpenAI":
            # Use UI input if provided, otherwise fall back to .env
            api_key = openai_key.strip() if openai_key.strip() else os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "❌ Error: OPENAI_API_KEY is required. Please enter it above or set it in .env file."
            
            user_controls_input = {
                "OPENAI_API_KEY": api_key,
                "selected_llm": model_name or "gpt-4o-mini",
            }
            llm_instance = OpenAiLLM(user_controls_input)
        elif llm_provider == "Ollama":
            # Use UI input if provided, otherwise fall back to .env
            base_url = ollama_url.strip() if ollama_url.strip() else os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            
            user_controls_input = {
                "selected_llm": model_name or "gemma3:1b",
                "OLLAMA_BASE_URL": base_url,
            }
            llm_instance = OllamaLLM(user_controls_input)
        else:
            return f"❌ Unknown LLM provider: {llm_provider}"
        
        llm = llm_instance.get_base_llm()
        graph_builder = GraphBuilder(llm, user_controls_input)
        graph = graph_builder.setup_graph("basic_chatbot")
        current_llm_provider = llm_provider
        
        return f"✅ Successfully initialized {llm_provider} with model: {user_controls_input['selected_llm']}"
    
    except Exception as e:
        return f"❌ Error initializing graph: {str(e)}"


def respond(message, history, llm_provider, model_name, groq_key="", gemini_key="", openai_key="", ollama_url=""):
    """Generate chatbot response using LangGraph"""
    global graph, current_llm_provider
    
    # Initialize or reinitialize graph if needed
    if graph is None or current_llm_provider != llm_provider:
        init_msg = initialize_graph(llm_provider, model_name, groq_key, gemini_key, openai_key, ollama_url)
        if "❌" in init_msg:
            return init_msg
    
    try:
        # Convert Gradio history to LangChain messages
        messages = [SystemMessage(content="You are a helpful and friendly assistant.")]
        
        # Handle new Gradio messages format (list of dicts)
        for msg in history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        # Create input state for the graph
        initial_state = {"messages": messages}
        
        # Run the graph and get the response
        result = graph.invoke(initial_state)
        
        # Extract the AI response from the result
        ai_response = result["messages"][-1].content
        
        return ai_response
    
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"


# Create the Gradio interface
with gr.Blocks(title="LangGraph Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 LangGraph Chatbot")
    gr.Markdown("### Powered by LangGraph and Multiple LLM Providers")
    
    # Left Sidebar - Configuration
    with gr.Sidebar(label="Configuration", open=True):
        gr.Markdown("### ⚙️ Settings")
        
        llm_provider = gr.Dropdown(
            choices=["Groq", "Gemini", "OpenAI", "Ollama"],
            value="Groq",
            label="LLM Provider",
        )
        
        model_dropdown = gr.Dropdown(
            choices=MODEL_OPTIONS["Groq"],
            value="openai/gpt-oss-20b",
            label="Model",
            interactive=True
        )
        
        # API Keys Configuration (collapsible)
        with gr.Accordion("🔑 API Keys (Optional)", open=False):
            gr.Markdown("""
                **Note:** Enter API keys here if deploying to Hugging Face or if not set in `.env`.
            """)
            
            groq_api_key = gr.Textbox(
                label="Groq API Key",
                placeholder="Enter your Groq API key",
                type="password"
            )
            
            gemini_api_key = gr.Textbox(
                label="Gemini API Key",
                placeholder="Enter your Gemini API key",
                type="password"
            )
            
            openai_api_key = gr.Textbox(
                label="OpenAI API Key",
                placeholder="Enter your OpenAI API key",
                type="password"
            )
            
            ollama_base_url = gr.Textbox(
                label="Ollama Base URL",
                placeholder="http://localhost:11434"
            )
        
        status_msg = gr.Textbox(
            label="📊 Status", 
            interactive=False, 
            value="Select LLM provider and model, then start chatting!",
            lines=2
        )
        
        clear_btn = gr.Button("🧹 Clear Chat", variant="secondary", size="lg")
    
    # Main Chat Interface (Right Side)
    gr.Markdown("### 💬 Conversation")
    
    chatbot = gr.Chatbot(
        label="", 
        height=600, 
        show_copy_button=True,
        show_label=False,
        type="messages"
    )

    with gr.Row():
        msg = gr.Textbox(
            label="",
            placeholder="Type your message here and press Enter...",
            scale=4,
            container=False,
            show_label=False
        )
        submit_btn = gr.Button("📤 Send", variant="primary", scale=1)

    def user_message(user_msg, history):
        """Add user message to history"""
        return "", history + [{"role": "user", "content": user_msg}]

    def bot_message(history, llm_prov, model, groq_key, gemini_key, openai_key, ollama_url):
        """Generate bot response and update history"""
        # Get the last user message
        user_msg = history[-1]["content"]
        
        # Get response (pass history excluding the last message)
        bot_msg = respond(user_msg, history[:-1], llm_prov, model, groq_key, gemini_key, openai_key, ollama_url)
        
        # Append bot response to history
        history.append({"role": "assistant", "content": bot_msg})
        return history

    def update_status(llm_prov, model, groq_key, gemini_key, openai_key, ollama_url):
        """Update status when LLM provider changes"""
        return initialize_graph(llm_prov, model, groq_key, gemini_key, openai_key, ollama_url)
    
    def update_model_dropdown(provider):
        """Update model dropdown when provider changes"""
        choices = MODEL_OPTIONS.get(provider, [])
        default_value = choices[0][1] if choices else ""
        return gr.Dropdown(choices=choices, value=default_value, label="Model", interactive=True)

    # Handle LLM provider change - update both model dropdown and status
    llm_provider.change(
        update_model_dropdown, 
        [llm_provider], 
        model_dropdown
    ).then(
        update_status, 
        [llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url], 
        status_msg
    )
    
    # Handle model change - update status
    model_dropdown.change(
        update_status, 
        [llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url], 
        status_msg
    )
    
    # Handle API key changes - re-initialize graph
    groq_api_key.change(
        update_status,
        [llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url],
        status_msg
    )
    
    gemini_api_key.change(
        update_status,
        [llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url],
        status_msg
    )
    
    openai_api_key.change(
        update_status,
        [llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url],
        status_msg
    )
    
    ollama_base_url.change(
        update_status,
        [llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url],
        status_msg
    )

    # Handle message submission
    msg.submit(user_message, [msg, chatbot], [msg, chatbot]).then(
        bot_message, [chatbot, llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url], chatbot
    )
    submit_btn.click(user_message, [msg, chatbot], [msg, chatbot]).then(
        bot_message, [chatbot, llm_provider, model_dropdown, groq_api_key, gemini_api_key, openai_api_key, ollama_base_url], chatbot
    )

    # Clear chat history
    clear_btn.click(lambda: None, None, chatbot, queue=False)


if __name__ == "__main__":
    demo.launch(share=False)
