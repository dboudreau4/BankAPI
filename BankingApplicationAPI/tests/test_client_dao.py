from daos.client_dao import ClientDAO
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from entities.bank_account import BankAccount
from entities.client import Client

client_dao: ClientDAO = ClientDAOPostgres()
#account1 = BankAccount(12345, "checking")
#account2 = BankAccount(67890, "savings")
#test_client = Client(0, "David", "Boudreau", account1, account2)
test_client = Client(0, "David", "Boudreau")


def test_create_client():
    client_dao.create_client(test_client)
    assert test_client.client_id != 0


def test_get_client():
    client = client_dao.get_client(test_client.client_id)
    assert test_client.first_name == client.first_name and test_client.last_name == client.last_name


def test_get_all_clients():
    client1 = Client(0, "Jane", "Doe")
    client2 = Client(0, "John", "Smith")
    client_dao.create_client(client1)
    client_dao.create_client(client2)
    clients = client_dao.get_all_clients()
    assert len(clients) >= 2


def test_update_client():
    test_client.last_name = "Jones"
    updated_client = client_dao.update_client(test_client)
    assert updated_client.last_name == test_client.last_name


def test_delete_client():
    result = client_dao.delete_client(test_client.client_id)
    assert result
