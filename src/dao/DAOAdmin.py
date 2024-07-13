import requests

class DAOAdmin:
    BASE_URL = 'https://secure-kery-db-92806f36d1d8.herokuapp.com/admin_users'
    BASE_URL2 = 'https://secure-kery-db-92806f36d1d8.herokuapp.com'
    def update_admin(self, dni, data):
        print(f"Actualizando usuario con DNI: {dni}")
        user_update_response = requests.put(f"{self.BASE_URL2}/users/{dni}", json=data)
        print(f"Respuesta de actualización de usuario: {user_update_response.status_code}, {user_update_response.text}")

        admin_update_response = requests.put(f"{self.BASE_URL}/admin_users/{dni}", json={'codAdmin': data['codAdmin']})
        print(f"Respuesta de actualización de admin: {admin_update_response.status_code}, {admin_update_response.text}")

        return user_update_response.status_code == 200 and admin_update_response.status_code == 200

    def verify_admin_code(self, dni, admin_code):
        print(f"Verifying admin code for DNI={dni}, admin_code={admin_code}")
        response = requests.post(f"{self.BASE_URL}/verify", json={'dni': dni, 'codAdmin': admin_code})
        print(f"Response: {response.status_code}, {response.text}")
        return response.status_code == 200
    
    def delete_admin(self, dni):
        admin_delete_response = requests.delete(f"{self.BASE_URL}/{dni}")
        user_delete_response = requests.delete(f"https://secure-kery-db-92806f36d1d8.herokuapp.com/users/{dni}")
        return admin_delete_response.status_code == 200 and user_delete_response.status_code == 200

    def get_admin(self, dni):
        user_response = requests.get(f"https://secure-kery-db-92806f36d1d8.herokuapp.com/users/{dni}")
        admin_response = requests.get(f"{self.BASE_URL}/{dni}")
        
        if user_response.status_code == 200 and admin_response.status_code == 200:
            user_data = user_response.json()
            admin_data = admin_response.json()
            user_data['codAdmin'] = admin_data['codAdmin']
            return user_data
        return None
