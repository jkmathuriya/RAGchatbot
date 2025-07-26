from logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input", user_input)
        res = chain.invoke({"input": user_input})
        response = {
            "response": res["answer"],
            "sources": [doc.metadata.get("source", "") for doc in res["context"]],
            "page_number": [f"Page No.: {doc.metadata.get('page', '')}" for doc in res["context"]],
            "res": res

        }
        return response
    except Exception as e:
        logger.exception("Error on query chain")
        raise

