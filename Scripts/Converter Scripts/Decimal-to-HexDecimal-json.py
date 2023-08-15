import json

# Open the JSON file
with open("Event-config.json", "r") as convertData:
    decimalData = json.load(convertData)

# Function to convert decimal values to hexadecimal values
def convert_dec_to_hex(data):
    if isinstance(data, dict):
        # If the value is a dictionary, recursively convert its values
        return {key: convert_dec_to_hex(value) for key, value in data.items()}
    elif isinstance(data, list):
        # If the value is a list, recursively convert its values
        return [convert_dec_to_hex(value) for value in data]
    elif isinstance(data, int):
        # If the value is a decimal integer, convert it to hexadecimal
        return hex(data)[2:].upper()
    else:
        # If the value is not a dictionary, list, or decimal integer, return it unchanged
        return data

# Convert decimal values to hexadecimal values
fileData = convert_dec_to_hex(decimalData)

# Write to a new file
## When it creates the data in the txt file other things will convert to to hex decimal aswell
## Im to lazy to try and figure out how to only convert only certain things from the json file 
## so it will just convert what ever it can.
with open("Event-config.txt", "w") as convertedData:
    json.dump(fileData, convertedData, indent=4)