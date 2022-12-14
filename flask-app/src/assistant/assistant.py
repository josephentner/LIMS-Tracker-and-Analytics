from flask import Blueprint, request, jsonify, make_response
import json
from src import db

assistant = Blueprint('assistant', __name__)

# Helper function mapping experiment number to id in database
def get_exp_dict(cursor):
    query = '''
        SELECT exp_num, id
        FROM experiment
    '''
    cursor.execute(query)
    result = cursor.fetchall()

    return {row[0]: row[1] for row in result}


# Insert new result into desired table
@assistant.route('/result', methods=['POST'])
def add_result():

    # first map experiment num to id
    connection = db.connect()
    cursor = connection.cursor()
    exp_dict = get_exp_dict(cursor)

    # get data from POST request and add it into SQL INSERT query
    table = request.form['table']
    exp_id = exp_dict[request.form['expNum']]
    trial_num = request.form['trialNum']
    sql = f'INSERT INTO {table} VALUES ({exp_id}, {trial_num}, '
    for result in ['result1', 'result2', 'result3', 'result4']:
        if request.form[result] != '':
            sql += f'{request.form[result]}, '
    sql = sql[:-2]
    sql += ');'

    # execute INSERT query
    cursor.execute(sql)
    connection.commit()

    return '<h1>Success!</h1>'
