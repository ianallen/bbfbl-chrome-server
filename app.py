from flask import Flask
from flask import jsonify
from player_fetcher import fetch_players
from contract_fetcher import fetch_contracts
from client_data_generator import generate_client_data
import json
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def hello():
    return 'Hello, from the BBFBL World!'


@app.route('/salaries')
def salaries():
    with open("./output/salaries.json") as salary_file:
        salaries = json.loads(salary_file.read())
        return jsonify(salaries)




def update_salaies_job():
    try:
        player_data = fetch_players()
        contracts = fetch_contracts()
        data = generate_client_data(player_data, contracts)
        print("Salary job complete!")
    except Exception as e:
        print("Job failed:", e)


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(update_salaies_job, trigger = 'interval', minutes = 2) #1440