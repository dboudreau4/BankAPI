from abc import ABC, abstractmethod
from typing import List

from entities.bank_account import BankAccount
from entities.client import Client


class BankAccountDAO(ABC):

    @abstractmethod
    def create_account(self, account: BankAccount) -> BankAccount:
        pass

    @abstractmethod
    def get_account(self, account_number: int) -> BankAccount:
        pass

    @abstractmethod
    def get_all_accounts(self) -> List[BankAccount]:
        pass

    @abstractmethod
    def update_account(self, account: BankAccount) -> BankAccount:
        pass

    @abstractmethod
    def delete_account(self, account_number: int) -> bool:
        pass
