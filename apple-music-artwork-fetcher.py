# Copyright (c) 2024 Amer Nejma for El Distro Network
# All rights reserved.
#
# This script is licensed under the MIT License.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, under the terms of the MIT License.

import requests
import re

def get_itunes_album_art(itunes_url):
    # Improved regex to capture the numeric album ID correctly
    album_id_match = re.search(r"/album/[^/]+/(\d+)", itunes_url)
    if not album_id_match:
        print("Invalid Apple Music album URL")
        return
    
    album_id = album_id_match.group(1)
    print("Attempting to get high-resolution artwork from Apple Music...")
    
    url = f"https://itunes.apple.com/lookup?id={album_id}&entity=album"
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            artwork_url = results[0].get("artworkUrl100", "").replace("100x100bb", "3000x3000bb")
            print("High-resolution album art found (3000x3000):", artwork_url)
            return
    print("Could not retrieve high-resolution artwork from Apple Music.")

if __name__ == "__main__":
    itunes_url = input("Enter Apple Music album URL: ")
    get_itunes_album_art(itunes_url)
