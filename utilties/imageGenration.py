import requests

import json
class image_API:
    def get_image(text):

        API_KEY = "our_Key"
        CX = "Your_Key"
        query = text

        # API Request
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={CX}&searchType=image&key={API_KEY}"
        response = requests.get(url).json()
        # print(response)
        # Print first image URL
        if "items" in response:
            image_url = response["items"][0]["link"]
            return image_url
        return "Not Available"
