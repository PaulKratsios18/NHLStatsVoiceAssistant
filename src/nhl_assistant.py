from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class NHLAssistant:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(temperature=0)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.qa_chain = self.create_qa_chain()
    
    def create_qa_chain(self):
        return ConversationalRetrievalChain.from_llm(
            self.llm,
            retriever=self.vector_store.vector_store.as_retriever(),
            memory=self.memory
        )
    
    def answer_question(self, question: str) -> str:
        response = self.qa_chain({"question": question})
        return response["answer"] 