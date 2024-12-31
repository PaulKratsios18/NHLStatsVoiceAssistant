import os
from dotenv import load_dotenv
from src.data_manager import NHLDataManager
from src.vector_store import NHLVectorStore
from src.nhl_assistant import NHLAssistant
from src.speech import speak, get_audio

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    data_manager = NHLDataManager("data")
    vector_store = NHLVectorStore(data_manager)
    assistant = NHLAssistant(vector_store)
    
    print("NHL Assistant initialized! Ask me anything about NHL statistics.")
    
    while True:
        text = get_audio()
        print(f"You said: {text}")
        
        if text == "stop":
            speak("Goodbye!")
            break
            
        if text:
            response = assistant.answer_question(text)
            speak(response)
            print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
