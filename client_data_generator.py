import csv
import re
import json
import os

def _get_date():
    month = datetime.now().month
    year = datetime.now().year - 2000
    day = datetime.now().day
    date = str(month) + str(year) + str(day)
    return date

def _clean_name(name):
    delim_index = name.find("\\")
    if delim_index == 0:
        raise ValueError("Bad player name input %s" % (name))
    return name[0:delim_index].strip()

_slugify_re = re.compile(r"(\.|\s|-|'|III|IV|Jr.|Sr.|II)")
def _slugify(text):
    accentless = remove_accents(text)
    slug = _slugify_re.sub("", accentless)
    return slug.lower()

def _is_fuzzy_match(str1, str2):
    return _slugify(str1) == _slugify(str2)

def remove_accents(text):
    return text \
        .replace("ć", "c") \
        .replace("č", "c") \
        .replace("ö", "o") \
        .replace("í", "i") \
        .replace("á", "a") \
        .replace("š", "s") \
        .replace("ý", "y") \
        .replace("ģ", "g") \
        .replace("ņ", "n") \
        .replace("ū", "u") \
        .replace("ā", "a") \
        .replace("İ", "I") \
        .replace("ò", "o") \
        .replace("Š", "S") \
        .replace("è", "e") \
        .replace("Ž", "Z") \
        .replace("ž", "z") \
        .replace("ó", "o") \
        .replace("é", "e") \
        .replace("Waller-Prince", "Prince") \
        .replace("Mo Bamba", "Mohamed Bamba") \
        .replace("Jakob Pöltl", "Jakob Poeltl") \
        .replace("Maurice Harkless", "Moe Harkless") \
        .replace("Juan Hernangómez", "Juancho Hernangómez") \
        .replace("Sviatoslav Mykhailiuk", "Svi Mykhailiuk")

def _salary_to_number(text):
    if text == "": return None
    return int(text.replace("$", "").replace(",", ""))


def generate_client_data(player_data, contract_data):
    output = []
    for contract in contract_data:
        record = {}
        record["name"] = contract["Player"]
        record["salary20_21"]= _salary_to_number(contract["2020-21"])
        record["salary21_22"]= _salary_to_number(contract["2021-22"])
        record["salary22_23"]= _salary_to_number(contract["2022-23"])
        record["salary23_24"]= _salary_to_number(contract["2023-24"])

        for row in player_data:
            if _is_fuzzy_match(row[1], record["name"]):
                record["name"] = row[1] # overwrite with Yahoo! name
                record["yahoo_id"] = int(row[0])
                output.append(record)
                break

        # Log if no match is found
        try:
            record["yahoo_id"]
        except KeyError as e:
            print("Couldn't find match:", record["name"], _slugify(record["name"]))

    output_path =  "./output/salaries.json"
    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, "w+") as out_file:
        json.dump(output, out_file)

    return output



