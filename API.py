import requests

API_KEY = "AIzaSyAT0CflO09eapMvWMOgX8P_-w8HIpUnojE"
CX = "039135c55604b4b19"
query = "Sunset over the ocean"

# API Request
url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={CX}&searchType=image&key={API_KEY}"
response = requests.get(url).json()
# print(response)
# Print first image URL
if "items" in response:
    image_url = response["items"][0]["link"]
    print("Image URL:", image_url)
