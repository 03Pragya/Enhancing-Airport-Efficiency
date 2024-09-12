import requests
import json

API_URL_JSON = "https://data.sfgov.org/resource/rkru-6vcg.json"
API_URL_CSV = "https://data.sfgov.org/resource/fpux-q53t.csv"

def AirTrafficClient():

    '''JSON block:
    Downloads and prepares the JSON file'''
    response_json = requests.get(API_URL_JSON)
    data_raw = response_json.json()
    json_data_to_string = json.dumps(data_raw)
    json_data_final = json.loads(json_data_to_string)

    with open("Air_Traffic_Passenger_Statistics.json", "w") as file: #this is a file meant to be use for visibility, to use this data please use the returned data.
        json.dump(data_raw, file)

    print('JSON Processing Done')

    '''CSV block:
    Downloads and prepares the CSV file'''
    csv_response = requests.get(API_URL_CSV)

    with open("Air_Traffice_Landings_Statitics.csv","wb") as file:
        file.write(csv_response.content)

    print("Done saving CSV File")

    return json_data_final
