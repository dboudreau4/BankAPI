class BankAccount:

    def __init__(self, account_number: int, account_type: str, client_id: int, balance: int):

        self.account_number = account_number
        self.balance = balance
        self.client_id = client_id

        try:
            acc = account_type.lower()
            if acc == "checking" or acc == "savings":
                self.account_type = acc
            else:
                raise ValueError("Account type must be checking or savings")
        except ValueError as e:
            print(e)

    def __str__(self):
        return f"{self.account_type}: {self.account_number}"

    def as_json_dict(self):
        return {
            "accountNumber": self.account_number,
            "accountType": self.account_type,
            "clientId": self.client_id,
            "balance": self.balance
        }
