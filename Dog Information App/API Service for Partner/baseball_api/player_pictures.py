import json
import requests
import wikipedia

def get_wiki_image(search_term):

    # set the wikipedia url for searching through pictures
    WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

    try:
        # try to pull the image with the wikpedia api and return it else return 0
        result = wikipedia.search(search_term, results=1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title=result[0])
        title = wkpage.title
        response = requests.get(WIKI_REQUEST + title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
    except:
        return 0

