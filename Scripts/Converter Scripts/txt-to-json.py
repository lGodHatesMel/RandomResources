import csv
import json

#RaidCalc .csv full columns list:
#  "Seed", "Species", "Shiny", "EC", "PID", "Tera Type"
#  "HP", "Atk", "Def", "SpA", "SpD", "Spe", "Ability"
#  "Nature", "Gender", "Height", "Weight", "Scale", "Drops"

# Define which columns to include in the output
columns_to_include = ['Seed', 'Species', 'Tera Type', 'Gender', 'Scale', 'Shiny']

# Reads the CSV data 
with open('Scarlet_4_xxxl.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = [{key: row[key] for key in columns_to_include if key in row} for row in csv_reader]

# Write the CSV data to a JSON format
with open('Scarlet_4_xxxl.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Write the CSV data to a text file in a JSON-like format
with open('RaidCalc.txt', 'w') as txt_file:
    for row in data:
        txt_file.write('{\n')
        for key, value in row.items():
            txt_file.write(f'  "{key}": "{value}",\n')
        txt_file.write('}\n')