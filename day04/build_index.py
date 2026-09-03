import time
import os
from dotenv import load_dotenv
from openai import OpenAI
 
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
 
load_dotenv()
 
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)
 
 
 
 
 
class LiquidEmbeddings(Embeddings):
 
    def _embed(self, text):
        max_retries = 5
 
        for attempt in range(max_retries):
            try:
                response = client.embeddings.create(
                    model=os.getenv("EMBEDDING_MODEL"),
                    input=text,
                    encoding_format="float"
                )
 
                return response.data[0].embedding
 
            except Exception as e:
                if "429" in str(e):
                    wait_time = 10 * (attempt + 1)
 
                    print(
                        f"Rate limited (429). "
                        f"Waiting {wait_time} seconds..."
                    )
 
                    time.sleep(wait_time)
                else:
                    raise
 
        raise RuntimeError(
            "Rate limit persisted after multiple retries."
        )
 
    def embed_documents(self, texts):
        embeddings = []
 
        total = len(texts)
 
        for i, text in enumerate(texts, start=1):
            print(f"Embedding chunk {i}/{total}...")
 
            embedding = self._embed(text)
            embeddings.append(embedding)
 
            # Give the free model some breathing room
            time.sleep(3)
 
        return embeddings
 
    def embed_query(self, text):
        return self._embed(text)
 
# 1. Load documents
docs = DirectoryLoader(
    "day04/kb",
    glob="*.txt",
    loader_cls=TextLoader
).load()
 
print(f"Loaded {len(docs)} documents.")
 
 
# 2. Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
 
chunks = splitter.split_documents(docs)
 
print(f"Created {len(chunks)} chunks.")
 
 
# 3. Create embeddings
embeddings = LiquidEmbeddings();
 
 
# 4. Create Chroma database
db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="chroma_db"
)
 
print(f"Indexed {len(chunks)} chunks from {len(docs)} documents.")