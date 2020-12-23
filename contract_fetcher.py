from bs4 import BeautifulSoup
import requests
import re
import csv
import os


def fetch_contracts():
    contracts_url = "https://www.basketball-reference.com/contracts/players.html"
    r = requests.get(contracts_url)

    contracts_html = r.text
    soup = BeautifulSoup(contracts_html, "html.parser")

    contracts_table = soup.find(id="player-contracts")

    player_id_regex = re.compile("\/\S\/(\S+\d)\.html")
    
    contracts = []
    contract_rows = contracts_table.tbody.find_all("tr")

    for row in contract_rows:
        row_data = [data.text for data in row.findAll("td")]
        if len(row_data) == 0:
            continue
        url = row.find("a").get("href")
        match = player_id_regex.search(url)
        row_data.append(match.group(1))
        contracts.append(row_data)



    contracts_output_file = "./output/contracts_20_21.csv"

    contracts_keys = [
        "Player",
        "Team",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26",
        "SignedUsing",
        "Guaranteed",
        "PlayerId"
    ]

    if os.path.exists(contracts_output_file):
        os.remove(contracts_output_file)


    with open(contracts_output_file, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(contracts_keys)
        writer.writerows(contracts)


    ret = [dict(zip(contracts_keys, contract)) for contract in contracts]
    return ret

