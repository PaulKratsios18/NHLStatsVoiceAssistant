from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

class NHLVectorStore:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        
        # Initialize HuggingFace embeddings (free to use)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",  # Small, fast model good for semantic search
            cache_folder="./models"  # Cache the model locally
        )
        self.vector_store = None
        self.initialize_store()
    
    def initialize_store(self):
        try:
            # Convert NHL data to documents
            context = self.data_manager.create_context_string()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_text(context)
            documents = [Document(page_content=text) for text in texts]
            
            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents,
                self.embeddings,
                persist_directory="./data/vectorstore"
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize vector store: {str(e)}")