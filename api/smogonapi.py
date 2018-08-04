from flask import Blueprint, jsonify
from api.helper import *
from api.exceptions import *

smogonapi = Blueprint('smogonapi', __name__)

@smogonapi.route('/data/<generation>/<pokemon>')
def getDataNoForm(generation, pokemon):
    try:
        if pokemon.isdigit(): dictval = extractData(int(pokemon), int(generation))
        else: dictval = extractDataFromString(pokemon, int(generation))
        return jsonify(dictval)
    except:
        APIError("Report to @thecommondude")

@smogonapi.route('/data/<generation>/<pokemon>/<form>')
def getDataForm(generation, pokemon, form):
    try:
        formattedpkm = (int(form) + int(pokemon) * 10) /10
        dictval = extractData(formattedpkm, int(generation))
        return jsonify(dictval)
    except:
        APIError("Report to @thecommondude")