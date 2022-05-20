# API for managing user/group records
# 
# Take Home Test project for Planet
# Aaron Worley
# 2022-05-19

from flask import Flask, jsonify, request, abort
import json
from tinydb import TinyDB, Query

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return "<html><body><p>Welcome to the User Records API</p></body></html>"

@app.route('/users', methods=['GET'])
def users_get():
    db = TinyDB('user-records-db.json')
    users_table = db.table('users')
    Users_query = Query()
    search_results = users_table.search(Users_query.user_id == request.args.get('user_id'))

    if search_results:
        return jsonify(search_results)
    else:
        abort(404)

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
    db = TinyDB('user-records-db.json')
    groups_table = db.table('groups')
    Groups_query = Query()
    search_results = groups_table.search(Groups_query.group_name == request.args.get('group_name'))

    if search_results:
        return jsonify(search_results)
    else:
        abort(404)

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
