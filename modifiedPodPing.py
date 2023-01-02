import requests

def podping():
    URL = 'https://hub.podcastindex.org/pubnotify?id='
    arg = '5734992'
    try:
        output = requests.get(URL + arg).json()
        title = title or arg
        if arg:
            print("Requesting podping for " + title + ': ' + output['descriptio>
        else:
            print("Requesting podping for feed ID" ) #" + arg + ": " + output['>
    except:
        print(output['description'])
podping()