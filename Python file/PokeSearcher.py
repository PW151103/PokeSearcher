import requests
import os

pokemon= input("enter the pokemon name or id: ").lower()
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

response = requests.get(url)
if response.status_code == 200:
    data= response.json()
    print(f"Name: {data['name'].capitalize()}")

    types = [t['type']['name'] for t in data['types']]
    print(f"Type(s): {', '.join(types)}")
#add weakness,/ resistant code here
    from collections import defaultdict
    damage_multipliers = defaultdict(lambda: 1.0)
    for t in data['types']:
        type_url = t['type']['url']
        type_response = requests.get(type_url)
        if type_response.status_code == 200:
            type_data = type_response.json()
            dr = type_data['damage_relations']
            for damage in type_data['damage_relations']['double_damage_from']:
                damage_multipliers[damage['name']] *= 2
            for damage in type_data['damage_relations']['half_damage_from']:
                damage_multipliers[damage['name']] *= 0.5
            for damage in type_data['damage_relations']['no_damage_from']:
                damage_multipliers[damage['name']] *= 0
    x4, x2, x05, x0 = [], [], [], []
    for typ, mult in damage_multipliers.items():
        if mult == 4:
            x4.append(typ)
        elif mult == 2:
            x2.append(typ)
        elif mult == 0.5:
            x05.append(typ)
        elif mult == 0:
            x0.append(typ)
    print("weaknesses / resistances:")
    if x4:
        print(f"  x4: {', '.join(x4)}")
    if x2:
        print(f"  x2: {', '.join(x2)}")
    if x05:
        print(f"  x0.5: {', '.join(x05)}")
    if x0:
        print(f"  x0: {', '.join(x0)}")

    abilities_info = []
    for a in data['abilities']:
        ability_name = a['ability']['name']
        ability_url = a['ability']['url']
        ability_response = requests.get(ability_url)
        if ability_response.status_code == 200:
            ability_data= ability_response.json()
            effect_entries = ability_data['effect_entries']
            effect = ""
            for entry in effect_entries:
                if entry['language']['name'] == 'en':
                    effect = entry['effect']
                    break
            print(f"  {ability_name.title()}: {effect}")
        else:
            print(f"  {ability_name.title()}: No effect information available.")

    print("Stats:")
    for stat in data["stats"]:
        print(f"  {stat['stat']['name'].title()}: {stat['base_stat']}")
    
    filename = f"{pokemon}_info.txt"
    with open(filename, "w", encoding="utf-8") as f:
        
        #name
        f.write(f"Name: {data['name'].title()}\n\n")
        
        #types
        f.write(f"Type(s): {', '.join(t.title() for t in types)}\n")
        
        #weaknesses / resistances
        f.write("Weaknesses / Resistances:\n")
        if x4:
            f.write(f"  x4: {', '.join(t.title() for t in x4)}\n")
        if x2:
            f.write(f"  x2: {', '.join(t.title() for t in x2)}\n")
        if x05:
            f.write(f"  x0.5: {', '.join(t.title() for t in x05)}\n")
        if x0:
            f.write(f"  x0: {', '.join(t.title() for t in x0)}\n")
        
        #abilities
        f.write("Abilities:\n")
        for a in data['abilities']:
            ability_name = a['ability']['name']
            ability_url = a['ability']['url']
            ability_response = requests.get(ability_url)
            if ability_response.status_code == 200:
                ability_data= ability_response.json()
                effect_entries = ability_data['effect_entries']
                effect = ""
                for entry in effect_entries:
                    if entry['language']['name'] == 'en':
                        effect = entry['effect']
                        break
                f.write(f"  {ability_name.title()}: {effect}\n")
            else:
                f.write(f"  {ability_name.title()}: No effect information available.\n")
        
        #stats
        f.write("Stats:\n")
        for stat in data["stats"]:
            f.write(f"  {stat['stat']['name'].title()}: {stat['base_stat']}\n")
        os.startfile(filename)

else:    print("Pokemon not found. Please check the name or ID and try again.")

