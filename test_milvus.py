from pymilvus import MilvusClient
import json
import requests

client = MilvusClient("milvus_demo.db")

if client.has_collection(collection_name="demo_collection"):
    client.drop_collection(collection_name="demo_collection")
client.create_collection(
    collection_name="demo_collection",
    dimension=768,  # The vectors we will use in this demo has 512 dimensions
)
from pymilvus import model

# Read vectors from clip_response.json
with open('clip_response.json', 'r') as f:
    vectors = json.load(f)

data = [
    {"id": i, "vector": vectors[i], "image_loc": f"output_frames/frame_{i}.jpg", "subject": "history"}
    for i in range(len(vectors))
]

print("Data has", len(data), "entities, each with fields: ", data[0].keys())
print("Vector dim:", len(data[0]["vector"]))

res = client.insert(collection_name="demo_collection", data=data)

query_text = "A girl in front of a ferris wheel."

# Generate vector for text query using CLIP
url = "http://localhost:3000/encode"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# For text-only query, we send empty image blob with the text
payload = [{
    "text": query_text
}]

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    query_vec = response.json()[0]  # Get first (and only) vector from response
else:
    raise Exception(f"Query encoding failed: {response.text}")

print(query_vec)
print(len(query_vec))

query_vectors = [query_vec]

res = client.search(
    collection_name="demo_collection",  # target collection
    data=query_vectors,  # query vectors
    limit=9,  # number of returned entities
    output_fields=["image_loc"],  # specifies fields to be returned
    search_params={"metric_type": "COSINE", "params": {}}
)

print(res)

