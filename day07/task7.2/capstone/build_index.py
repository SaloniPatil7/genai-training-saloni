from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv
import requests
import os


load_dotenv()

# Liquid Embedding Class

class LiquidEmbeddings:

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/embeddings"
        self.model = "liquid/lfm-2.5-embedding-350m:free"

    def _embed(self, texts):

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "input": texts
            }
        )

        response.raise_for_status()

        data = response.json()

        return [item["embedding"] for item in data["data"]]

    def embed_documents(self, texts):
        return self._embed(texts)

    def embed_query(self, text):
        return self._embed([text])[0]


# Load documents

docs = DirectoryLoader(
    "day04/task4.1/kb",
    glob="*.txt",
    loader_cls=TextLoader
).load()

print(f"Loaded {len(docs)} documents.")


# Split documents

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

print(f"Created {len(chunks)} chunks.")


# Create embeddings

embeddings = LiquidEmbeddings()


# Store in Chroma

db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="day04/chroma_db"
)


print(
    f"Indexed {len(chunks)} chunks from {len(docs)} documents."
)