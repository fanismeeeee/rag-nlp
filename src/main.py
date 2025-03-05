import os
from agents.local_rag_agent import LocalRAGAgent

def main():
    # Initialize the Local RAG agent
    agent = LocalRAGAgent()
    
    print("Local RAG Agent initialized. Type 'quit' to exit.")
    print("Type 'reload' to reload documents.")
    
    while True:
        question = input("\nYour question: ")
        
        if question.lower() == 'quit':
            break
        elif question.lower() == 'reload':
            agent.ingest_documents()
            print("Documents reloaded!")
            continue
        
        try:
            answer = agent.query(question)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()