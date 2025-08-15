from langchain_openai import OpenAIEmbeddings
from langchain.evaluation import load_evaluator
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

def main():
    embedding_function = OpenAIEmbeddings()
    vector = embedding_function.embed_query("apple")
    print(f"Vector for 'apple': {vector}")
    print(f"Vector length: {len(vector)}")
    
    evaluator = load_evaluator("pairwise_embedding_distance")
    w1, w2 = "apple", "iphone"
    result = evaluator.evaluate_string_pairs(prediction=w1, prediction_b=w2)
    print(f"Comparing ({w1}, {w2}): {result}")

if __name__ == "__main__":
    main()
