from chroma_config import ChromaConfig
from fastapi import Depends
from ollama import chat
from ollama import ChatResponse
import json

# @lru_cache()
def get_retriever():
    return Retriver()

class Retriver:
    def __init__(self):
        self.db_config = ChromaConfig()

    def query_by_product_description(self, query_text: str, n_results: int = 5):
        """Query specifically by product description."""
        print(f"Querying for {query_text}...")
        return self.db_config.query_documents(query_text, 'product_description', n_results)

    def query_by_business_context(self, query_text: str, n_results: int = 5):
        """Query specifically by business context (incident type + reason)."""
        print(f"Querying for {query_text}...")
        return self.db_config.query_documents(query_text, 'business_context', n_results)

    def query_by_all(self, query_text: str, n_results: int = 5):
        """Query specifically by business context (incident type + reason)."""
        print(f"Querying for all...")
        return self.db_config.query_documents(query_text, 'all', n_results)

    def recommend_solution(self, product_description: str, reason: str, reason_type: str):
        business_context = f"{reason}:{reason_type}"
        db_response = self.query_by_business_context(business_context, n_results=3)
        print(f"=====> response from db: {db_response}")
        response: ChatResponse = chat(
            model='gemma3',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant who recommends solutions.',
                },
                {
                    'role': 'assistant',
                    'content': f"Based on the response from the db : {db_response}. "
                               f"Consider the similarity_score of the solution for relevance. "
                               f"Lower the score more the relevance. "
                               f"Make sure response is in json format with field solution and reason."
                               f"Field solution should have only the solution name which is recommended."
                               f"Field reason should have only the reason for which this solution is recommended."
                },
                # {
                #     'role': 'user',
                #     'content': f"The customer is having issue with following product: {product_description} for the following reason is {reason}:{reason_type}.Please provide a solution recommendation based on the product description and reason provided.",
                # },
            ]
        )
        model_response = self.extract_json_from_string(response['message']['content'])
        print(f"response from model: {model_response}")
        return model_response

    def extract_json_from_string(self, s: str):
        try:
            # Find the first '{' and the last '}'
            start = s.find('{')
            end = s.rfind('}') + 1
            json_str = s[start:end]
            return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            return None

    def print_results(result):
        print(result)
        print("\n" + "="*50)
        for i in range(len(result['metadatas'][0])):
            print(f"Result: {i+1}")
            print(f"Product Description: {result['metadatas'][0][i]['productDescription']}")
            print(f"Business Incident Context: {result['metadatas'][0][i]['businessIncidentContext']}")
            print(f"Solution Type: {result['metadatas'][0][i]['solutionType']}")
            print(f"Partner ID: {result['metadatas'][0][i]['partner_id']}")
            print(f"Similarity Score: {result['distances'][0][i]}\n")

if __name__ == "__main__":
    retriver = Retriver()
    # Example queries to test the embeddings
    print("\n" + "="*80)
    print("TESTING EMBEDDINGS WITH FIELD-SPECIFIC QUERIES")
    print("="*80)

    # Test product description queries
    print("\n" + "="*50)
    print("PRODUCT DESCRIPTION QUERIES")
    print("="*50)
    product_queries = ["LG OLED TV", "Bose headphones", "Dyson vacuum"]
    for query in product_queries:
        result = retriver.query_by_product_description(query, n_results=2)
        retriver.print_results(result)
        print("\n")

    # Test business context queries
    print("\n" + "="*50)
    print("BUSINESS CONTEXT QUERIES")
    print("="*50)
    business_context_queries = ["PRODUCT_DEFECT: SCREEN_DEAD_PIXELS", "DELIVERY_ISSUE: LATE_DELIVERY", "FAULTY_PRODUCT: BATTERY_NOT_CHARGING"]
    for query in business_context_queries:
        result = retriver.query_by_business_context(query, n_results=2)
        retriver.print_results(result)
        print("\n")

    # Test partial business context queries
    print("\n" + "="*50)
    print("PARTIAL BUSINESS CONTEXT QUERIES")
    print("="*50)
    partial_context_queries = ["PRODUCT_DEFECT", "LATE_DELIVERY", "BATTERY_NOT_CHARGING"]
    for query in partial_context_queries:
        result = retriver.query_by_business_context(query, n_results=2)
        retriver.print_results(result)
        print("\n")

    # Test combined queries (all fields)
    print("\n" + "="*50)
    print("COMBINED QUERIES (ALL FIELDS)")
    print("="*50)
    combined_queries = ["TV screen issues", "audio problems", "battery issues"]
    for query in combined_queries:
        result = retriver.query_by_all(n_results=3)
        retriver.print_results(result)
        print("\n")