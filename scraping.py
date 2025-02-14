##Honda dealer

import pandas as pd
import requests
import requests
from bs4 import BeautifulSoup
import json, re

df = pd.DataFrame(columns=['Overall rank',
    'Law School Name',
    'Bus/Corp Law',
    'Clinical Training',
    'Const. Law',
    'Contracts/Comm Law',
    'Crim. Law',
    'Dispute Res.',
    'Environmental',
    'Health Care',
    'Intell. Prop.',
    'Internat.',
    'Legal Writing',
    'Tax Law',
    'Trial Advoc.',
    'Peer Assess. Score',
    'Assess. by Lawyers/Judges',
    'Median GPA',
    'Median LSAT',
    'acceptance',
    'studen-faculty ratio',
    'full-credit outcomes',
    'first-time bar',
    'avg first time bar among states',
    'ultimate bar pass'])

url = "https://www.usnews.com/best-graduate-schools/api/search?format=json&program=top-law-schools&specialty=law"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
           'content-type': 'application/json',
           'x-origin': 'BestGraduateSchools',
           'x-powered-by': 'Best Graduate Schools',
           'content-security-policy': "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:; style-src 'self' 'unsafe-inline' https: data:; img-src 'self' https: data: blob: android-webview-video-poster:; font-src https: data:; connect-src https: wss: blob:; media-src https: data: blob:; object-src 'none'; child-src https: data: blob:; form-action https:; frame-ancestors 'self' https://*.usnews.com;"}

pages = requests.get(url, headers=headers).json()['data']['totalPages']

for page in range(1, pages):

    url_page = "https://www.usnews.com/best-graduate-schools/api/search?format=json&program=top-law-schools&specialty=law&_page={}".format(page)
    items = requests.get(url_page, headers=headers).json()['data']['items']

    for item in items:

        url = item['url']
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content)
        
        data_dicts = []
        row_dict = {}

        row_dict['Overall rank'] = item['ranking']['display_rank']
        row_dict['Law School Name'] = item['name']

        target = soup.select('.jQPDxW')[0]
        for row in target:
            if row.name == 'div':
                row_dict[row.find_next('div').text] = row.find_next('div').find_next('div').text

        target = soup.select('.rank-list')[1]

        for row in target.select('.rank-list-item'):
            details = row.select('.has-badge')
            row_dict[details[0].findChildren('strong')[1].text] = details[0].findChildren('strong')[0].text
            
        data_dicts.append(row_dict)
            
        df = pd.DataFrame(data_dicts)
        df.to_excel('./school/{}.xlsx'.format(item['name']))
