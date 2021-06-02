from unittest.mock import MagicMock

from daos.bank_account_dao_postgres import BankAccountDAOPostgres
from entities.bank_account import BankAccount
from services.bank_account_service import BankAccountService
from services.bank_account_service_impl import BankAccountServiceImpl

accounts = [BankAccount(0, "checking", 0, 0),
            BankAccount(0, "savings", 0, 0),
            BankAccount(0, "checking", 0, 0)]

mock_dao = BankAccountDAOPostgres()
mock_dao.get_all_accounts = MagicMock(return_value=accounts)
accounts = mock_dao.get_all_accounts()

bank_account_service: BankAccountService = BankAccountServiceImpl(mock_dao)


def test_transact():
    assert bank_account_service.transact(accounts[0], "deposit", 100)


def test_transfer():
    assert bank_account_service.transfer(accounts[0], accounts[1], 100)


def test_accounts_in_range():
    account_list = bank_account_service.accounts_in_range("0", "100", "50")
    assert len(account_list) == 1
