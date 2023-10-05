from bs4 import BeautifulSoup
import requests
import re
import csv
import os
import time
from datetime import date

team_index_url = "https://www.spotrac.com/nba/"

def fetch_contracts(refresh=False):
    if not refresh:
        print("Fetching contracts from cache...")
        with open("./output/contracts_23_24.csv") as raw:
            reader = csv.DictReader(raw)
            data = []
            for row in reader:
                data.append(row)
            return data
        
    team_index = get_page(team_index_url)
    urls = parse_team_index(team_index)
    # urls = urls[0:1]
    print(urls)
    player_info = []
    for url in urls:
        print(url)
        time.sleep(2) #be nice...
        print(f"Fetching: {url}...")
        team_page = get_page(url)
        data = parse_team_page(team_page) # get the url [2]
        # print(data)
        for player in data:
            try:
                player_row = fetch_player_salaries(player)
                player_info.append(player)
                print('player', player_row)
            except Exception:
                print(f'Could not fetch {player[0]}')
                continue

    today = date.today().strftime("%b-%d-%Y")
    outfilename = "./output/contracts_23_24.csv"
    headers = ["Player", "current_salary", "salary_url", 'sportrac_id', '2023-24', '2024-25', '2025-26', '2026-2027']
    with open(outfilename, "w+", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)      
        writer.writerow(headers)
        writer.writerows(player_info)
    
    ret = [dict(zip(headers, info)) for info in player_info]
    return ret



def get_page(url):
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Status code: {res.status_code}. Check the request")
        raise 

    return res.content

def parse_team_index(team_index):
    soup = BeautifulSoup(team_index, 'html.parser')
    links = soup.select("a.team-name")
    urls = [link["href"] for link in links]
    return urls
    
def parse_team_page(team_page):
    soup = BeautifulSoup(team_page, 'html.parser')

    # There's a bunch of tables with the same classes so lets just grab the one we need
    player_table = soup.select("table")[0]
    player_links = player_table.select("td.player a")
    
    names = [link.text.strip() for link in player_links]
    player_refs = [link["href"].strip() for link in player_links]   
    salaries = [entry.text.strip() for entry in soup.select("td.result.right.xs-visible .cap.info")]
    
    return _transpose([names, salaries, player_refs])

def parse_player_page(page):
    soup = BeautifulSoup(page, 'html.parser')

    salary_table = soup.select("table.salaryTable")[2]
    # print(salary_table)
    salary_rows = salary_table.select('table.salaryTable .salaryRow')
    # print(salary_rows)
    cap_figures = []
    for row in salary_rows:
        cap_figures.extend(row.select('td.result'))
    # print(cap_figures)
    result =  filter(lambda x: 'Hold' not in x, [e.text for e in cap_figures])
    # print(list(result))
    return list(result)

def fetch_player_salaries(player_data):
    time.sleep(2)
    player_url = player_data[2]
    # print(player_url)
    player_page = get_page(player_url)
    player_id = player_url.split('/')[-2]
    salary_info = parse_player_page2(player_page)
    player_data.append(int(player_id))
    player_data.extend(salary_info)
    return player_data

def parse_player_page2(page, debug=False):
    if not debug:
        soup = BeautifulSoup(page, 'html.parser')
    else:
        f = open('./sample_player_page.html')
        soup = BeautifulSoup(f, 'html.parser')

    salary_table = soup.select("table.salaryTable")[2]
    # print(salary_table)
    salary_rows = salary_table.select('table.salaryTable .salaryRow')
    # print(salary_rows)
    years = []
    cap_figures = []
    for row in salary_rows:
        year = row.select('td a')
        figure = row.select('td.result')
        years.extend(year)
        cap_figures.extend(figure)
    # print([e.text for e in years], [e.text for e in cap_figures])

    # extract year and cap number from the pulled out elements
    # Note that we can zip() this into tuples
    years = [e.text.strip() for e in years]
    cap_figures = [e.text.strip() for e in cap_figures]
    result = {}
    for i, year in enumerate(years):
        result[int(year)] = cap_figures[i]
    # print("result", result)
    #  Filter out any "Hold" cap figures and any years outside if the window
    to_remove = []
    for k, v in result.items():
        if 'Hold' in v:
            to_remove.append(k)
        if k not in [2023, 2024, 2025, 2026]:
            to_remove.append(k)

    for k in to_remove:
        del result[k]

    # return the salaries ** in order **
    ordered_keys = sorted(result.keys())
    ret = []
    for k in ordered_keys: 
        val = sal_to_int(result[k])
        ret.append(val)

    # print(ret)
    return ret


def sal_to_int(sal_str):
    return int(sal_str.replace(',', '').replace('$', ''))

def _transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]
        
def _flatten(t):
    return [item for sublist in t for item in sublist]

def _fill(arr, limit=8):
    length = len(arr)
    remainder = limit - len
    while remainder > 0:
        arr.append(None)
        remainder - remainder - 1