import argparse
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()

    query = args.query_text
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    results = db.similarity_search_with_relevance_scores(query, k=3)
    if not results or results[0][1] < 0.7:
        print("Unable to find matching results.")
        return

    context = "\n\n---\n\n".join(doc.page_content for doc, _ in results)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context, question=query
    )

    model = ChatOpenAI()
    answer = model.predict(prompt)
    sources = [doc.metadata.get("source") for doc, _ in results]

    print(f"Response: {answer}\nSources: {sources}")

if __name__ == "__main__":
    main()
