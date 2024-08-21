# import chainlit as cl
# import requests
# import os
# import openai
# from dotenv import load_dotenv
# load_dotenv()
# openai.api_key=os.getenv("openai_api_key")

# @cl.on_message
# async def on_message(message: str):
#     # Generate a query vector using the LLM
#     query_vector = generate_vector_using_llm(message)  # Using the LLM for embedding
#     response = requests.post("http://localhost:9000/query/", json={"query_vector": query_vector, "top_k": 5})
#     results = response.json()
    
#     # Interpret the vector database response using the LLM
#     interpreted_results = interpret_results_with_llm(results)  # Custom interpretation function
#     print("this is data: \n",interpreted_results)
    
#     #await cl.Message(content=interpreted_results).send()
#     await cl.Message(content=str(interpreted_results)).send()


# def generate_vector_using_llm(text):
#     # Generate embeddings using an LLM
#     response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
#     print(response)
#     vector = response['data'][0]['embedding']
#     return vector

# def interpret_results_with_llm(results):
#     indices = results['indices'][0]
#     distances = results['distances'][0]
    
#     response_text = f"Query results:\nIndices: {indices}\nDistances: {distances}"
    
#     interpretation = openai.Completion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": response_text}]
#     )
    
#     return interpretation.choices[0].message['content']


import chainlit as cl
import requests
import os
import openai
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError


load_dotenv()
openai.api_key = os.getenv("openai_api_key")

@cl.on_message
async def main(message: cl.Message):
    # # Generate a query vector using the LLM
    # query_vector = generate_vector_using_llm(message.content)
    # response = requests.post("http://localhost:9000/query/", json={"query_vector": query_vector, "top_k": 5})
    # print(response)
    # results = response.json()

    # # Interpret the vector database response using the LLM
    # interpreted_results = interpret_results_with_llm(results)
    # print("this is data: \n", interpreted_results)

    # # await cl.Message(content=interpreted_results).send()

    try:
        # Generate a query vector using the LLM
        query_vector = generate_vector_using_llm(message.content)
        response = requests.post("http://localhost:7000/query/", json={"query_vector": query_vector, "top_k": 5})
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        results = response.json()

        # Interpret the vector database response using the LLM
        interpreted_results = await interpret_results_with_llm(results)
        print("this is data: \n", interpreted_results)

        return cl.Message(content=interpreted_results)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return cl.Message(content="An error occurred while making the request.")
    except JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return cl.Message(content="The response from the query endpoint was not in the expected JSON format.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return cl.Message(content="An unexpected error occurred.")



def generate_vector_using_llm(text):
    # Generate embeddings using an LLM
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    vector = response['data'][0]['embedding']
    return vector

def interpret_results_with_llm(results):
    indices = results['indices'][0]
    distances = results['distances'][0]

    response_text = f"Query results:\nIndices: {indices}\nDistances: {distances}"

    interpretation = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": response_text}]
    )

    return interpretation.choices[0].message['content']