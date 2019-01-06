# play-by-play-scraper
A web scraper for Northwestern Baseball play-by-play data.

This project contains Scrapy spiders for scraping information about every NCAA D1 baseball team, every 2018 NCAA D1 baseball player, and play-by-play data for every 2018 Northwestern University baseball game.

This project also uses Firebase and Algolia to store and search for team, player, and play data.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing Requirements
First, clone the respository.

```
git clone https://github.com/isaacrlee/play-by-play-scraper.git
```

Next, [setup a Python 3 virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/#creating-a-virtualenv), activate it, and install the packages in `requirements.txt`.

### Setting up Firebase and Algolia
Now, setup a Firebase app with a realtime database, and add an authenticated user. [docs](https://firebase.google.com/docs/)

Setup an Algolia app and an index with the name `teams`. [docs](https://www.algolia.com/doc/)

#### Recording Key Information

in `/pbp/pbp/keys.py` record the following information from setting up the Algolia and Firebase apps:
```
algolia_app_id = "XXX"
algolia_api_key = "XXX"

config = {
    "apiKey": "XXX",
    "authDomain": "XXX.firebaseapp.com",
    "databaseURL": "https://XXX.firebaseio.com/",
    "storageBucket": "XXX.appspot.com"
}

email = 'XXX@XXX.com'
password = 'XXX'
```

### Running the Spiders
Uncomment lines 13-19 of `pipelines.py`:
```
# if spider.name == 'team':
#     db.child('teams').child(item['tbc_team_id']).set(item)
# if spider.name == 'player':
#     db.child("players").child(item['tbc_player_id']).set(item)
#     # db.child("players").child(item['tbc_player_id']).update(item)
# if spider.name == 'pbp':
#     db.child("plays").push(item)
```

This function uploads the scraped team, player, and play data to your Firebase database.

In the terminal, make sure you're in the virtual environment and move into the first `pbp` directory:
```
cd pbp
```

Run the team spider first:
```
scrapy crawl team -o teams.json
```
This will also store the scraping output in `teams.json`


Next, run the player spider (Note: this may take a few minutes):

```
scrapy crawl player -o players.json
```
This will store the scraping output in `players.json`

Finally, fun the pbp (play-by-play) spider:

```
scrapy crawl pbp -o pbp.json
```
This will store the scraping output in `pbp.json`.
Note: There may be a couple of exceptions if this spider is run on the given `northwestern_games` pages, this is due to the fact that Northwestern played a couple D3 teams that are not in the database and will be fixed in the future. These exceptions do not stop the rest of the games from being scraped.

After this spider completes, the play-by-play data can be accessed using the Firebase client of your choice or by loading the `pbp.json` file into the data analysis software of your choice.
(I prefer Pyrebase for Python 3 and Jupyter notebooks).

### Using A Different Team's Dataset
This scraper is optimized for pages using the SIDEARM Sports template and has only been tested on Northwestern Baseball games.

A fair amount of code customized specifically for edge cases with Northwestern Baseball games is used and can be found by searching `# CUSTOM` throughout the codebase.

This scraper can be tested on other team's play-by-play data, as long as they use the SIDEARM Sports page template, by loading a different set of `starting_urls` in `pbp_spider.py` (Line 12):
```
# CUSTOM: Northwestern Games
start_urls = northwestern_games
```

If run on a different set of games, it is extremely likely that the regex expressions used in `middlewares.py` will need to be changed, and additional custom code will have to be introduced to deal with different edge case.

### Common Errors

* `Firebase 'Unauthorized'`: Need to add an authorized user to Firebase and record the details in a `keys.py` file.
* `Unknown command: crawl`: Need to change into the `pbp` directory

### Known Issues
* Name parsing not 100% accurate as it relies on a lot of regular expressions and unambiguos play-by-play data.
* The batted ball location for a fielder's choice is not recorded. This is due to difficulties with regular expressions
* Games against non-D1 opponents is not recorded. This can be fixed by adapting the `team` spider to scrape all teams info, not just D1.
* Plays such as dropped fly balls and ejections are skipped.

### Built With
* [Algolia](https://www.algolia.com/)
* [Firebase](https://firebase.google.com)
* [Pyrebase](https://github.com/thisbejim/Pyrebase)
* [Scrapy](https://scrapy.org/)
