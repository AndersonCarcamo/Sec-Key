import pymysql

class DAOUser:
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", db="db_secure_place")

    def create_user(self, data):
        conn = self.connect()
        cursor = conn.cursor()
        
        politicas = data.get('politicas') == 'on'

        try:
            cursor.execute("""
                INSERT INTO users (dni, nombre, apellido, gmail, password, foto, politicas, isAdmin, isCliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (data['dni'], data['nombre'], data['apellido'], data['gmail'], data['password'], data['foto'], politicas, data.get('isAdmin', False), data.get('isCliente', False)))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def update_user(self, dni, data):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE users SET nombre = %s, apellido = %s, gmail = %s, password = %s, foto = %s, politicas = %s WHERE dni = %s
            """, (data['nombre'], data['apellido'], data['gmail'], data['password'], data['foto'], data['politicas'], dni))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

        
    def delete_user(self, dni):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM users WHERE dni = %s", (dni,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def list_users(self):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return [self.dict_from_row(row) for row in users]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_user(self, dni):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE dni = %s", (dni,))
            user = cursor.fetchone()
            return self.dict_from_row(user)
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def verify_user(self, gmail, password):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE gmail = %s AND password = %s", (gmail, password))
            user = cursor.fetchone()
            return self.dict_from_row(user) if user else None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def dict_from_row(self, row):
        if row is None:
            return None
        return {
            'dni': row[0],
            'nombre': row[1],
            'apellido': row[2],
            'gmail': row[3],
            'password': row[4],
            'foto': row[5],
            'politicas': row[6],
            'isAdmin': row[7],
            'isCliente': row[8]
        }
