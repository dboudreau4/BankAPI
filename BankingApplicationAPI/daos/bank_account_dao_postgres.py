from typing import List

from daos.bank_account_dao import BankAccountDAO
from entities.bank_account import BankAccount
from entities.client import Client
from utils.connection_util import connection


class BankAccountDAOPostgres(BankAccountDAO):
    # def create_account(self, account: BankAccount, client: Client) -> BankAccount:
    #     sql = """insert into account (account_type, c_id) values (%s, %s) returning account_number"""
    #     cursor = connection.cursor()
    #     cursor.execute(sql, (account.account_type, client.client_id))
    #     connection.commit()
    #     account_number = cursor.fetchone()[0]
    #     account.account_number = account_number
    #     return account
    def create_account(self, account: BankAccount) -> BankAccount:
        sql = """insert into account (account_type, c_id, balance) values (%s, %s, %s) returning account_number"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_type, account.client_id, account.balance))
        connection.commit()
        account_number = cursor.fetchone()[0]
        account.account_number = account_number
        return account

    def get_account(self, account_number: int) -> BankAccount:
        sql = """select * from account where account_number = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_number])
        record = cursor.fetchone()
        account = BankAccount(*record)
        return account

    def get_all_accounts(self) -> List[BankAccount]:
        sql = """select * from account"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        account_list = []
        for record in records:
            account_list.append(BankAccount(*record))
        return account_list

    def update_account(self, account: BankAccount) -> BankAccount:
        sql = """update account set account_type=%s, c_id=%s, balance=%s where account_number =%s"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.account_type, account.client_id, account.balance, account.account_number))
        connection.commit()
        return account

    def delete_account(self, account_number: int) -> bool:
        sql = """delete from account where account_number = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_number])
        connection.commit()
        return True
