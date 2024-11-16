import requests
import base64
import json

# Define the API endpoint
url = "http://localhost:3000/encode"

# Define the headers
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Define the payload
import os

output_frames = os.listdir('output_frames')

payload = [{"img_blob": base64.b64encode(open(f"output_frames/{frame}", 'rb').read()).decode()} for frame in output_frames]

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Check the response status and print the result
if response.status_code == 200:
    response_data = response.json()
    print("Response JSON:", response_data)
    
    # Save response to a file
    with open('clip_response.json', 'w') as f:
        json.dump(response_data, f, indent=4)
else:
    print("Request failed with status code:", response.status_code)
    print("Response:", response.text)

print(response_data[0])
print(len(response_data[0]))

