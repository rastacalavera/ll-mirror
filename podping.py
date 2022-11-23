import requests

def podping():
    URL = 'https://hub.podcastindex.org/pubnotify?id='
    arg = '5734992'
    output = requests.get(URL + arg).json()
    print(output['description'])
podping()
