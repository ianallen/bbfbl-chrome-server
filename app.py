from flask import Flask
from flask import jsonify
from player_fetcher import fetch_players
from contract_fetcher import fetch_contracts
from client_data_generator import generate_client_data
import json

app = Flask(__name__)
app.config["DEBUG"] = True

#players = fetch_players()
# contracts = fetch_contracts()
# players = fetch_players()

# data = generate_client_data(players, contracts)


@app.route('/')
def hello():
    return 'Hello, from the BBFBL World!'


@app.route('/salaries')
def salaries():
    with open("./output/salaries.json") as salary_file:
        salaries = json.loads(salary_file.read())
        return jsonify(salaries)