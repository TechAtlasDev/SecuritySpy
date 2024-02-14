# Modulo para realizar las consultas
import re
import shodan
import requests
from bs4 import BeautifulSoup
import json, os

def load_api_key():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "config.json")
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            return config.get("api_key")
    except FileNotFoundError:
        return None

def save_api_key(api_key):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    with open(config_path, "w") as config_file:
        json.dump({"api_key": api_key}, config_file)

def is_ip(data):
    return re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data)

def ipquery(ip:str, key:str) -> dict:
    """Una funcion que permite realizar consultas a la base de datos de shodan con la API KEY con la suscripción gratuita."""
    API = shodan.Shodan(key)
    DATA_IP = API.host(ip)
    return json.dumps(DATA_IP)

def search(query, facet="ip", limit=30):
    DICTY = {}
    
    URL = f"https://www.shodan.io/search/facet?query={query}&facet={facet}"

    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": '"gzip", "deflate", "br"',
        "Accept-Language": "es-US,es-419;q=0.9,es;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Referer": URL,
        "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

    data = f"query={query}&facet={facet}"
    response = requests.get(URL, headers=header, data=data)

    soup = BeautifulSoup(response.text, "lxml")
    caja = soup.find_all("div", class_="four columns name", limit=limit)
    conteo = soup.find_all("div", class_="one column value", limit=limit)
    for counter, (container_data, container_amount) in enumerate(zip(caja, conteo)):
        counter += 1
        data = container_data.find("strong").get_text()
        amount = container_amount.get_text()
        DICTY[data] = amount
    return DICTY