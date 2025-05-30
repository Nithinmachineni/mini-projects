import nltk
import spacy

# Load English tokenizer, POS tagger, etc.
nlp = spacy.load("en_core_web_sm")

# Responses database (simple rule-based)hi
responses = {
    
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there!",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "what is your name": "I'm ChatBot, your virtual assistant!",
    "what can you do": "I can chat with you and answer simple questions!",
    "bye": "bye! Have a nice day!",
    "tell me a joke": "Why did the computer go to therapy? Because it had too many bugs!",
    "who created you": "I was created by a Python developer who loves AI!",
    "what is python": "Python is a powerful, easy-to-learn programming language used for many things including web development and AI!",
    "thank you": "You're welcome! 😊",
    "what time is it": "I can't tell time yet, but I’ll learn soon!",
    "where are you from": "I live in the world of code!",
    
    # New time-based greetings
    "good morning": "Good morning!",
    "good afternoon": "Good afternoon!",
    "good evening": "Good evening !",
}
    # Function to preprocess and match intent
def get_response(user_input):
    user_input = user_input.lower()
    doc = nlp(user_input)

    for key in responses:
        if key in user_input:
            return responses[key]
    
    return "I'm sorry, I didn't understand that. Can you try asking something else?"

# Chat loop
print("🤖 ChatBot: Welcome to the AI Chatbot!")
print("🤖 ChatBot: Hello! Type 'bye' to exit.")
while True:
    user_input = input("🧑 You: ")
    if "bye" in user_input.lower():
        print("🤖 ChatBot:", responses["bye"])
        break
    response = get_response(user_input)
    print("🤖 ChatBot:", response)
