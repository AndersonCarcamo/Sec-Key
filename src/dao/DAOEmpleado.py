import requests

class DAOEmpleado:
    BASE_URL = 'https://secure-kery-db-92806f36d1d8.herokuapp.com/empleados'

    def create_empleado(self, data):
        response = requests.post(self.BASE_URL, json=data)
        return response.status_code == 201

    def update_empleado(self, codigo_empleado, data):
        response = requests.put(f"{self.BASE_URL}/{codigo_empleado}", json=data)
        return response.status_code == 200

    def delete_empleado(self, codigo_empleado):
        response = requests.delete(f"{self.BASE_URL}/{codigo_empleado}")
        return response.status_code == 200

    def list_empleados(self):
        response = requests.get(self.BASE_URL)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_empleado(self, codigo_empleado):
        response = requests.get(f"{self.BASE_URL}/{codigo_empleado}")
        if response.status_code == 200:
            return response.json()
        return None