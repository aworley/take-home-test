# API for managing user/group records
# 
# Take Home Test project for Planet
# Aaron Worley
# 2022-05-19

from flask import Flask, jsonify, request
import json

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return "<html><body><p>Welcome to the User Records API</p></body></html>"

@app.route('/users', methods=['GET'])
def users_get():
    return jsonify({'message': 'Placeholder 1'})

@app.route('/users', methods=['POST'])
def users_post():
    return jsonify({'message': 'Placeholder 2'})

@app.route('/users', methods=['DELETE'])
def users_delete():
    return jsonify({'message': 'Placeholder 3'})

@app.route('/users', methods=['PUT'])
def users_put():
    return jsonify({'message': 'Placeholder 4'})

@app.route('/groups', methods=['GET'])
def groups_get():
    return jsonify({'message': 'Placeholder 5'})

@app.route('/groups', methods=['POST'])
def groups_post():
    return jsonify({'message': 'Placeholder 6'})

@app.route('/groups', methods=['PUT'])
def groups_put():
    return jsonify({'message': 'Placeholder 7'})

@app.route('/groups', methods=['DELETE'])
def groups_delete():
    return jsonify({'message': 'Placeholder 8'})

# Add a welcome message to the HTTP headers.
# Doesn't serve a purpose other than cosmetics.
@app.after_request
def add_header(response):
    response.headers['Server-Message'] = 'Welcome to the User Records API'
    return response

app.run()
