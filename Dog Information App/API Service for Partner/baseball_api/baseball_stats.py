import requests
from bs4 import BeautifulSoup

def baseball_lookup(search_term):

    # request data from the url and parse the it with bs4
    url = requests.get('https://www.baseball-reference.com/awards/hof.shtml')
    soup = BeautifulSoup(url.text, 'html.parser')

    # base the table of stats to the baseball table
    baseball_table = soup.find('table', class_='sortable stats_table')

    # loop through all data of the tbody
    for player in baseball_table.find_all('tbody'):

        # store all data in rows for each row
        rows = player.find_all('tr')

        # loop through rows to pull individual data
        for row in rows:

            # pull the player name
            player_name = row.find_all('td')[0].text.strip()

            # if the player name = the search term pull the rest of stats by column and store that data in temp_dict
            # and return it
            if player_name == search_term:

                temp_dict = {}

                year_inducted = row.find_all('th')[0].text.strip()
                temp_dict["Year"] = year_inducted

                position = row.find_all('td')[3].text.strip()

                temp_dict["Position"] = position

                lifespan = row.find_all('td')[1].text.strip()
                temp_dict["Lifespan"] = lifespan

                voted_by = row.find_all('td')[2].text.strip()
                temp_dict["Voted By"] = voted_by

                votes = row.find_all('td')[4].text.strip()
                temp_dict["Votes"] = votes

                ballet_percentage = row.find_all('td')[5].text.strip()
                temp_dict["Ballot Percent"] = ballet_percentage

                # --------------- This pulls the image url from the table-----------------
                player_td_data = str(row.find_all('td')[0])
                player_td_data = player_td_data.split("href=\"")[1]
                player_td_data = player_td_data.split("\">")[0]
                player_td_data = "https://www.baseball-reference.com" + player_td_data

                player_url = requests.get(player_td_data)
                soup2 = BeautifulSoup(player_url.text, 'html.parser')
                player_image_div = str(soup2.find_all('div', class_="media-item multiple"))
                player_image_div = player_image_div.split("src=\"")[1]
                player_image_div = player_image_div.split("\"/>")[0]

                temp_dict["picture"] = player_image_div
                # -----------------------------------------------------------------------

                return temp_dict

    # return 0 if not found
    return 0