import os

from dotenv import load_dotenv
from openai import OpenAI

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings


load_dotenv()


# --------------------------------------------------
# 1. OpenRouter client
# --------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)


# --------------------------------------------------
# 2. Same embedding class used in build_index.py
# --------------------------------------------------

class LiquidEmbeddings(Embeddings):

    def _embed(self, text):

        response = client.embeddings.create(
            model=os.getenv("EMBEDDING_MODEL"),
            input=text,
            encoding_format="float"
        )

        return response.data[0].embedding

    def embed_documents(self, texts):

        return [self._embed(text) for text in texts]

    def embed_query(self, text):

        return self._embed(text)


# --------------------------------------------------
# 3. Load existing Chroma database
# --------------------------------------------------

embeddings = LiquidEmbeddings()

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


# --------------------------------------------------
# 4. Create retriever
# --------------------------------------------------

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)


# --------------------------------------------------
# 5. Refusal message
# --------------------------------------------------

REFUSAL = (
    "I don't have that information in my knowledge base "
    "— let me connect you to a human agent."
)


# --------------------------------------------------
# 6. Ask function
# --------------------------------------------------

def ask(question):

    # Retrieve relevant chunks
    documents = retriever.invoke(question)

    print("\nRetrieved sources:")

    for i, doc in enumerate(documents, start=1):

        source = os.path.basename(
            doc.metadata.get("source", "unknown")
        )

        print(f"{i}. {source}")

    # Build context
    context_parts = []

    for doc in documents:

        source = os.path.basename(
            doc.metadata.get("source", "unknown")
        )

        context_parts.append(
            f"SOURCE: {source}\n"
            f"CONTENT:\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt = f"""
You are a banking support assistant.

Answer the user's question ONLY using the provided context.

Rules:

1. Do not use outside knowledge.
2. Do not invent or guess information.
3. Every factual statement must cite its source filename
   in square brackets.
4. If the context does not contain the answer, reply EXACTLY:

I don't have that information in my knowledge base — let me connect you to a human agent.

Context:

{context}

User question:

{question}
"""

    # --------------------------------------------------
    # Generate answer
    # --------------------------------------------------

    response = client.chat.completions.create(
        model=os.getenv("CHAT_MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    print("\nAnswer:")
    print(answer)


# --------------------------------------------------
# 7. Interactive loop
# --------------------------------------------------

if __name__ == "__main__":

    while True:

        question = input("\nYou: ")

        if question.lower() in {"exit", "quit"}:
            break

        ask(question)