from datetime import datetime
import json
from script import send
import script

for i in script.Rappel_league:
    date = datetime.today()
    with open('./Ressource/calendar.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    date_j = str(str(date.year) + '-' + str(date.month) + '-' + str(date.day))
    data_j = data[i]
    for j in data_j:
        if data_j[j] == date_j:
            text = "C\'est le jour J pour " + i + " , pense à ton équipe ou utilise /Auto"
            send(text)
