import requests
import sys
import time
import json
import csv
from datetime import datetime


def create_date():
    month = datetime.now().month
    year = datetime.now().year - 2000
    day = datetime.now().day
    date = str(month) + str(year) + str(day)
    return date

def fetch_players():
    date = create_date()
    url_template = "https://sports.yahoo.com/site/api/resource/sports.team.roster;id=nba.t.{0}?bkt=sports-US-en-US-def&device=smartphone&feature=canvassOffnet%2CenableCMP%2CenableConsentData%2CnewMyTeamsNav%2Csp-nav-test%2CvideoShowTest%2CnewContentAttribution%2Clivecoverage%2CcaasSmartphone%2Ccanvass%2CnflLiveVideo%2CdesktopNotifications%2CsearchAssist%2Clicensed-only%2CdfsFavoriteTeamPromo%2CnewLogo%2CenableScrollRestoration%2CoathPlayer&intl=us&lang=en-US&partner=none&prid=5mk036leqt4rj&region=US&site=sports&tz=America/Montreal&ver=1.0.5052&returnMeta=true"

    entries = []

    for team_id in range(1, 31):
        url = url_template.format(str(team_id))
        user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36"
        headers = {'User-Agent': user_agent}

        print("Getting %s..." % (url))
        print("...")
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)

        # parse player data    
        team = data["data"]["team"]["display_name"]
        player_images = data["data"]["playerimage"]
        player_data = data["data"]["players"]

        print("Got data for %s!" % (team))
        for key in player_data.keys():
            player_id = key.split(".")[2]
            name = player_data[key]["display_name"]
            image_url = player_images[key]
            entry = [int(player_id), name, image_url]
            entries.append(entry)
            print("Added entry for %s (%s)" % (name, player_id))

        time.sleep(1.5)


    output_file = "./output/player_info.csv"
    if os.path.exists(output_file):
        os.remove(output_file)       

    with open(output_file, mode='w+') as out_file:
        writer = csv.writer(out_file, delimiter=",", quotechar='"')
        writer.writerows(entries)

    return entries



