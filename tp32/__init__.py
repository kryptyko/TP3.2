from flask import Flask, request, jsonify
from config import Config
from .database import DatabaseConnectionSales
from .database import DatabaseConnectionproduction
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
   
    
    
    @app.route('/customers', methods=['GET'])
    def get_customers():
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

        # for field in required_fields:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Los campos {", ".join(missing_fields)} son requeridos'}), 400

           
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

        # Construir la respuesta mostrando el customerid
        response = {'customer_id': customer_id}
        return jsonify({}), 201 # como pide que el return sea vacio lo dejamos vacio

    

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
        

    #Ejercicio 1.5
    @app.route('/customers/<int:customer_id>', methods=['DELETE'])
    def delete_customer(customer_id):
        # Verificar que el cliente exista en la base de datos
        customer = DatabaseConnectionSales.fetch_one("SELECT * FROM customers WHERE id = %s", (customer_id,))
        if not customer:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        # Eliminar el cliente de la base de datos
        query = "DELETE FROM customers WHERE id = %s"
        params = (customer_id,)
        DatabaseConnectionSales.execute_query(query, params)

        return jsonify({}), 204
        




    #EJERCICIO 2.1.1
    @app.route('/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        # Obtener el producto de la base de datos
        query = """
            SELECT p.product_id, p.product_name, b.brand_id, b.brand_name, c.category_id, c.category_name, p.model_year, p.list_price
            FROM products AS p
            JOIN brands AS b ON p.brand_id = b.brand_id
            JOIN categories AS c ON p.category_id = c.category_id
            WHERE p.product_id = %s
        """
        params = (product_id,)
        product = DatabaseConnectionproduction.fetch_one(query, params)
        if not product:
            return jsonify({'error': 'Producto no encontrado'}), 404

        # Construir la respuesta
        response = {
            'product_id': product[0],
            'product_name': product[1],
            'brand': {
                'brand_id': product[2],
                'brand_name': product[3]
            },
            'category': {
                'category_id': product[4],
                'category_name': product[5]
            },
            'model_year': product[6],
            'list_price': product[7]
        }

        return jsonify(response), 200  

    #Ejercicio 2.1.2
    # 
    @app.route('/products', methods=['GET'])
    def get_products():
        # Obtener los parámetros de consulta opcionales
        brand_id = request.args.get('brand_id')
        category_id = request.args.get('category_id')

        # Construir la consulta SQL base
        query = """
            SELECT p.product_id, p.product_name, b.brand_id, b.brand_name, c.category_id, c.category_name, p.model_year, p.list_price
            FROM products AS p
            JOIN brands AS b ON p.brand_id = b.brand_id
            JOIN categories AS c ON p.category_id = c.category_id
        """

        # Agregar filtros según los parámetros proporcionados
        params = ()
        if brand_id:
            query += " WHERE p.brand_id = %s"
            params += (brand_id,)
        if category_id:
            if not brand_id:
                query += " WHERE"
            else:
                query += " AND"
            query += " p.category_id = %s"
            params += (category_id,)

        # Obtener el listado de productos de la base de datos
        products = DatabaseConnectionproduction.fetch_all(query, params)

        # Construir la respuesta
        response = {
            'products': [],
            'total': len(products)
        }

        for product in products:
            response['products'].append({
                'product_id': product[0],
                'product_name': product[1],
                'brand': {
                    'brand_id': product[2],
                    'brand_name': product[3]
                },
                'category': {
                    'category_id': product[4],
                    'category_name': product[5]
                },
                'model_year': product[6],
                'list_price': product[7]
            })

        return jsonify(response), 200  
    

    #Ejercicio 2.1.4
    @app.route('/products/<int:product_id>', methods=['PUT'])
    def update_product(product_id):
        # Verificar si el producto existe
        query = "SELECT * FROM products WHERE product_id = %s"
        params = (product_id,)
        product = DatabaseConnectionproduction.fetch_one(query, params)
        if not product:
            return jsonify({'error': 'Producto no encontrado'}), 404

        # Obtener los datos del cuerpo de la petición
        data = request.get_json()

        # Actualizar los campos del producto si se proporcionan en el cuerpo de la petición
        update_query = "UPDATE products SET"
        update_values = []
        update_params = []

        if 'product_name' in data:
            update_values.append("product_name = %s")
            update_params.append(data['product_name'])

        if 'brand_id' in data:
            update_values.append("brand_id = %s")
            update_params.append(data['brand_id'])

        if 'category_id' in data:
            update_values.append("category_id = %s")
            update_params.append(data['category_id'])

        if 'model_year' in data:
            update_values.append("model_year = %s")
            update_params.append(data['model_year'])

        if 'list_price' in data:
            update_values.append("list_price = %s")
            update_params.append(data['list_price'])

        if not update_values:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400

        update_query += " " + ", ".join(update_values)
        update_query += " WHERE product_id = %s"
        update_params.append(product_id)

        # Actualizar el producto en la base de datos
        DatabaseConnectionproduction.execute_query(update_query, update_params)

        return jsonify({}), 200


    #Ejercicio 2.1.5
    @app.route('/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        # Verificar si el producto existe
        query = "SELECT * FROM products WHERE product_id = %s"
        params = (product_id,)
        product = DatabaseConnectionSales.fetch_one(query, params)
        if not product:
            return jsonify({'error': 'Producto no encontrado'}), 404

        # Eliminar el producto de la base de datos
        delete_query = "DELETE FROM products WHERE product_id = %s"
        DatabaseConnectionSales.execute_query(delete_query, params)

        return jsonify({}), 204
    return app