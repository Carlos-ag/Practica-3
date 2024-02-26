# http://127.0.0.1:5000/api/v2/available-dates

from flask import Blueprint, jsonify
from app.db_connection import create_connection
from app.auth import auth

bicimad_bp = Blueprint('bicimad_bp', __name__)

def adapt_query_to_authenitfication(query):
    if auth.current_user() == 'guest':
        query += " LIMIT 10"
    return query


# 1.
@bicimad_bp.route('/available-dates', methods=['GET'])
@auth.login_required
def get_available_dates():
    '''
    Obtenemos todas las fechas disponibles en la base de datos
    '''
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT DISTINCT fecha FROM bicimad"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    dates = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(dates)




# 2.
@bicimad_bp.route('/origin-stations', methods=['GET'])
@auth.login_required
def get_origin_stations():
    '''
    Obtenemos todas las estaciones de origen disponibles en la base de datos
    '''
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT DISTINCT idunplug_station FROM bicimad"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    stations = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify([station[0] for station in stations])

# 3.
@bicimad_bp.route('/destination-stations', methods=['GET'])
@auth.login_required
def get_destination_stations():
    '''
    Obtenemos todas las estaciones de destino disponibles en la base de datos
    '''
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT DISTINCT idplug_station FROM bicimad"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    stations = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify([station[0] for station in stations])

# 4.
@bicimad_bp.route('/movements/<date>', methods=['GET'])
@auth.login_required
def get_movements_by_date(date):
    '''
    Obtenemos todos los movimientos de una fecha concreta
    '''
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM bicimad WHERE fecha='{date}'"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    movements = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(movements)

# 5.
@bicimad_bp.route('/movements/<date>/origin/<origin_station>', methods=['GET'])
@auth.login_required
def get_movements_by_origin(date, origin_station):
    '''
    Obtenemos todos los movimientos de una fecha concreta y una estación de origen concreta
    '''
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM bicimad WHERE fecha='{date}' AND idunplug_station={origin_station}"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    movements = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(movements)

# 6.
@bicimad_bp.route('/movements/<date>/destination/<destination_station>', methods=['GET'])
@auth.login_required
def get_movements_by_destination(date, destination_station):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM bicimad WHERE fecha='{date}' AND idplug_station={destination_station}"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    movements = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(movements)

# 7.
@bicimad_bp.route('/movements/<date>/origin/<origin_station>/destination/<destination_station>', methods=['GET'])
@auth.login_required
def get_movements_by_origin_and_destination(date, origin_station, destination_station):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM bicimad WHERE fecha='{date}' AND idunplug_station={origin_station} AND idplug_station={destination_station}"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    movements = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(movements)

# 8.
@bicimad_bp.route('/movements/<date>/origin/<origin_station>/destination/<destination_station>/duration/<condition>/<value>', methods=['GET'])
@auth.login_required
def get_movements_by_conditions(date, origin_station, destination_station, condition, value):
    connection = create_connection()
    cursor = connection.cursor()
    operator = '>' if condition == 'greater' else '<'
    query = f"SELECT * FROM bicimad WHERE fecha='{date}' AND idunplug_station={origin_station} AND idplug_station={destination_station} AND travel_time {operator} {value}"
    query = adapt_query_to_authenitfication(query)
    cursor.execute(query)
    movements = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(movements)

# 9.
@bicimad_bp.route('/add-movement', methods=['POST'])
@auth.login_required
def add_movement():
    '''
    Añadimos un nuevo movimiento a la base de datos
    '''
    data = request.json
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""INSERT INTO bicimad (fecha, ageRange, user_type, idunplug_station, idplug_station, idunplug_base, idplug_base, travel_time, Fichero) 
                VALUES ('{data['fecha']}', {data['ageRange']}, {data['user_type']}, {data['idunplug_station']}, 
                        {data['idplug_station']}, {data['idunplug_base']}, {data['idplug_base']}, {data['travel_time']}, '000000')"""
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Movement added successfully"}), 201


# 2.1
@bicimad_bp.route('/update-movement', methods=['PUT'])
@auth.login_required
def update_movement():
    data = request.json
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""UPDATE bicimad SET travel_time = {data['travel_time']}
                WHERE fecha = '{data['fecha']}' AND ageRange = {data['ageRange']} AND user_type = {data['user_type']}
                AND idunplug_station = {data['idunplug_station']} AND idplug_station = {data['idplug_station']}
                AND idunplug_base = {data['idunplug_base']} AND idplug_base = {data['idplug_base']}"""
    cursor.execute(query)
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"message": "No entry found to update"}), 404
    return jsonify({"message": "Movement updated successfully"}), 200



# 2.2
@bicimad_bp.route('/delete-movement', methods=['DELETE'])
@auth.login_required
def delete_movement():
    data = request.args
    conditions = " AND ".join([f"{key} = '{value}'" for key, value in data.items()])
    connection = create_connection()
    cursor = connection.cursor()
    query = f"DELETE FROM bicimad WHERE {conditions}"
    cursor.execute(query)
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"message": "No entries found to delete"}), 404
    return jsonify({"message": "Movements deleted successfully"}), 200
