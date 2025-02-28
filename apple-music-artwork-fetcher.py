# Copyright (c) 2024 Amer Nejma for El Distro Network
# All rights reserved.
#
# This script is licensed under the MIT License.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, under the terms of the MIT License.

import requests
import re
import os

def get_itunes_album_art(itunes_url):
    # Improved regex to capture the numeric album ID correctly
    album_id_match = re.search(r"/album/([^/]+)/(\d+)", itunes_url)
    if not album_id_match:
        print("Invalid Apple Music album URL")
        return False
    
    album_name = album_id_match.group(1).replace('-', ' ').title()
    album_id = album_id_match.group(2)
    print(f"Attempting to get high-resolution artwork for '{album_name}' from Apple Music...")
    
    url = f"https://itunes.apple.com/lookup?id={album_id}&entity=album"
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            artwork_url = results[0].get("artworkUrl100", "").replace("100x100bb", "3000x3000bb")
            if "3000x3000bb" not in artwork_url:
                artwork_url = artwork_url.replace("1400x1400bb", "3000x3000bb")
            print("High-resolution album art found. Downloading...")
            return download_artwork(artwork_url, album_name)
    print("Could not retrieve high-resolution artwork from Apple Music.")
    return False

def download_artwork(artwork_url, album_name):
    response = requests.get(artwork_url, stream=True)
    if response.status_code == 200:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_name = f"{album_name}.jpg".replace(" ", "_")  # Replace spaces with underscores
        file_path = os.path.join(script_directory, file_name)
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Artwork successfully downloaded to: {file_path}")
        return True
    else:
        print("Failed to download artwork.")
        return False

if __name__ == "__main__":
    while True:
        itunes_url = input("Enter Apple Music album URL (or type 'exit' to quit): ")
        if itunes_url.lower() == 'exit':
            print("Thank you for using El Distro Network's Artwork Fetcher! Visit us at https://www.eldistronetwork.com 🚀")
            break
        success = get_itunes_album_art(itunes_url)
        if success:
            print("✅ Done! Want to grab another one? Enter a new URL or type 'exit' to quit.")
