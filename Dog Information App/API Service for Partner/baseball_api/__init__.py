import json
from flask import Flask
from baseball_api import baseball_stats
from baseball_api import player_pictures

app = Flask(__name__)

@app.route('/get_player/<name>', methods=["GET"])
def get_player(name):

    # get image and stats for players
    image_link = player_pictures.get_wiki_image(name)
    player_data = baseball_stats.baseball_lookup(name)

    # add image to the dictionary
    #player_data['picture'] = image_link

    # return the JSON object
    return json.dumps(player_data)

if __name__ == '__main__':
    app.run(debug=True)