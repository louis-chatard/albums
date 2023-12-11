import os
import requests
from bs4 import BeautifulSoup
import re

artists = ['hugo tsr']

# List to store URLs that fail
failed_urls = []

for artist in artists:
    artist = artist.replace(' ', '-')
    artist = artist.replace("'", "")
    try:
        url = 'https://genius.com/artists/' + artist + '/albums'
        # Get the HTML content
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the specified ul tag
        ul_tag = soup.find('ul', {'class': 'ListSectiondesktop__Items-sc-53xokv-8 kbIuNQ'})

        # Make sure the directory for images exists
        os.makedirs(f'images/{os.path.basename(url)}', exist_ok=True)

        # For each li tag in the ul
        for li in ul_tag.find_all('li'):
            # Find the img and h3 tags
            img_tag = li.find('img')
            h3_tag = li.find('h3')

            if img_tag and h3_tag:
                img_url = img_tag.get('src')
                img_name = h3_tag.text

                # Remove any characters from the h3 text that are not valid in file names
                img_name = re.sub(r'[\\/*?:"<>|]', '', img_name)

                if img_url:
                    # Download the image
                    img_response = requests.get(img_url, stream=True)
                    img_response.raise_for_status()

                    # Save the image to a file
                    img_file = os.path.join(f'images/{artist}', img_name + '.jpg')
                    os.makedirs(os.path.dirname(img_file), exist_ok=True)
                    with open(img_file, 'wb') as f:
                        for chunk in img_response.iter_content(chunk_size=8192):
                            f.write(chunk)
        print(artist, "successfully downloaded")
    except Exception as e:
        print(f"Failed to process: ", artist)
        failed_urls.append(url)

if failed_urls != []:
    # Write the failed URLs to a file
    with open('failed_urls.txt', 'w') as f:
        for url in failed_urls:
            f.write(url + '\n')

