import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def boldWord(word,string):
    index = string.find(word)

    if index != -1:
        output_string = string[:index] + '<b>' + word + '</b>' + string[index + len(word):]
    else:
        output_string = string
    return output_string

def getDefEx(soup):
    print()
    first_sense = soup.find('li', class_='sense')
    
    # Making python print the definition of the first sense
    definition = f'<b>{word_to_search}</b>' + ': ' + first_sense.find('span', class_='def').text
    
    # Making python print the first example where the word is used.
    examples = first_sense.find('ul', class_='examples')
    if examples != None:
        first_example = examples.find('span', class_='x').text
    
    # In case Oxford Dictionaries don't have examples available, it will scrape it from Reverso instead
    if examples == None:
        scrape_reverso = 'https://context.reverso.net/translation/english-portuguese/' + word_to_search
        reverso_response = requests.get(scrape_reverso, headers=headers)
        if web_response.status_code == 200:
            soup = BeautifulSoup(reverso_response.text, 'html.parser')
            examples = soup.find('section', id='examples-content')
            twosentences = examples.find('div')
            first_example = twosentences.find('div', class_='src ltr').text
        else:
            print('Failed to get Response...')
    
    return definition, boldWord(word_to_search, first_example)

# creating a dictionary where we put the action that we want to run in Anki, the parameters and version of Anki Connect
def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

# We convert the dictionary to a json string and then POST it to the AnkiConnect Server so that it runs in Anki what we want
def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = requests.post('http://localhost:8765', data=requestJson).json()
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

with open('words.txt', 'r') as f:
    for word in f:
        print(word)
        word_to_search = word.strip()
        scrape_url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + word_to_search

        headers = {"User-Agent": ""}
        web_response = requests.get(scrape_url, headers=headers)

        if web_response.status_code == 200:
            soup = BeautifulSoup(web_response.text, 'html.parser')

            try:
                definition, example = getDefEx(soup)
                note = {'deckName': 'CIMV', 'modelName': 'Basic', 'fields': {'Front': f'{example}', 'Back': f'{definition}'}}
                invoke('addNote', note=note)
            except AttributeError:  
                print('Word not found!!')
        else:
            print('Failed to get response...')
with open('words.txt', 'w') as f:
    pass
