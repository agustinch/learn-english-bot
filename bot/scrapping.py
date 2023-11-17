import requests
import time
from bs4 import BeautifulSoup

def get_longman_definition(word):
    base_url = "https://www.ldoceonline.com/dictionary/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Make the request to the Longman website
        response = requests.get(base_url + word, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        time.sleep(1)  # Introduce a delay to avoid making too many requests in a short period
        definitions = {}

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the entry with class "ldoceEntry Entry"
            definitions = {}
            audio = ''
            for en in soup.find_all('span', class_='ldoceEntry Entry'):
                
                # Initialize a dictionary to store definitions
                if en.find('span', class_='speaker amefile fas fa-volume-up hideOnAmp'):
                    audio = en.find('span', class_='speaker amefile fas fa-volume-up hideOnAmp').attrs['data-src-mp3']
                # Loop through each sense of the word
                for sense in en.find_all('span', class_='Sense'):
                    # Get the sense number
                    definition = ''
                    type = sense.find('span', class_='SIGNPOST').text.strip() if sense.find('span', class_='SIGNPOST') else ''
                    sense_number = sense.find('span', class_='sensenum span').text.strip() if sense.find('span', class_='sensenum span') else ''
                    key = sense_number
                    if type:
                        key = key + ' - ' + type

                    # Get the definition
                    if sense.find('span', class_='DEF'):
                        definition = sense.find('span', class_='DEF').text.strip()
                        definitions[key] = definition

            return definitions, audio
        return f"Definition for {word} not found."

    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Request Error: {err}"

get_longman_definition('test')
