from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

##Loading dotenv for retrieval of API keys
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
    llm=ChatGroq(groq_api_key=GROQ_API_KEY,
                 model_name='llama3-70b-8192'
                 )
    prompt=PromptTemplate(input_variables=["context","input"],
                          template="""You are a **BusinessAssistantBot**, an AI-powered assistant trained to help users understand business documents --contracts, tenders, reports and answer business related questions.

             Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.
             
              ---

            🔍 **Context**:
                {context}

            🙋‍♂️ **User Question**:
                {input}

            ---
            💬 **Answer**:
                - Respond in a calm, factual, and respectful tone.
                - Use simple explanations when needed.
                - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
                - Do NOT make up facts. """)

    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    return create_retrieval_chain(retriever, combine_docs_chain)




