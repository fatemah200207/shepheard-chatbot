import os

from dotenv import load_dotenv
from google import genai

from app.retrieval import retrieve_relevant_documents


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


SYSTEM_PROMPT = """
You are the Shepheard Hotel Annex Project Assistant.

Your job is to answer questions ONLY using the provided Shepheard Hotel Annex project documents.

The provided documents include:
- The Shepheard Hotel Annex Graduation Project Book
- Contract SH-06A
- Contract SH-06B and SH-06C

STRICT RULES:

1. Only answer questions related to the Shepheard Hotel Annex project or information contained in the provided project documents.

2. Use the retrieved project documents as the primary and authoritative source for project-specific information.

3. Do NOT answer unrelated general-knowledge questions.
   For example, questions about countries, populations, celebrities, sports, entertainment, weather, or unrelated subjects must be refused.

4. Do NOT use your general knowledge to provide information that is not supported by the retrieved project documents.

5. If the user asks a question that is unrelated to the Shepheard Hotel Annex project, respond:
   "I can only answer questions related to the Shepheard Hotel Annex project and the documents provided."

6. If the question is related to the Shepheard project but the retrieved documents do not contain enough information to answer it, say:
   "The information is not available in the provided project documents."

7. Do not invent, assume, or guess project-specific facts.

8. Clearly distinguish between:
   - Graduation Project Book information
   - Contract information

9. When possible, mention the document name and page number used for the answer.

10. If the user asks about a technical or project-management concept, only explain it if it is relevant to the Shepheard Hotel Annex project or is discussed in the provided documents.

11. Stay focused on the Shepheard Hotel Annex project at all times.
"""


def generate_answer(question):
    results = retrieve_relevant_documents(question, n_results=5)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(documents, metadatas):
        context_parts.append(
            f"""
Document: {metadata['document_name']}
Document type: {metadata['document_type']}
Page: {metadata['page']}

Content:
{document}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
{SYSTEM_PROMPT}

Retrieved project information:
{context}

User question:
{question}

Answer the question using the retrieved information.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text