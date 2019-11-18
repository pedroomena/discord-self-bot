import requests
from bs4 import BeautifulSoup


KNOWN_SITES = [
    'rankedboost.com/pokemon-go/',
    'pokemondb.net/pokedex/',
    'www.pokemon.com/us/pokedex/',
    'pokemon.wikia.com/wiki/',
    'bulbapedia.bulbagarden.net/wiki/',
    'rankedboost.com/pokemon-lets-go/'
]
SEARCH_URL = 'https://www.google.com/searchbyimage?hl=en-US&image_url='
HEADERS = requests.utils.default_headers()
HEADERS.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
})


def search(image_url):
    response = requests.get(f'{SEARCH_URL}{SEARCH_URL}{image_url}', headers=HEADERS)
    return parse_results(response.text)


def parse_results(code):
    soup = BeautifulSoup(code, 'html.parser')

    guesses = set()
    guess_link = {}
    for div in soup.findAll('div', attrs={'class': 'rc'}):
        link = div.find('a')['href']
        for site in KNOWN_SITES:
            if site in link:
                guess = link.replace(site, 'ç').split('ç')
                guess = guess[1].split('/')[0].replace('-', ' ').replace('_(Pok%C3%A9mon)', '')
                guess_link[guess] = link
                if guess and not any(i.isdigit() for i in guess):
                    guesses.add(guess.lower())
    guesses = list(guesses)
    print('guesses_sites: {}'.format(guess_link))
    print('guesses: {}'.format(guesses))
    return guesses
