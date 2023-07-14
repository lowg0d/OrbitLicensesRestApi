"""
checklinces = get the information by a license
checkuser = get the information by a user

delete license 
create license
edit license

regenerate license
license/user list
"""

data_base = ""
table = "orbit_licenses"

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)
mysql_connection = MySQL(app)

@app.route("/license_list", methods=['GET'])
def show_license_list():
    try:
        cursor = mysql_connection.connection.cursor()
        sql="SELECT id, user_id, license, creation_date FROM licenses"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        license_list = []
        for row in data:
            license_data = {'license_id':row[0],
                            'user_id':row[1],
                            'license':row[2],
                            'creation_date':row[3]}
            license_list.append(license_data)
        
        return jsonify({'license_list':license_list})
    
    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check_console"})

@app.route("/license/<_license>", methods=['GET'])
def get_lincese_info(_license):
    try:
        cursor = mysql_connection.connection.cursor()
        sql=f"SELECT id, user_id, license, creation_date FROM licenses WHERE license = {_license}"
        cursor.execute(sql)
        data = cursor.fetchone()
        
        if data != None:
            license_data = {'license_id':data[0],
                            'user_id':data[1],
                            'license':data[2],
                            'creation_date':data[3]}
            
            return jsonify({'license_list':license_data})

        else:
            return jsonify({'error': "not found"})
    
    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check_console"})

@app.route("/user/<_user_id>", methods=['GET'])
def get_user_info(_user_id):
    try:
        cursor = mysql_connection.connection.cursor()
        sql=f"SELECT id, user_id, license, creation_date FROM licenses WHERE user_id = {_user_id}"
        cursor.execute(sql)
        data = cursor.fetchone()
        
        if data != None:
            license_data = {'license_id':data[0],
                            'user_id':data[1],
                            'license':data[2],
                            'creation_date':data[3]}
            
            return jsonify({'license_list':license_data})

        else:
            return jsonify({'error': "not found"})
    
    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check_console"})

@app.route("/license/validate/<_license>", methods=['GET'])
def check_license(_license):
    try:
        cursor = mysql_connection.connection.cursor()
        if fetch_license(_license, cursor) == True:
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False})

    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check the console for more information."})

@app.route("/license", methods=['POST'])
def create_license():
    try:
        cursor = mysql_connection.connection.cursor()
        
        _license = request.json['license']
        if fetch_license(_license, cursor) != True:
            user_id = request.json['user_id']
        
        else:
            print("[ERROR]: License Already On The Database")
            return jsonify({'error': "license_duplicated"})
            
        if fetch_user_id(user_id, cursor) != True:
            creation_data = request.json['creation_date']
            
            sql=f"""INSERT INTO licenses (license, user_id, creation_date) VALUES ('{_license}','{user_id}','{creation_data}')"""
            cursor.execute(sql)
            
            mysql_connection.connection.commit()
            return jsonify({'success': True})
    
        else:
            print("[ERROR]: User License Limit Reached")
            return jsonify({'error': "user_max"})
    
    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check the console for more information."})

@app.route("/license/<_license>", methods=['DELETE'])
def delete_license(_license):
    try:
        cursor = mysql_connection.connection.cursor()
        if fetch_license(_license, cursor) != True:
            print("[ERROR]: License Already On The Database")
            return jsonify({'error': "license_not_found"})
        
        else:
            sql=f"""DELETE FROM licenses WHERE license='{_license}'"""
            cursor.execute(sql)
            
            mysql_connection.connection.commit()
            return jsonify({'success': True})
    
    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check the console for more information."})

@app.route("/license/<_license>", methods=['PUT'])
def update_license(_license):
    try:
        cursor = mysql_connection.connection.cursor()
        if fetch_license(_license, cursor) != True:
            print("[ERROR]: License Already On The Database")
            return jsonify({'error': "license_not_found"})
        
        else:
            new_license = request.json['license']
            new_user_id = request.json['user_id']
            
            sql=f"""UPDATE licenses SET license='{new_license}',user_id='{new_user_id}' WHERE license='{_license}'"""
            cursor.execute(sql)
            
            mysql_connection.connection.commit()
            return jsonify({'success': True})
    
    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check the console for more information."})

@app.route("/table/check", methods=['GET'])
def check_table():
    print("[AAAAAAAAAAAAAAAAAAAAAAAAA]")
    try:
        check_table()
        return jsonify({'exits': "True"})
    
    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check the console for more information."})

@app.route("/table/create", methods=['GET'])
def create_table():
    try:
        cursor = mysql_connection.connection.cursor()
        create_table(cursor)
        return jsonify({'done': True})

    except Exception as e:
        print("[ERROR]: " + str(e))
        return jsonify({'error': "check the console for more information."})


def fetch_license(_license, cursor):
    sql=f"SELECT user_id FROM licenses WHERE license='{_license}'"
    cursor.execute(sql)
    
    if cursor.fetchone():
        return True
    
    else:
        return False

def fetch_user_id(user_id, cursor):
    sql=f"SELECT user_id FROM licenses WHERE user_id='{user_id}'"
    cursor.execute(sql)
    
    if cursor.fetchone():
        return True
    
    else:
        return False

def not_found(error):
    return "<h1>👎</h1>"

def check_for_table():
    cursor = mysql_connection.connection.cursor()
    sql = f"SHOW TABLES LIKE 'licenses'"
    
    try:
        cursor.execute(sql)
        table_exits = cursor.fetchall()
    
    except:
        create_table(cursor)
    
def create_table(cursor):
    try:
        sql = f"CREATE TABLE licenses (id int AUTO_INCREMENT PRIMARY KEY, user varchar(80), user_id varchar(80), license varchar(100), creation_date varchar(80))"
        
        cursor.execute(sql)
        mysql_connection.connection.commit()
        
    except Exception as e:
        return e

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, not_found)    
    app.run(port=6969)
    check_for_table()