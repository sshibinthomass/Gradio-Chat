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


def initialize_graph(llm_provider, model_name):
    """Initialize the LangGraph chatbot with the selected LLM provider"""
    global graph, current_llm_provider
    
    try:
        user_controls_input = {}
        
        if llm_provider == "Groq":
            user_controls_input = {
                "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
                "selected_llm": model_name or "openai/gpt-oss-20b",
            }
            llm_instance = GroqLLM(user_controls_input)
        elif llm_provider == "Gemini":
            user_controls_input = {
                "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
                "selected_llm": model_name or "gemini-2.5-flash",
            }
            llm_instance = GeminiLLM(user_controls_input)
        elif llm_provider == "OpenAI":
            user_controls_input = {
                "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
                "selected_llm": model_name or "gpt-4o-mini",
            }
            llm_instance = OpenAiLLM(user_controls_input)
        elif llm_provider == "Ollama":
            user_controls_input = {
                "selected_llm": model_name or "gemma3:1b",
                "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
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


def respond(message, history, llm_provider, model_name):
    """Generate chatbot response using LangGraph"""
    global graph, current_llm_provider
    
    # Initialize or reinitialize graph if needed
    if graph is None or current_llm_provider != llm_provider:
        init_msg = initialize_graph(llm_provider, model_name)
        if "❌" in init_msg:
            return init_msg
    
    try:
        # Convert Gradio history to LangChain messages
        messages = [SystemMessage(content="You are a helpful and friendly assistant.")]
        
        for user_msg, bot_msg in history:
            if user_msg:
                messages.append(HumanMessage(content=user_msg))
            if bot_msg:
                messages.append(AIMessage(content=bot_msg))
        
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
    
    with gr.Row():
        llm_provider = gr.Dropdown(
            choices=["Groq", "Gemini", "OpenAI", "Ollama"],
            value="Groq",
            label="LLM Provider",
            scale=1
        )
        model_dropdown = gr.Dropdown(
            choices=MODEL_OPTIONS["Groq"],
            value="openai/gpt-oss-20b",
            label="Model",
            scale=2,
            interactive=True
        )
    
    status_msg = gr.Textbox(label="Status", interactive=False, value="Select LLM provider and model, then start chatting!")
    
    chatbot = gr.Chatbot(label="Conversation", height=400, show_copy_button=True)

    with gr.Row():
        msg = gr.Textbox(
            label="Your Message",
            placeholder="Type your message here and press Enter...",
            scale=4,
            container=False,
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)

    clear_btn = gr.Button("Clear Chat", variant="secondary")

    def user_message(user_msg, history):
        """Add user message to history"""
        return "", history + [[user_msg, None]]

    def bot_message(history, llm_prov, model):
        """Generate bot response and update history"""
        user_msg = history[-1][0]
        bot_msg = respond(user_msg, history[:-1], llm_prov, model)
        history[-1][1] = bot_msg
        return history

    def update_status(llm_prov, model):
        """Update status when LLM provider changes"""
        return initialize_graph(llm_prov, model)
    
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
        [llm_provider, model_dropdown], 
        status_msg
    )
    
    # Handle model change - update status
    model_dropdown.change(update_status, [llm_provider, model_dropdown], status_msg)

    # Handle message submission
    msg.submit(user_message, [msg, chatbot], [msg, chatbot]).then(
        bot_message, [chatbot, llm_provider, model_dropdown], chatbot
    )
    submit_btn.click(user_message, [msg, chatbot], [msg, chatbot]).then(
        bot_message, [chatbot, llm_provider, model_dropdown], chatbot
    )

    # Clear chat history
    clear_btn.click(lambda: None, None, chatbot, queue=False)


if __name__ == "__main__":
    demo.launch(share=False)
