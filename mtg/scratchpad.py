import json

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

