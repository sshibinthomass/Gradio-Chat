import gradio as gr


def respond(message, history):
    """Simple chatbot response function"""
    # Simple echo-based responses with some variations
    if not message.strip():
        return "Please enter a message!"

    # Simple rule-based responses
    message_lower = message.lower()

    if "hello" in message_lower or "hi" in message_lower:
        return "Hello! How can I help you today?"
    elif "how are you" in message_lower:
        return "I'm doing well, thank you for asking! How are you?"
    elif "bye" in message_lower or "goodbye" in message_lower:
        return "Goodbye! It was nice chatting with you!"
    elif "help" in message_lower:
        return "I'm a simple chatbot. Try asking me questions or just chat with me!"
    elif "?" in message:
        return f"That's an interesting question about '{message}'. I'm a simple chatbot, so I might not have all the answers, but I'm here to chat!"
    else:
        return f"You said: '{message}'. That's interesting! Tell me more."


# Create the Gradio interface
with gr.Blocks(title="Simple Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 💬 Simple Chatbot")
    gr.Markdown("### A simple conversational chatbot built with Gradio")

    chatbot = gr.Chatbot(label="Conversation", height=500, show_copy_button=True)

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

    def bot_message(history):
        """Generate bot response and update history"""
        user_msg = history[-1][0]
        bot_msg = respond(user_msg, history)
        history[-1][1] = bot_msg
        return history

    # Handle message submission
    msg.submit(user_message, [msg, chatbot], [msg, chatbot]).then(
        bot_message, chatbot, chatbot
    )
    submit_btn.click(user_message, [msg, chatbot], [msg, chatbot]).then(
        bot_message, chatbot, chatbot
    )

    # Clear chat history
    clear_btn.click(lambda: None, None, chatbot, queue=False)


if __name__ == "__main__":
    demo.launch(share=False)
