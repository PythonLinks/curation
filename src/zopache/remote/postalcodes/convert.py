import json
from slugify import slugify

def createStates():
    new = {}    
    # Open and read the JSON file
    with open('states.json', 'r') as file:
        states= json.load(file)
        for key, value in states.items():
               new[key.lower()] = slugify(value)
    result = json.dumps (new, indent = 2)
    print (result)

if __name__ == "__main__":    
    createStates()


