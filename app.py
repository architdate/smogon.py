from flask import Flask, jsonify
from api.smogonapi import smogonapi

app = Flask(__name__)
app.register_blueprint(smogonapi, url_prefix = '/api/v1')

if __name__ == '__main__':
    app.run(debug=True)