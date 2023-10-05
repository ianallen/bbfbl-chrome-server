from flask import Flask
from flask import jsonify, request
from player_fetcher import fetch_players
from contract_fetcher import fetch_contracts
from client_data_generator import generate_client_data
import json
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS



app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/')
def hello():
    return 'Hello, from the BBFBL World!'


@app.route('/salaries')
def salaries():
    with open("./output/salaries.json") as salary_file, open("./data/hard_coded_salaries.json") as extras:
        salaries = json.loads(salary_file.read())
        extra = json.loads(extras.read())
        salaries.extend(extra)
        return jsonify(salaries)


@app.route('/kick')
def kick():
    force = request.args.get('force', False)
    result = update_salaies_job(force)
    if result:
        return "Complete"
    return "Job Failed"

@app.route('/fetch-players')
def run_fetch_players():
    fetch_players() 
    return 'Success', 200



def update_salaies_job(force=False):
    try:
        player_data = fetch_players(force) 
        contracts = fetch_contracts(force)
        data = generate_client_data(player_data, contracts)
        print("Salary job complete!")
        return True
    except Exception as e:
        print("Job failed:", str(e))
        return False


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(update_salaies_job, trigger = 'interval', minutes = 1440) #1440