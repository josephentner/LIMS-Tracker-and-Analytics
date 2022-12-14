from flask import Blueprint, request, jsonify, make_response
import json
from src import db


scientist = Blueprint('scientist', __name__)

# Helper function to map target code to id in the database
def get_target_dict(cursor):
    query = '''
        SELECT target_code, id
        FROM target
    '''
    cursor.execute(query)
    result = cursor.fetchall()

    return {row[0]: row[1] for row in result}

# Find which scientists/assistants conduct the most experiments
@scientist.route('/users', methods=['GET'])
def get_users():
    cursor = db.get_db().cursor()
    query = '''
    SELECT username AS `User`, count(*) AS `# Experiments Conducted`
    FROM experiment e JOIN users u ON e.creator_id = u.id
    GROUP BY u.username
    ORDER BY `# Experiments Conducted` DESC;
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add new protein
@scientist.route('/protein', methods=['POST'])
def add_protein():

    # create connection and map target num to id
    connection = db.connect()
    cursor = connection.cursor()
    target_dict = get_target_dict(cursor)

    # get data from POST request
    prot_name = request.form['protein']
    mol_weight = request.form['mol_weight']
    theoretical_pi = request.form['theoretical_pi']
    target_id = target_dict[request.form['target']]

    # turn into SQL INSERT statement
    sql = '''
        INSERT INTO protein (name, mol_weight, theoretical_pi, target_id)
        VALUES (%s, %s, %s, %s);
    '''
    values = (prot_name, mol_weight, theoretical_pi, target_id)
    
    # execute INSERT query
    cursor.execute(sql, values)
    connection.commit()

    return '<h1>Success!</h1>'