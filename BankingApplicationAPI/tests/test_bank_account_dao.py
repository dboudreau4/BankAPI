from daos.bank_account_dao import BankAccountDAO
from daos.bank_account_dao_local import BankAccountDAOLocal
from daos.bank_account_dao_postgres import BankAccountDAOPostgres
from entities.bank_account import BankAccount
from entities.client import Client

# bank_account_dao: BankAccountDAO = BankAccountDAOLocal()
bank_account_dao: BankAccountDAO = BankAccountDAOPostgres()

test_account = BankAccount(0, "checking", 2, 0)


def test_create_account():
    bank_account_dao.create_account(test_account)
    assert test_account.account_number != 0


def test_get_account():
    account = bank_account_dao.get_account(test_account.account_number)
    assert test_account.account_number == account.account_number


def test_get_all_accounts():
    account1 = BankAccount(0, "checking", 2, 0)
    account2 = BankAccount(0, "savings", 2, 0)
    account3 = BankAccount(0, "savings", 2, 0)
    bank_account_dao.create_account(account1)
    bank_account_dao.create_account(account2)
    bank_account_dao.create_account(account3)
    accounts = bank_account_dao.get_all_accounts()
    assert len(accounts) >= 3


def test_update_account():
    test_account.account_type = "savings"
    updated_account = bank_account_dao.update_account(test_account)
    assert updated_account.account_type == test_account.account_type


def test_delete_account():
    result = bank_account_dao.delete_account(test_account.account_number)
    assert result
