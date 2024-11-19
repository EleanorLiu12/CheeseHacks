import bentoml

with bentoml.SyncHTTPClient('http://localhost:3000') as client:
    summarized_text: str = client.summarize([bentoml.__doc__])[0]
    print(f"Result: {summarized_text}")

