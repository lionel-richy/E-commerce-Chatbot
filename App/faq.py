import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()  # Charge les variables du fichier .env





client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),) 






faqs_path = Path(__file__).parent / "Ressources/faq_data.csv"
chroma_client = chromadb.Client()
collection_name_faqs = "faqs"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

#faqs_path = "/Ressources/faq_data.csv"
def ingest_faq_data(path):
    print("Ingesting FAQ data into chromadb...")
    collection = chroma_client.get_or_create_collection(name=collection_name_faqs, embedding_function=ef)
    df = pd.read_csv(path)
    docs = df["question"].to_list()
    metadata = [{"answer": ans} for ans in df["answer"].to_list()]
    ids = [f"id_{i}" for i in range(len(docs))]

    collection.add(
        documents=docs,
        metadatas=metadata,
        ids=ids,
    )
    print(f"FAQ Data successfully ingested into chroma collection: ... {collection_name_faqs}")
  


  
def get_relevant_qa(query):
    collection = chroma_client.get_collection(name=collection_name_faqs)
    results = collection.query(
        query_texts= [query],
        n_results=2  
    )
    return results
   
def generate_answer(query, context):
    
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.
    
    
    question: {query}
    context: {context}
    
    '''
    
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
)

    return chat_completion.choices[0].message.content
   
   
   

def chain_faq(query):
    result= get_relevant_qa(query)
    context= ''.join(r.get("answer") for r in result['metadatas'][0])
    answer= generate_answer(query, context)
    return answer
    
    

if __name__ =="__main__":
    
    ingest_faq_data(faqs_path)
    query = "What is your policy on defective products?"
    #results = get_relevant_qa(query)
    #print ("Query Results:", results)
    answer = chain_faq(query)
    print("Query Results:", answer)
    