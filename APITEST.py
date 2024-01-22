import requests
import json

response_API = requests.get('http://127.0.0.1:5000')
# # Print the response content
# print(response_API.content)

# if response_API.status_code == 200:  # Successful response
#     # Proceed to process data
#     print('hi')
# else:
#     print("API request failed with status code:", response_API.status_code)
#     # Handle the error appropriately

data = response_API.json()  # Convert JSON response to Python dictionary
# Explore the structure of the data using print(data) or a debugger
# Access specific elements based on their keys:
# for state in data['statewise']:
#     print(state['state'], state['confirmed'], state['active'])
