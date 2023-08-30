from flask import Flask, request, jsonify
from config import Config
from .database import DatabaseConnectionSales
import pdb

def init_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)


    # Ejercicio 1.1
    @app.route('/customer/<int:customer_id>', methods = ['GET'])
    def get_customer(customer_id):
        query = 'SELECT customer_id, first_name, last_name, phone, email, street, city, state, zip_code FROM sales.customers WHERE customer_id = %s;'
        params = (customer_id,)
        result = DatabaseConnectionSales.fetch_one(query, params)
        if result is not None:
            return {
                'id': result[0],
                'nombre': result[1],
                'apellido': result[2],
                'email': result[4],
                'telefono': result[3],
                'calle': result[5],
                'ciudad': result[6],
                'provincia': result[7],
                'codigo_postal': result[8]
            }, 200
        return {'msg': 'No se encontró el actor'}, 404

    # Ejercicio 1.2
   
    @app.route('/customers', methods = ['GET'])
    def get_customers():
        query = 'SELECT customer_id, first_name, last_name, phone, email, street, city, state, zip_code FROM sales.customers;'
        results = DatabaseConnectionSales.fetch_all(query)
        customers = []
        contador = 0
        for result in results:
            customers.append({
                'id': result[0],
                'nombre': result[1],
                'apellido': result[2],
                'email': result[4],
                'telefono': result[3],
                'calle': result[5],
                'ciudad': result[6],
                'provincia': result[7],
                'codigo_postal': result[8]
            })
            contador += 1
        return {'clientes': customers, 'total': contador}, 200
    #ejercicio 1.2 bis
    @app.route('/customers1', methods=['GET'])
    def get_customers1():
        state = request.args.get('state')

        if state:
            query = 'SELECT customer_id, first_name, last_name, phone, email, street, city, state, zip_code FROM sales.customers WHERE state = %s;'
            params = (state,)
        else:
            query = 'SELECT customer_id, first_name, last_name, phone, email, street, city, state, zip_code FROM sales.customers;'
            params = None

        results = DatabaseConnectionSales.fetch_all(query, params)
        customers = []
        contador = 0
        for result in results:
            customer = {
                'id': result[0],
                'nombre': result[1],
                'apellido': result[2],
                'email': result[4],
                'telefono': result[3],
                'calle': result[5],
                'ciudad': result[6],
                'provincia': result[7],
                'codigo_postal': result[8]
            }
            customers.append(customer)
            contador += 1

        response = {'clientes': customers, 'total': contador}
        return jsonify(response), 200
        




    # Ejercicio 1.3
    # Cambiar a POST no debe ser con get es pon post
    @app.route('/customer_create', methods = ['GET'])
    def create_customer1():
        query = 'INSERT INTO sales.customers (first_name, last_name, phone, email, street, city, state, zip_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
        params = (
                request.args.get('first_name', ''),
                request.args.get('last_name', ''),
                request.args.get('phone', ''), 
                request.args.get('email', ''),
                request.args.get('street', ''),
                request.args.get('city', ''),
                request.args.get('state', ''),
                request.args.get('zip_code', '')
                )
        DatabaseConnectionSales.execute_query(query, params)
        return {'msg': 'Actor creado con éxito'}, 201
    
    #Ejercicio 1.3 modificado
    # Ejercicio 1.3 tratando de hacerlo con post
    @app.route('/customers', methods=['POST'])
    def create_customer():
        data = request.get_json()

        # Verificar que los campos requeridos estén presentes en la solicitud
        required_fields = ['first_name', 'last_name', 'email', 'phone']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'El campo "{field}" es requerido'}), 400
        #pdb.set_trace()  
        # Obtener los datos del cliente desde la solicitud
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zip_code')

        # Insertar el nuevo cliente en la base de datos
        query = 'INSERT INTO sales.customers (first_name, last_name, email, phone, street, city, state, zip_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        params = (first_name, last_name, email, phone, street, city, state, zip_code)
        customer_id = DatabaseConnectionSales.execute_query(query, params)

        # Construir la respuesta
        response = {'customer_id': customer_id}
        return jsonify(response), 201

    

    # Ejercicio 1.4
    @app.route('/customer_update/<int:customer_id>', methods = ['PUT'])
    def update_customer(customer_id):
        
        first_name = request.args.get('first_name', None)
        last_name = request.args.get('last_name', None)
        email = request.args.get('email', None)
        phone = request.args.get('phone', None)
        street = request.args.get('street', None)
        city = request.args.get('city', None)
        state = request.args.get('state', None)
        zip_code = request.args.get('zip_code', None)
        
        modificar = []
        params = []

        if first_name:
            modificar.append('first_name = %s')
            params.append(first_name)
        if last_name:
            modificar.append('last_name = %s')
            params.append(last_name)
        if email:
            modificar.append('email = %s')
            params.append(email)
        if phone:
            modificar.append('phone = %s')
            params.append(phone)
        if street:
            modificar.append('street = %s')
            params.append(street)
        if city:
            modificar.append('city = %s')
            params.append(city)
        if state:
            modificar.append('state = %s')
            params.append(state)
        if zip_code:
            modificar.append('zip_code = %s')
            params.append(zip_code)

        if not modificar:
            return jsonify({'msg': 'Nada para actualizar'}), 200

        query = f"UPDATE customers SET {', '.join(modificar)} WHERE customer_id = %s;"
        params.append(customer_id)

        DatabaseConnectionSales.execute_query(query, params)

        return jsonify({}), 200
        
        
        
    return app