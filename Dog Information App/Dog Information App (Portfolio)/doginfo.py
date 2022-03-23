import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import wikipedia
import urllib
import json

def get_breed_info(breed):

    # main
    soup = breed_url_driver(breed)
    breedinfo = breed_info(soup)
    breedservice = breed_service(breed)
    breedimage = breed_pic(breedservice[0])

    breeddatalist = breedinfo + breedservice + breedimage

    return breeddatalist

def breed_url_driver(breed):
    """
    webscrape the lxml data from akc using selenium and beautifulsoup, then return the scraped page
    """

    # open up the chrome driver for web scraping
    # open options to make it headless so it doesnt open browser
    chromedriver_path = r'C:\\Users\timur\Documents\chromedrive\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)

    # set the url and get the data using get
    urldog = "https://www.akc.org/dog-breeds/{}/".format(breed)
    driver.get(urldog)
    # time.sleep(0)  # if you want to wait 3 seconds for the page to load

    # load the source code into_page source and then use beautifulsoup to pull as lxml
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    return soup

def breed_info(soup):

    """
    parses out the info from akc and returns its as a tuple
    """

    # This will be need for concatenation
    div3 = r'</div></div></div>'
    div = r'</div>'

    # pull the basic info from call classes that are breed-table
    infobreed = soup.find_all("div", class_="breed-table__accordion-padding")
    aboutbreed = soup.find("div", class_="breed-page__about")

    # remove read more
    aboutbreed = str(aboutbreed)
    aboutbreed = aboutbreed.replace("Read More", "")

    healthbreed, groomingbreed, exercisebreed, trainingbreed, nutritionbreed = [str(e) for e in infobreed]

    # for health, grooming, exercise, training, and nutrition cut out the unnecessary source code
    if "<form id=" in healthbreed:
        healthbreed = healthbreed.split("<form id=")[0]
        healthbreed = healthbreed + div3
    if "<form id=" in groomingbreed:
        groomingbreed = groomingbreed.split("<form id=")[0]
        groomingbreed = groomingbreed + div
    if "<form id=" in exercisebreed:
        exercisebreed = exercisebreed.split("<form id=")[0]
        exercisebreed = exercisebreed + div
    if "<form id=" in trainingbreed:
        trainingbreed = trainingbreed.split("<form id=")[0]
        trainingbreed = trainingbreed + div
    if "<form id=" in nutritionbreed:
        nutritionbreed = nutritionbreed.split("<form id=")[0]
        nutritionbreed = nutritionbreed + div

    # make list
    breed_info = [aboutbreed, healthbreed, groomingbreed, exercisebreed, trainingbreed, nutritionbreed]

    # return data
    return breed_info

def breed_service(breed):
    """
    a function to get a json object for breedname, height, weight, lifespan, and group
    """

    # get the json object and parse out the data
    dogbreedonedavid = requests.get("http://127.0.0.1:5000/data/{}".format(breed))
    dogbreedonedavid = dogbreedonedavid.json()
    namebreed = dogbreedonedavid['breed']
    heightbreed = dogbreedonedavid['height']
    weightbreed = dogbreedonedavid['weight']
    lifebreed = dogbreedonedavid['life expentancy']
    groupbreed = dogbreedonedavid['group']
    imagebreed = dogbreedonedavid['picture_url']

    # make list
    service_list = [namebreed, heightbreed, weightbreed, lifebreed, groupbreed, imagebreed]

    # return data
    return service_list

def breed_pic(search_term):
    """
    gets a picture of the dog
    """

    # get the url for the wiki page with the dog breed and get the bs4 data
    url = wikipedia.page(search_term + "Dog").url
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    # declare an address variable
    address = "https:"

    # loop through the image tags until one containing the thumbnail is found and and save it
    for img in soup.select('a.image > img'):
        image = str(img)
        if "thumb" in image:
            image = image.split("src=\"")[1]
            image = image.split(" srcset=\"")[0]
            image = image.split("\"")[0]
            address = address + image
            break

    # return the address
    address = [address]
    return address