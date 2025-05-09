import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage
from dotenv import load_dotenv


# ✅ Load Environment Variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Set Data Directory
APP_DATA_DIR = "APP_DATA"

def load_documents(directory):
    """Load all JSON, SAS, and text files into vector store."""
    docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith((".json", ".sas", ".txt")):
                with open(file_path, "r", encoding="utf-8") as f:
                    docs.append(f.read())
    return docs

# ✅ Load and Process Documents
documents = load_documents(APP_DATA_DIR)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
flat_chunks = [chunk for doc in documents for chunk in text_splitter.split_text(doc)]

# ✅ Create Vector Store for AI
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
vector_store = FAISS.from_texts(flat_chunks, embedding=embeddings)

# ✅ Set Up Retriever & Memory
retriever = vector_store.as_retriever()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ Initialize GPT-4o Model
gpt4o = ChatOpenAI(model_name="gpt-4o", temperature=0.2)

