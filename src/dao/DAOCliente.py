import requests

class DAOCliente:
    BASE_URL = 'https://secure-kery-db-92806f36d1d8.herokuapp.com/cliente_users'

    def update_cliente(self, dni, data):
        user_update_response = requests.put(f"https://secure-kery-db-92806f36d1d8.herokuapp.com/users/{dni}", json=data)
        cliente_update_response = requests.put(f"{self.BASE_URL}/{dni}", json={'reserva': data['reserva']})
        return user_update_response.status_code == 200 and cliente_update_response.status_code == 200

    def delete_cliente(self, dni):
        cliente_delete_response = requests.delete(f"{self.BASE_URL}/{dni}")
        user_delete_response = requests.delete(f"https://secure-kery-db-92806f36d1d8.herokuapp.com/users/{dni}")
        return cliente_delete_response.status_code == 200 and user_delete_response.status_code == 200

    def get_cliente(self, dni):
        response = requests.get(f"{self.BASE_URL}/{dni}")
        if response.status_code == 200:
            return response.json()
        return None
