from flask import Blueprint, request, jsonify, make_response
import json
from src import db

# Create analyst blueprint
analyst = Blueprint('analyst', __name__)

# Get all data related to thermostability assay
@analyst.route('/thermostability', methods=['GET'])
def get_thermostability():
    cursor = db.get_db().cursor()
    query = '''
    SELECT exp_num AS `EXP #`, trial_num AS `Trial #`, date_created AS `Date Created`, 
	    username AS creator, pb.name AS protein, target_code AS target, 
        onset_temp AS `Onset Temp`, midpoint_temp AS `Midpoint Temp`
    FROM thermostability t JOIN experiment e ON t.exp_id = e.id
        JOIN protein_batch pb ON e.batch_id = pb.id
        JOIN protein p ON pb.parent_id = p.id
        JOIN target tg ON p.target_id = tg.id
        JOIN users u ON e.creator_id = u.id
    ORDER BY e.date_created;
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

# Compare theoretical to experimental pI 
@analyst.route('/pi', methods=['GET'])
def get_pI():
    cursor = db.get_db().cursor()
    query = '''
    SELECT exp_num AS `EXP #`, trial_num AS `Trial #`, pb.name AS `Batch`,
        theoretical_pi AS `Theoretical pI`, experimental_pi AS `Experimental pI`
    FROM pi_analysis p JOIN experiment e ON p.exp_id = e.id
        JOIN protein_batch pb ON e.batch_id = pb.id
        JOIN protein pt ON pb.parent_id = pt.id
    ORDER BY e.date_created;
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

# Find which projects (targets) have proteins that successfully kill 
# the most cancer cells
@analyst.route('/lysis', methods=['GET'])
def get_lysis():
    cursor = db.get_db().cursor()
    query = '''
    SELECT target_code AS `Target`, avg(max_lysis) AS `Max Lysis`, avg(ec50) AS `Ec50`
    FROM cell_lysis c JOIN experiment e ON c.exp_id = e.id
        JOIN protein_batch pb ON e.batch_id = pb.id
        JOIN protein pt ON pb.parent_id = pt.id
        JOIN target tg ON pt.target_id = tg.id
    GROUP BY target_code;
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

# Find which projects (targets) have proteins that successfully bind 
# to the target cells
@analyst.route('/binding', methods=['GET'])
def get_binding():
    cursor = db.get_db().cursor()
    query = '''
    SELECT target_code AS `Target`, avg(max_expression) AS `Max Expression`, avg(ec50) AS `Ec50`
    FROM cell_binding c JOIN experiment e ON c.exp_id = e.id
        JOIN protein_batch pb ON e.batch_id = pb.id
        JOIN protein pt ON pb.parent_id = pt.id
        JOIN target tg ON pt.target_id = tg.id
    GROUP BY target_code;
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


# After averaging each batch, find the proteins with most hydrophobicity
@analyst.route('/hydrophobicity', methods=['GET'])
def get_hydrophobicity():
    cursor = db.get_db().cursor()
    query = '''
        SELECT p.name AS `Protein`, avg(retention_time) AS `Retention Time`
        FROM hydrophobicity h JOIN experiment e ON h.exp_id = e.id
            JOIN protein_batch pb ON e.batch_id = pb.id
            JOIN protein p ON pb.parent_id = p.id
        GROUP BY p.name
        ORDER BY min(p.id);
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
