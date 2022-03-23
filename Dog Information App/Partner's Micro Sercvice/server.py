#########################################################################
#   
#   Microservice provided by David Mingeaud to Timur Guner
#   CS361 Fall 2021
#      
#   Request Format - 'text_string"
#   Response Format - JSON file = {'breed':'text',
#                                  'height':'text',
#                                  'weight':'text',
#                                  'life expentancy':'text',
#                                  'group':'text',
#                                  'picture_url':'text'}
#########################################################################
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
from bs4 import BeautifulSoup
from bs4 import Comment
import requests
import urllib.request

# Creates a Flask App for recieving/sending data
app = Flask(__name__)
api = Api(app)

# Imports a locally saved list of breeds with the photo URLs.
file_name = "dog_output.json"
with open(file_name, 'r') as infile:
    dog_data = json.load(infile)

# The base URL for finding breed data
link = 'https://www.akc.org/dog-breeds/'

# initializing the response in JSON format
response = {'breed':'',
            'height':'',
            'weight':'',
            'life expentancy':'',
            'group':'',
            'picture_url':''}


class Data(Resource):
    '''
    Handles the response as either a GET or POST. A dog breed sent in as text string, and a JSON is returned as the response.
    '''
    def get(self, name):
        '''
        If the request is in GET format, the request is sent directly to process_request()
        '''
        return self.process_request(name)

    def post(self, name):
        '''
        If the request is in POST format, the request is sent directly to process_request()
        '''
        return self.process_request(name)

    def process_request(self, name):
        '''
        Takes the breed name in as a text string and scrapes AKC.org for breed information and returns
        a JSON file.
        '''

        # This for loop is an error handler. If the breed doesn't exist the initialized empty response is sent.
        # otherwise this loop will fill in the JSON with data.
        for x in dog_data:
            # if the request matches a breed from the list continue to fill in the JSON
            if x['request_name'] == name:
                response['breed'] = x['breed']
                response['picture_url'] = x['picture_url']
                response['group'] = x['group']

                # scrapes the website for the entire HTML text
                html_text = requests.get(link + name).text
                soup = BeautifulSoup(html_text, 'html.parser')

                # AKC.org put breed data into the comments. This line specifically parses comments from their HTML and splits
                # into indivdual list items
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                temp = str(comments[8])
                temp = temp.split('\n')

                # assigns the JSON file with the pasted data from AKC.org
                response['height'] = self.clean_text(temp[4])
                response['weight'] = self.clean_text(temp[5])
                response['life expentancy'] = self.clean_text(temp[6])
      
        return response

    def clean_text(self, text):
        '''
        Parses the text from the individual HTML comments and returns only the breeds information
        '''
        parsed_text = text.split(': ')[1]
        parsed_text = parsed_text.split('<')[0]
        return parsed_text


# Starts the REST request listener. recieves text in either GET or POST
api.add_resource(Data, "/data/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
