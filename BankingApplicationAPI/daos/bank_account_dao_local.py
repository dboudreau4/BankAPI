from typing import List

from daos.bank_account_dao import BankAccountDAO
from entities.bank_account import BankAccount
from entities.client import Client


class BankAccountDAOLocal(BankAccountDAO):
    account_number_maker = 0
    account_number_table = {}

    # def create_account(self, account: BankAccount, client: Client) -> BankAccount:
    #     BankAccountDAOLocal.account_number_maker += 1
    #     account.account_number = BankAccountDAOLocal.account_number_maker
    #     BankAccountDAOLocal.account_number_table[BankAccountDAOLocal.account_number_maker] = account
    #     account.client_id = client.client_id
    #     return account
    def create_account(self, account: BankAccount) -> BankAccount:
        BankAccountDAOLocal.account_number_maker += 1
        account.account_number = BankAccountDAOLocal.account_number_maker
        BankAccountDAOLocal.account_number_table[BankAccountDAOLocal.account_number_maker] = account
        return account

    def get_account(self, account_number: int) -> BankAccount:
        account = BankAccountDAOLocal.account_number_table[account_number]
        return account

    def get_all_accounts(self) -> List[BankAccount]:
        account_list = list(BankAccountDAOLocal.account_number_table.values())
        return account_list

    def update_account(self, account: BankAccount) -> BankAccount:
        BankAccountDAOLocal.account_number_table[account.account_number] = account
        return account

    def delete_account(self, account_number: int) -> bool:
        try:
            del BankAccountDAOLocal.account_number_table[account_number]
            return True
        except KeyError:
            return False
