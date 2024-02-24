from flask import Blueprint, jsonify
from app.db_connection import create_connection
from app.auth import auth

bicimad_bp = Blueprint('bicimad_bp', __name__)


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