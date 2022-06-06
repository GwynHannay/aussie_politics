import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlopen


federal_register_url = 'https://www.legislation.gov.au'

register_sections = [
    'Browse/ByTitle/Constitution/InForce'
    # 'Browse/ByTitle/Acts',
    # 'Browse/ByTitle/LegislativeInstruments',
    # 'Browse/ByTitle/NotifiableInstruments',
    # 'Browse/ByTitle/Gazettes',
    # 'Browse/ByTitle/Bills',
    # 'Browse/ByRegDate/AdministrativeArrangementsOrders',
    # 'Browse/ByTitle/NorfolkIslandLegislation',
    # 'Browse/ByTitle/PrerogativeInstruments'
]


def build_scrape_url(base_url, index_url):
    return urljoin(base_url, index_url)


def get_soup(url):
    response = urlopen(url)
    soup = BeautifulSoup(response, "html.parser")
    return soup


def get_constitution():
    scrape_url = build_scrape_url(federal_register_url, register_sections[0])
    soup = get_soup(scrape_url)
    series_details = soup.find_all('input', value='View Series')
    series_id = ''

    for button in series_details:
        series_id = re.findall(r'/Series/([A-Za-z0-9]*)"', str(button))[0]
    
    return series_id


def get_series(series_id):
    landing_url = build_scrape_url(federal_register_url, ''.join(['Series/', series_id]))
    soup = get_soup(landing_url)
    table_contents = soup.find_all('table', class_='rgMasterTable')
    table_headers = table_contents[0].thead.find_all('th', class_='rgHeader')
    print(table_headers)