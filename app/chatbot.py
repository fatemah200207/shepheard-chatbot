import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

from app.retrieval import retrieve_relevant_documents


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ============================================================
# SYSTEM INSTRUCTIONS
# ============================================================

SYSTEM_PROMPT = """
You are the Shepheard Hotel Annex Project Assistant.

Your job is to answer questions ONLY using the provided Shepheard Hotel Annex
project documents.

The provided documents include:

- The Shepheard Hotel Annex Graduation Project Book
- Contract SH-06A
- Contract SH-06B and SH-06C

STRICT RULES:

1. Only answer questions related to the Shepheard Hotel Annex project or
   information contained in the provided project documents.

2. Use the retrieved project documents as the primary and authoritative
   source for project-specific information.

3. Do NOT answer unrelated general-knowledge questions.

   For example, questions about:
   - countries
   - populations
   - celebrities
   - sports
   - entertainment
   - weather
   - unrelated subjects

   must be refused.

4. Do NOT use your general knowledge to provide information that is not
   supported by the retrieved project documents.

5. If the user asks a question that is unrelated to the Shepheard Hotel
   Annex project, respond:

   "I can only answer questions related to the Shepheard Hotel Annex
   project and the documents provided."

6. If the question is related to the Shepheard project but the retrieved
   documents do not contain enough information to answer it, say:

   "The information is not available in the provided project documents."

7. Do not invent, assume, or guess project-specific facts.

8. Clearly distinguish between:

   - Graduation Project Book information
   - Contract information

9. If the user asks about a technical or project-management concept, only
   explain it if it is relevant to the Shepheard Hotel Annex project or is
   discussed in the provided documents.

10. Stay focused on the Shepheard Hotel Annex project at all times.

11. Do not provide source citations, page references, or document references
    in the answer unless the user specifically asks for them.
"""


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question):

    # --------------------------------------------------------
    # STEP 1: Retrieve relevant project information
    # --------------------------------------------------------

    results = retrieve_relevant_documents(
        question,
        n_results=5
    )

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


    # --------------------------------------------------------
    # STEP 2: Build the prompt
    # --------------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

Retrieved project information:
{context}

User question:
{question}

Answer the question using ONLY the retrieved project information.
"""


    # --------------------------------------------------------
    # STEP 3: Ask Gemini
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text


    # --------------------------------------------------------
    # STEP 4: Handle Gemini quota errors
    # --------------------------------------------------------

    except ClientError as error:

        # Gemini returns HTTP 429 when the request/quota limit
        # has been exceeded.
        if getattr(error, "code", None) == 429:

            return (
                "The AI service has temporarily reached its request "
                "limit. Please try again later."
            )

        # Handle RESOURCE_EXHAUSTED even if the SDK exposes
        # the error slightly differently.
        if "RESOURCE_EXHAUSTED" in str(error):

            return (
                "The AI service has temporarily reached its request "
                "limit. Please try again later."
            )

        # Other Gemini errors should still be visible in the
        # Render logs rather than being silently hidden.
        raise


    # --------------------------------------------------------
    # STEP 5: Safety fallback
    # --------------------------------------------------------

    except Exception as error:

        print(f"Unexpected chatbot error: {error}")

        return (
            "The project assistant is temporarily unavailable. "
            "Please try again later."
        )