import requests
import json
import subprocess
import sys
from api.exceptions import *

def copy(s):
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(s.encode('utf-8'))
    else:
        raise Exception('Platform not supported')

def getSpeciesName(id):
    with open("data/smogonspecies.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    return content[id]

def getForms(species, generation):
    # Ignore Megas and totems as megastones are items and smogon does not care about totems
    # Generation 1
    if species <= 151:
        alola_species = [19, 26, 27, 28, 37, 38, 50, 51, 52, 53, 74, 75, 76, 88, 89, 103]
        if species == 25: return getFormsPikachu(generation)
        if generation < 7: return ['']
        if species in alola_species: return ['', 'Alola']
        return ['']
    # Generation 2:
    if species <= 251:
        if species == 172: return getFormsPichu(generation)
        if species == 201: return getFormsUnown(generation)
        return ['']
    # Generation 3:
    if species <= 386:
        if species == 351: return ['', 'Sunny', 'Rainy', 'Snowy']
        if species == 382: return ['', 'Primal']
        if species == 383: return ['', 'Primal']
        if species == 386: return ['', 'Attack', 'Defense', 'Speed']
        return ['']
    # Generation 4:
    if species <= 493:
        if species in [412, 413, 414]: return ['', 'Sandy', 'Trash']
        if species == 421: return ['', 'Sunshine']
        if species == 422: return ['', 'East']
        if species == 423: return ['', 'West']
        if species == 479: return ['', 'Heat', 'Wash', 'Frost', 'Fan', 'Mow']
        if species == 479: return ['', 'Origin'] 
        if species == 492: return ['', 'Sky']
        if species == 493: return ['', 'Fighting', 'Flying',  'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']
        return ['']
    # Generation 5
    if species <= 649:
        genies = [641, 642, 645]
        if species == 550: return ['', 'Blue-Striped']
        if species == 555: return ['', 'Zen']
        if species == 585: return [''] # No deerling forms? wtf smogon?
        if species == 586: return [''] # No deerling forms? wtf smogon?
        if species in genies: return ['', 'Therian']
        if species == 646: return ['', 'White', 'Black']
        if species == 647: return ['', 'Resolute']
        if species == 648: return ['', 'Pirouette']
        if species == 649: return ['', 'Douse', 'Shock', 'Burn', 'Chill']
        return ['']
    # Generation 6
    if species <= 721:
        if species == 720: return ['', 'Unbound']
        if species == 718: return ['', '10%', 'Complete'] #Zygardes
        return ['']
    # Generation 7
    else:
        if species == 741: return [''] #Oricorios
        if species == 745: return ['', 'Midnight', 'Dusk']
        if species == 773: return ['', 'Fighting', 'Flying',  'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']
        if species == 800: return ['', 'Dusk-Mane', 'Dawn-Wings'] # Necrozmas
        return ['']


def getFormsPikachu(generation):
    if generation == 6: return ['', 'Rockstar', 'Belle', 'Pop-Star', 'PhD', 'Libre', 'Cosplay']
    elif generation == 7: return ['', 'Original', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Partner']
    else: return ['']

def getFormsPichu(generation):
    if generation == 4: return ['', 'Spiky']
    return ['']

def getFormsUnown(generation):
    letterlist = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    extras = ['!', '?']
    if generation == 2: return letterlist
    else: return letterlist + extras

def createShowdownSet(data, species):
    j = data
    ability = j['abilities'][0]
    if 'items' in j.keys(): item = j['items'][0]
    else: item = None
    movelist = j['moveslots']
    filtermoves = []
    for i in movelist:
        filtermoves.append(i[0])
    nature = j['natures'][0]
    evdict = j['evconfigs'][0]
    if len(j['ivconfigs']) > 0: ivdict = j['ivconfigs'][0]
    else: ivdict = []
    result = ""
    if item != None:
        result += (species + " @ " + item + "\n")
    else: result += species + "\n"
    result += "Ability: " + ability + "\n"
    result += getEVIVString(evdict, False) + "\n"
    result += getEVIVString(ivdict, True) + "\n"
    result += nature + " Nature\n"
    for i in filtermoves:
        result += "- " + i + "\n"
    return result.strip()

def getEVIVString(evdict, iv):
    evs = [0, 0, 0, 0, 0, 0]
    if iv: evs = [31, 31, 31, 31, 31, 31]
    if evdict == []: evdict = {}
    if 'hp' in evdict.keys(): evs[0] = evdict['hp']
    if 'atk' in evdict.keys(): evs[1] = evdict['atk']
    if 'def' in evdict.keys(): evs[2] = evdict['def']
    if 'spa' in evdict.keys(): evs[3] = evdict['spa']
    if 'spd' in evdict.keys(): evs[4] = evdict['spd']
    if 'spe' in evdict.keys(): evs[5] = evdict['spe']
    startText = "EVs: "
    if iv: startText = "IVs: "
    return startText + str(evs[0]) + " HP / " + str(evs[1]) + " Atk / " + str(evs[2]) + " Def / " + str(evs[3]) + " SpA / " + str(evs[4]) + " SpD / " + str(evs[5]) + " Spe"

def extractData(pokemon, generation = 7):
    generation_codes = {'1': 'rb', '2': 'gs', '3': 'rs', '4': 'dp', '5': 'bw', '6': 'xy', '7': 'sm'}
    try:
        species = getSpeciesName(int(pokemon // 1))
    except:
        raise InvalidSpecies
    formIndex = int((pokemon % 1) * 10)
    try:
        form = getForms(int(pokemon // 1), generation)[formIndex]
    except:
        raise InvalidForm
    returnjson = {}
    if formIndex == 0: returnjson['url'] = "https://www.smogon.com/dex/{}/pokemon/{}/".format(generation_codes[str(generation)], species)
    else: returnjson['url'] = "https://www.smogon.com/dex/{}/pokemon/{}-{}/".format(generation_codes[str(generation)], species, form)
    returnjson['sets'] = [] # to include a json of format, title, description and showdownset
    r = requests.get(returnjson['url']).text
    jsonstring = r.split("<script")[1].split("</script>")[0].split("dexSettings = ")[1].strip()
    jsondata = json.loads(jsonstring)
    strategylist = jsondata['injectRpcs'][2][1]['strategies']
    for i in strategylist:
        meta = i['format']
        for j in i['movesets']:
            set_description = j['description']
            set_name = j['name']
            set_abilities = j['abilities']
            set_moves = j['moveslots']
            set_natures = j['natures']
            set_evs = j['evconfigs']
            set_ivs = j['ivconfigs']
            if 'items' in j.keys(): set_items = j['items']
            else: set_items = []
            if formIndex == 0: showdown_set = createShowdownSet(j, species)
            else: showdown_set = createShowdownSet(j, species + "-" + form)
            returnjson['sets'].append({'format': meta, 'name': set_name, 'description': set_description, 'abilities': set_abilities, 'moves': set_moves, 'natures': set_natures, 'evs': set_evs, 'ivs': set_ivs, 'showdown': showdown_set})
    return returnjson