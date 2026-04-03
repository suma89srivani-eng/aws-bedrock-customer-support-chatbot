from bedrock import get_bedrock_response
from openai_api import get_openai_response
from groq_api import get_groq_response

chat_history = []

def choose_model(user_input):
    """
    Simple routing logic for tool/model selection.
    You can improve this later.
    """
    if "refund" in user_input.lower() or "order" in user_input.lower():
        return "bedrock"
    elif "technical" in user_input.lower() or "error" in user_input.lower():
        return "groq"
    else:
        return "openai"

def main():
    print("🤖 AI Customer Support Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Thank you for contacting support. Goodbye!")
            break

        model_choice = choose_model(user_input)

        if model_choice == "bedrock":
            response = get_bedrock_response(user_input, chat_history)
        elif model_choice == "groq":
            response = get_groq_response(user_input)
        else:
            response = get_openai_response(user_input)

        print(f"Bot ({model_choice}): {response}\n")

        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
