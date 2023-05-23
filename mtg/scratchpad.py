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
    