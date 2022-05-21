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
        abort(400) 
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

@app.route('/users/<url_userid>', methods=['PUT'])
def users_put(url_userid):
    updated_user = json.loads(request.data)
    db = TinyDB('users-table.json')
    db_query = Query()

    # Bail out if the userid in the url does not exist in the table.
    if not db.search(db_query.userid == url_userid):
        abort(404)

    # Bail out if a userid change is attempted but the requested 
    # new userid already exists in the table.
    if url_userid != updated_user['userid'] and db.search(db_query.userid == updated_user['userid']):
        abort(400) 
    
    # Save updated user record to the users table.
    # TODO: catch exceptions
    db.update(updated_user, db_query.userid == url_userid)
    return jsonify({'message': 'User updated'})

@app.route('/groups/<url_name>', methods=['GET'])
def groups_get(url_name):
    db0 = TinyDB('groups-table.json')
    db0_query = Query()
    # Bail out if an invalid group was requested
    if not db0.search(db0_query.name == url_name):
        abort(404)
    db1 = TinyDB('users-table.json')
    db1_query = Query()
    userids_list = []
    for user in db1:
        if url_name in user['groups']:
            userids_list.append(user['userid'])
    return jsonify(userids_list)

@app.route('/groups', methods=['POST'])
def groups_post():
    new_group = json.loads(request.data)
    db = TinyDB('groups-table.json')
    db_query = Query()

    # Bail out if the provided userid already exists in the table.
    if db.search(db_query.name == new_group['name']):
        abort(400) 
    # Add new user record to the users table.
    # TODO: catch exceptions
    if db.insert(new_group):
        return jsonify({'message': 'Group added'})
    else:
        abort(404)

@app.route('/groups/<url_name>', methods=['PUT'])
def groups_put(url_name):
    group_list = json.loads(request.data)
    db0 = TinyDB('groups-table.json')
    db0_query = Query()
    # Bail out if the group name in the url does not exist in the table.
    if not db0.search(db0_query.name == url_name):
        abort(404)
    # Bail out if there is an invalid userid in the provided list.
    db1 = TinyDB('users-table.json')
    db1_query = Query()
    for userid_value in group_list:
        if not db1.search(db1_query.userid == userid_value):
            abort(400)
    # Retrieve all user records. Add and remove group memberships
    # as needed.
    for user in db1:
        if user['userid'] in group_list and url_name not in user['groups']:
            user['groups'].append(url_name)
        if url_name in user['groups'] and user['userid'] not in group_list:
            user['groups'].remove(url_name)
        db1.update(user, db1_query.userid == user['userid'])
    return jsonify({'message': 'Group updated'})

@app.route('/groups/<url_name>', methods=['DELETE'])
def groups_delete(url_name):
    db0 = TinyDB('groups-table.json')
    db0_query = Query()
    # Bail out if an invalid group was requested
    if not db0.search(db0_query.name == url_name):
        abort(404)
    db1 = TinyDB('users-table.json')
    db1_query = Query()
    userids_list = []
    for user in db1:
        if url_name in user['groups']:
            user['groups'].remove(url_name)
            db1.update(user, db1_query.userid == user['userid'])
    # TODO: catch exceptions    
    db0.remove(db0_query.name == url_name)
    return jsonify({'message': 'Group deleted'})

@app.route('/reset_test_data', methods=['GET'])
def reset_test_data():
    # Warning: this section empties both database tables and replaces existing
    # data with sample data.
    db0 = TinyDB('users-table.json')
    db0.truncate()
    db0.insert({"first_name": "Joe", "last_name": "Smith", "userid": "jsmith", "groups": ["admins", "users"]})
    db0.insert({"first_name": "Jane", "last_name": "Saito", "userid": "jsaito", "groups": ["admins", "users"]})
    db0.insert({"first_name": "Juan", "last_name": "Santiago", "userid": "jsantiago", "groups": ["admins"]})
    db0.insert({"first_name": "Janet", "last_name": "Simmons", "userid": "jsimmons", "groups": ["users"]})
    db1 = TinyDB('groups-table.json')
    db1.truncate()
    db1.insert({"name": "admins"})
    db1.insert({"name": "users"})
    return jsonify({'message': 'All data purged and test data added'})

# Add a welcome message to the HTTP headers.
# Doesn't serve a purpose other than cosmetics.
@app.after_request
def add_header(response):
    response.headers['Server-Message'] = 'Welcome to the User Records API'
    return response

app.run()
