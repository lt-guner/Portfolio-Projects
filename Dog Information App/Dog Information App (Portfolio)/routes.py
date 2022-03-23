from flask import Flask, render_template, request
import json
import doginfo
from random import randint
from doglist import dog_list

app = Flask(__name__)
app.secret_key = 'A243CE5757B9C3C97A45B38984B66'

@app.route('/', methods=['POST', 'GET'])
@app.route('/search/', methods=['POST', 'GET'])
def search():

    return render_template("search.html")

@app.route('/breeds_random/', methods=['POST', 'GET'])
def random():

    breedone = dog_list[randint(0, 272)]
    breedtwo = dog_list[randint(0, 272)]
    breedthree = dog_list[randint(0, 272)]

    breedonedata = doginfo.get_breed_info(breedone)
    breedtwodata = doginfo.get_breed_info(breedtwo)
    breedthreedata = doginfo.get_breed_info(breedthree)
    return render_template('threebreed.html', breedonedata=breedonedata, breedtwodata=breedtwodata, breedthreedata=breedthreedata)

@app.route('/breeds/', methods=['POST', 'GET'])
def breeds():

    if request.method == 'POST':

        # get the user submissions
        breedone = request.form['dogbreedone']
        breedtwo = request.form['dogbreedtwo']
        breedthree = request.form['dogbreedthree']

        # if only one dog breed was submitted
        if breedtwo == "n/a" and breedthree == "n/a":
            breedonedata = doginfo.get_breed_info(breedone)
            return render_template('onebreed.html', breedonedata=breedonedata)

        # if only two breeds were submitted
        elif (breedtwo == "n/a" and breedthree != "n/a") or (breedtwo != "n/a" and breedthree == "n/a"):
            if (breedtwo == "n/a" and breedthree != "n/a"):
                breedonedata = doginfo.get_breed_info(breedone)
                breedtwodata = doginfo.get_breed_info(breedthree)
                return render_template('twobreed.html', breedonedata=breedonedata, breedtwodata=breedtwodata)
            else:
                breedonedata = doginfo.get_breed_info(breedone)
                breedtwodata = doginfo.get_breed_info(breedtwo)
                return render_template('twobreed.html', breedonedata=breedonedata, breedtwodata=breedtwodata)

        # get data for three dogs
        else:
            breedonedata = doginfo.get_breed_info(breedone)
            breedtwodata = doginfo.get_breed_info(breedtwo)
            breedthreedata = doginfo.get_breed_info(breedthree)
            return render_template('threebreed.html', breedonedata=breedonedata, breedtwodata=breedtwodata, breedthreedata=breedthreedata)