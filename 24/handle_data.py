#!/usr/bin/env python3

import os
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
# Function to extract desired data from JSON
def extract_data(json_data):

    obj = {}
    # Extract relevant information
    obj["headline"] = json_data[0]["data"]["headline"]
    #print(obj["headline"])
    #day = json_data[2]["data"]["items"][0]["day"]
    nat = json_data[0]["data"]["nationalityCode"]
    obj["nationality"] = country_codes.get(nat, nat)
    app = get_appearence_data(json_data[0]["data"]["appearences"])
    obj["stage"] = app["stage"]
    obj["date"] = app["date"]
    obj["timeOfDay"] = app["timeOfDay"]
    obj["startDate"] = app["startDate"]
    obj["endDate"] = app["endDate"]
    endDateNotPushed = True
    if obj["timeOfDay"] < "05.00":
        start_date = datetime.fromisoformat(obj["startDate"]) + timedelta(days=1)
        obj["startDate"] = start_date.isoformat()
        if obj["endDate"]:
            end_date = datetime.fromisoformat(obj["endDate"]) + timedelta(days=1)
            obj["endDate"] = end_date.isoformat()
            endDateNotPushed = False

    if obj["endDate"]:
        end_date = datetime.fromisoformat(obj['endDate'])
        if end_date.time() < datetime.strptime("05:00:00", "%H:%M:%S").time() and endDateNotPushed:
            end_date = datetime.fromisoformat(obj["endDate"]) + timedelta(days=1)
            obj["endDate"] = end_date.isoformat()

    if "endDate" not in obj or obj["endDate"] is None:
        obj["endDate"] = obj["startDate"]
    # print(obj["headline"])
    # print(obj["endDate"])
    duration = datetime.fromisoformat(obj["endDate"]) - datetime.fromisoformat(obj["startDate"])
    obj["length"] = int(duration.total_seconds() / 60)
    # print(obj["length"])
    obj["description"] = json_data[1]["data"]["headline"]
    description = json_data[3]["data"]["text"]
    soup = BeautifulSoup(description, "html.parser")
    #obj["text"] = soup.get_text()
    obj["musObj"] = analyze_text(soup.get_text())
    obj["musician"] = obj["musObj"]["type"]
    # obj["musician"] = "test"
    #if obj["musiker"]["count"] == 1:
        #print(json.dumps(obj))


    return obj


def analyze_text(text):
    count_han = text.count("han")
    count_hun = text.count("hun") + text.count("hendes")
    #count_hun = count_hun + text.count("hendes")
    total_count = count_han + count_hun
    obj = {
        "count": total_count
    }
    if total_count < 2:
        obj["type"] = "band"
        return obj

    pop_han = count_han / total_count
    pop_hun = count_hun / total_count
    if pop_han > 0.5:
        obj["type"] = "mand"
        return obj

    if pop_hun > 0.5:
        obj["type"] = "kvinde"
        return obj
    if "type" not in obj:
        obj["type"] = "ukendt"
        return obj

    measures = {
        "han": count_han,
        "hun": count_hun,
        "pop_han": pop_han,
        "pop_hun": pop_hun,
        "count": total_count
    }
    return measures

def get_appearence_data(app):
    obj = {
        "stage": "",
        "date": ""
    }
    if len(app) != 0 and isinstance(app[0], dict):
        obj["stage"] = app[0].get("stage").replace(" Scene", "")
        obj["date"] = app[0].get("date")
        obj["timeOfDay"] = app[0].get("timeOfDay")
        obj["startDate"] = app[0].get("startDate")
        obj["endDate"] = app[0].get("endDate")

    return obj

#Load country codes
with open('../countryCodes.json', 'r') as file:
    country_codes = json.load(file)


# Directory containing JSON files
directory = "./"

# List JSON files in the directory
json_files = [f for f in os.listdir(directory) if f.endswith(".json")]
bands = []
bands_dict = {}
replaceDate = "20240604"
# Loop through each JSON file
for json_file in json_files:
    band = {}
    # Construct full path to JSON file
    json_path = os.path.join(directory, json_file)
    #band_name = json_file.replace("da-band-20240430-", "").replace(".json", "")
    band_name = json_file.replace("da-band-" + replaceDate + "-", "").replace(".json", "")
    rf_link = "https://www.roskilde-festival.dk/program/musik/" + band_name
    #print(band_name)
    # Read JSON data from file
    with open(json_path, "r") as f:
        json_data = json.load(f)

    # Extract desired data
    #headline, description, day = extract_data(json_data)
    obj = extract_data(json_data)
    obj["rfLink"] = rf_link
    bands.append(obj)
    bands_dict[band_name] = obj
    #print(obj)
    # Print or process the extracted data as needed
    #print(f"Band: {obj['headline']}")
    #print(f"Nationality: {obj['nationality']}")
    #print(f"Description: {obj['description']}")
    #print()

sorted_bands = sorted(bands, key=lambda x: (x['startDate'], x['stage']))
print(json.dumps(sorted_bands))
#print(json.dumps(bands))
#print(json.dumps(bands_dict))


columns = ["headline", "nationality", "description", "musician", "timeOfDay", "length", "stage", "date", "rfLink"]

# Write the data to a TSV file
with open("output.tsv", "w", newline="", encoding="utf-8") as tsvfile:
    writer = csv.DictWriter(tsvfile, fieldnames=columns, delimiter="\t")

    # Write the header
    writer.writeheader()

    # Write each dictionary as a row in the TSV file
    for entry in sorted_bands:
        entry["timeOfDay"] = "'" + entry["timeOfDay"]
        writer.writerow({key: entry[key] for key in columns})
