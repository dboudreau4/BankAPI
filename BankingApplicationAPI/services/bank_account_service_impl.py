from typing import List

from daos.bank_account_dao import BankAccountDAO
from entities.bank_account import BankAccount
from entities.client import Client
from services.bank_account_service import BankAccountService


class BankAccountServiceImpl(BankAccountService):

    def __init__(self, bank_account_dao: BankAccountDAO):
        self.bank_account_dao = bank_account_dao

    # def add_account(self, account: BankAccount, client: Client):
    #     return self.bank_account_dao.create_account(account, client)
    def add_account(self, account: BankAccount):
        return self.bank_account_dao.create_account(account)

    def retrieve_all_accounts(self):
        return self.bank_account_dao.get_all_accounts()

    def retrieve_account_by_account_number(self, account_number: int):
        return self.bank_account_dao.get_account(account_number)

    def update_account(self, account: BankAccount):
        return self.bank_account_dao.update_account(account)

    def remove_account(self, account_number: int):
        return self.bank_account_dao.delete_account(account_number)

    def transact(self, account: BankAccount, transaction: str, amount: float) -> bool:
        if transaction == "deposit":
            account.balance += amount
            return True
        if transaction == "withdraw" and account.balance - amount >= 0:
            account.balance -= amount
            return True
        else:
            return False

    def transfer(self, account_1: BankAccount, account_2: BankAccount, amount: float) -> bool:
        if account_1.balance - amount >= 0:
            account_1.balance -= amount
            account_2.balance += amount
            return True
        else:
            return False

    def accounts_in_range(self, client_id: str, maximum: str, minimum: str) -> List[BankAccount]:
        accounts = self.bank_account_dao.get_all_accounts()
        client_accounts = []
        for a in accounts:
            if a.client_id == int(client_id):
                if int(minimum) <= a.balance <= int(maximum):
                    client_accounts.append(a.as_json_dict())
        return client_accounts




