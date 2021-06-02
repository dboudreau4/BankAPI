from abc import ABC, abstractmethod
from typing import List

from entities.bank_account import BankAccount
from entities.client import Client


class BankAccountService(ABC):

    @abstractmethod
    def add_account(self, account: BankAccount):
        pass

    @abstractmethod
    def retrieve_all_accounts(self):
        pass

    @abstractmethod
    def retrieve_account_by_account_number(self, account_number: int):
        pass

    @abstractmethod
    def update_account(self, account: BankAccount):
        pass

    @abstractmethod
    def remove_account(self, account_number: int):
        pass

    @abstractmethod
    def transact(self, account: BankAccount, transaction: str, amount: float) -> bool:
        pass

    @abstractmethod
    def transfer(self, account_1: BankAccount, account_2: BankAccount, amount: float) -> bool:
        pass

    @abstractmethod
    def accounts_in_range(self, client_id: str, maximum: str, minimum: str) -> List[BankAccount]:
        pass
