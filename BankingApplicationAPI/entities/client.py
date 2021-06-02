class Client:

    def __init__(self, client_id: int, first_name: str, last_name: str):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.client_accounts = []

    def __str__(self):
        return f"Client id: {self.client_id}, Name: {self.first_name} {self.last_name}"

    def as_json_dict(self):
        return {
            "clientId": self.client_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "clientAccounts": str(self.client_accounts)
        }
