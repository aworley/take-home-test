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

@app.route('/users/<url_userid>', methods=['GET'])
def users_get(url_userid):
    db = TinyDB('users-table.json')
    db_query = Query()
    search_results = db.search(db_query.userid == url_userid)

    if search_results:
        return jsonify(search_results)
    else:
        abort(404)

@app.route('/users', methods=['POST'])
def users_post():
    new_user = json.loads(request.data)
    db = TinyDB('users-table.json')
    db_query = Query()

    # Bail out if the provided userid already exists in the table.
    if db.search(db_query.userid == new_user['userid']):
        abort(409) 
    # Add new user record to the users table.
    # TODO: catch exceptions
    if db.insert(new_user):
        return jsonify({'message': 'User added'})
    else:
        abort(404)

@app.route('/users/<url_userid>', methods=['DELETE'])
def users_delete(url_userid):
    db = TinyDB('users-table.json')
    db_query = Query()

    if db.remove(db_query.userid == url_userid):
        return jsonify({'message': 'User deleted'})
    else:
        abort(404)

@app.route('/users', methods=['PUT'])
def users_put():
    return jsonify({'message': 'Placeholder 4'})

@app.route('/groups/<url_name>', methods=['GET'])
def groups_get(url_name):
    db = TinyDB('groups-table.json')
    db_query = Query()
    search_results = db.search(db_query.name == url_name)

    if search_results:
        return jsonify(search_results)
    else:
        abort(404)

@app.route('/groups', methods=['POST'])
def groups_post():
    new_group = json.loads(request.data)
    db = TinyDB('groups-table.json')
    db_query = Query()

    # Bail out if the provided userid already exists in the table.
    if db.search(db_query.name == new_group['name']):
        abort(409) 
    # Add new user record to the users table.
    # TODO: catch exceptions
    if db.insert(new_group):
        return jsonify({'message': 'Group added'})
    else:
        abort(404)

@app.route('/groups', methods=['PUT'])
def groups_put():
    return jsonify({'message': 'Placeholder 7'})

@app.route('/groups/<url_name>', methods=['DELETE'])
def groups_delete(url_name):
    db = TinyDB('groups-table.json')
    db_query = Query()
    
    if db.remove(db_query.name == url_name):
        return jsonify({'message': 'Group deleted'})
    else:
        abort(404)

@app.route('/reset_test_data', methods=['GET'])
def reset_test_data():
    # Warning: this section empties both database tables and replaces existing
    # data with sample data.
    db0 = TinyDB('users-table.json')
    db0.truncate()
    db0.insert({"first_name": "Jane", "last_name": "Smith", "userid": "jsmith", "groups": ["admins"]})
    db1 = TinyDB('groups-table.json')
    db1.truncate()
    db1.insert({"name": "admins"})
    db1.insert({"name": "staff"})
    db1.insert({"name": "devops"})
    db1.insert({"name": "mgmt"})
    return jsonify({'message': 'All data purged and test data added'})

# Add a welcome message to the HTTP headers.
# Doesn't serve a purpose other than cosmetics.
@app.after_request
def add_header(response):
    response.headers['Server-Message'] = 'Welcome to the User Records API'
    return response

app.run()
