import json
from mtgsdk import Card

def load_precon(filename):
    file = open(filename, 'r')
    raw_text = file.readlines()
    decklist = []
    for line in raw_text:
        index = line.index(' ')
        count = int(line[:index])
        name = line[index+1:-1]
        decklist.append({'name': name, 'count': count})
    file.close()
    return decklist

def load_library():
    file = open("card_list.txt", 'r')
    raw_text = file.readlines()
    library = []
    for line in raw_text:
        library.append(line[:-1])
    return library

def load_list(path):
    file = open(path, "r")
    raw_text = file.readlines()
    new_list = []
    for line in raw_text:
        new_list.append(line[:-1])
    return new_list


def find_unowned(decklist, library):
    not_owned = []
    for card in decklist:
        if card['name'] not in library:
            not_owned.append(card['name'])
    return not_owned

def add_to_lib(decklist, library):
    for card in decklist:
        if card['name'] not in ['Swamp', 'Mountain', 'Island', 'Forest', 'Plain']:
            library.append(card['name'])
    
def make_grouped_lib(library):
    grouped_lib = {}
    for card in library:
        if (card not in grouped_lib):
            grouped_lib[card] = {"count": 1}
        else:
            grouped_lib[card]["count"] += 1
    return grouped_lib

def get_card_data(card_name):
    res = Card.where(name=card_name).all()
    return res

def print_card(card):
    return json.dumps({
        "color_identity": card.color_identity,
        "colors": card.colors,
        "flavor": card.flavor,
        "mana_cost": card.mana_cost,
        "name": card.name,
        "number": card.number,
        "original_text": card.original_text,
        "original_type": card.original_type,
        "power": card.power,
        "rarity": card.rarity,
        "rulings": card.rulings,
        "set": card.set,
        "set_name": card.set_name,
        "source": card.source,
        "starter": card.starter,
        "subtypes": card.subtypes,
        "supertypes": card.supertypes,
        "text": card.text,
        "timeshifted": card.timeshifted,
        "toughness": card.toughness,
        "type": card.type,
        "types": card.types,
        "variations": card.variations,
        "watermark": card.watermark
    })

def save_all_cards(cards_obj):
    c_file = open('compendium.txt', 'a')
    for card_name in cards_obj:
        card = get_card_data(card_name)
        if card != None:
            c_file.write(card)
    c_file.close()

def get_card_data(card_name):
    versions = []
    try:
        versions = Card.where(name=card_name).all()
    except:
        print(f"Error occured while trying to find {card_name}")
        return None
    versions.sort(key=lambda x:x.number)
    if len(versions) == 0:
        print(f"No versions returned for card {card_name}")
        return None
    return print_card(versions[0])

