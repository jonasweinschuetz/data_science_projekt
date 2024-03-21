import pandas as pd
import json
from parse_raw_data_scraped import parse_mensa_files
from cleaning_scraped import filter_vvo_tags

# files that will be read and parsed, must be in directory called raw-data
file_names = ["flensburg-cafeteria","flensburg-mensa","heide-mensa-mit-cafeteria","kiel-mensa-1","kiel-mensa-2","kiel-mensa-gaarden","kiel-mensa-kasselhaus-mit-cafeteria","luebeck-mensa-mit-cafeteria","luebeck-musikhoschschule-cafeteria"]

data = []

total_attempted = 0
total_success = 0
total_failed = 0

for name in file_names:
    attempted, success, failed = parse_mensa_files(name, data)

    total_attempted += attempted
    total_success += success
    total_failed += failed 


arguments = ["location", "date", "mensa", "name", "student_price", "faculty_price", "guest_price", "category"]
data = pd.DataFrame(data, columns=arguments)


datetime = pd.to_datetime(data["date"], format="%Y-%m-%d")
data.drop(columns="date", inplace=True)
data["date"] = datetime


#!!Attention!! if new data entries are done please check manualy if new relevant vvo_tags are available and update the applicable list
# filter_vvo_tags should throw "Tags missed" message in case entries contain tags that are not present in (non_)vvo_tags
# domain(data["category])   # may help finding the problematic tags
# vegan/vegetarian/omnivore tags 
vvo_tags = ['Enthält Rind', 'Enthält Geflügel', 'Enthält Schwein aus artgerechter Haltung', 'vegetarisch', 'vegan', 'Enthält Geflügel aus artgerechter Haltung', 'Enthält Schwein',  'Enthält Fisch aus artgerechter Haltung', 'Enthält Lamm']
non_vvo_tags = ['International','mensaVital', 'enthält Alkohol']

data["vvo_tags"], data["additional_notes"] = filter_vvo_tags(data, vvo_tags, non_vvo_tags)
data.drop(columns="category", inplace=True)
print(data)



data = data.astype({"location":"category", "mensa":bool, "student_price":"float32", "faculty_price":"float32", "guest_price":"float32"})
# data.to_csv("scraped-data.csv", sep="@")

