import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


# for i in range(0, 720, 20):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     a = soup.find_all('a', class_='bt-open-in-overlay')
#     for p in a:
#         p = p.get('href')
#         with open('links.txt', 'a') as f:
#             f.write(f'{p}\n')

def get_data():
    with open('links.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]

    for line in lines:
        r = requests.get(line, headers=headers)
        result = r.content

        soup = BeautifulSoup(result, 'lxml')
        name = soup.find(class_='bt-biografie-name').find('h3').text
        link = soup.find_all('a', class_='bt-link-extern')

        social_media = []

        for l in link:
            l = l.get('href')
            social_media.append(l)

        k = name.strip().split(',')
        person_name = k[0]
        name_company = k[1]


        data = {
            'profile_name': person_name,
            'profile_company': name_company,
            'social_media': social_media
        }
        with open('data.json', 'a') as f:
            f.write(json.dumps(data, indent=4))


def main():
    get_data()


if __name__ == '__main__':
    main()