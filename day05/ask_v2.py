import os
import json

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
# 6. Generate three query variations
# --------------------------------------------------

def generate_queries(question):

    prompt = f"""
You are helping a banking support system improve document retrieval.

Generate exactly three differently-worded versions of the user's question.

The three versions should:
- Ask for the same information.
- Use different wording.
- Preserve the original meaning.
- Be useful for semantic document retrieval.

Return ONLY valid JSON in this exact format:

{{
    "queries": [
        "query 1",
        "query 2",
        "query 3"
    ]
}}

User question:
{question}
"""

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

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        queries = data["queries"]

        if not isinstance(queries, list) or len(queries) != 3:
            raise ValueError("Expected exactly 3 queries")

        return queries

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):

        print("\nCould not parse generated queries.")
        print("Raw response:")
        print(content)

        return [question]


# --------------------------------------------------
# 7. Ask function
# --------------------------------------------------

def ask(question):

    # --------------------------------------------------
    # Generate three query variations
    # --------------------------------------------------

    queries = generate_queries(question)

    print("\nGenerated queries:")

    for i, query in enumerate(queries, start=1):
        print(f"{i}. {query}")


    # --------------------------------------------------
    # Retrieve documents for every query
    # --------------------------------------------------

    all_documents = []

    for query in queries:

        documents = retriever.invoke(query)

        all_documents.extend(documents)


    # --------------------------------------------------
    # De-duplicate chunks by content
    # --------------------------------------------------

    unique_documents = []
    seen_contents = set()

    for doc in all_documents:

        content = doc.page_content

        if content not in seen_contents:

            seen_contents.add(content)
            unique_documents.append(doc)


    # --------------------------------------------------
    # Print retrieved sources
    # --------------------------------------------------

    print("\nRetrieved sources:")

    for i, doc in enumerate(unique_documents, start=1):

        source = os.path.basename(
            doc.metadata.get("source", "unknown")
        )

        print(f"{i}. {source}")


    # --------------------------------------------------
    # Build context
    # --------------------------------------------------

    context_parts = []

    for doc in unique_documents:

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


    # --------------------------------------------------
    # Print answer
    # --------------------------------------------------

    print("\nAnswer:")
    print(answer)


# --------------------------------------------------
# 8. Interactive loop
# --------------------------------------------------

if __name__ == "__main__":

    while True:

        question = input("\nYou: ")

        if question.lower() in {"exit", "quit"}:
            break

        ask(question)