import requests

class DAOVisitor:
    BASE_URL = 'https://secure-kery-db-92806f36d1d8.herokuapp.com/visitors'

    def create_visitor(self, data):
        response = requests.post(self.BASE_URL, json=data)
        return response.status_code == 201

    def update_visitor(self, dni, data):
        response = requests.put(f"{self.BASE_URL}/{dni}", json=data)
        return response.status_code == 200

    def delete_visitor(self, dni):
        response = requests.delete(f"{self.BASE_URL}/{dni}")
        return response.status_code == 200

    def list_visitors(self):
        response = requests.get(self.BASE_URL)
        if response.status_code == 200:
            return response.json()
        return None

    def get_visitor(self, dni):
        response = requests.get(f"{self.BASE_URL}/{dni}")
        if response.status_code == 200:
            return response.json()
        return None

    def get_visitors(self, dni_cliente):
        response = requests.get(f"{self.BASE_URL}/client/{dni_cliente}")
        if response.status_code == 200:
            return response.json()
        return None
