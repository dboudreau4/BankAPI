import logging

from flask import Flask, request, jsonify

from daos.bank_account_dao_local import BankAccountDAOLocal
from daos.bank_account_dao_postgres import BankAccountDAOPostgres
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from entities.bank_account import BankAccount
from entities.client import Client
from services.bank_account_service_impl import BankAccountServiceImpl
from services.client_service_impl import ClientServiceImpl

app = Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

client_dao = ClientDAOPostgres()
client_service = ClientServiceImpl(client_dao)

bank_account_dao = BankAccountDAOPostgres()
bank_account_service = BankAccountServiceImpl(bank_account_dao)


# create a client
# post with no accounts when created
@app.route("/clients", methods=["POST"])
def create_client():
    body = request.json
    client = Client(body["clientId"], body["firstName"], body["lastName"])
    client_service.add_client(client)
    return f"Created client with id {client.client_id}", 201


# get all clients
@app.route("/clients", methods=["GET"])
def get_all_clients():
    clients = client_service.retrieve_all_clients()
    json_clients = [c.as_json_dict() for c in clients]
    return jsonify(json_clients), 200


# get a client
@app.route("/clients/<client_id>", methods=["GET"])
def get_client_by_id(client_id: str):
    try:
        client = client_service.retrieve_client_by_id(int(client_id))
        return jsonify(client.as_json_dict())
    except TypeError:
        return f"The client with id {client_id} does not exist", 404


# update a client
@app.route("/clients/<client_id>", methods=["PUT"])
def update_client(client_id: str):
    body = request.json
    client = Client(body["clientId"], body["firstName"], body["lastName"])
    client.client_id = int(client_id)

    try:
        client_service.update_client(client)
        return "Updated successfully"
    except TypeError:
        return f"The client with id {client_id} does not exist", 404


# delete a client
@app.route("/clients/<client_id>", methods=["DELETE"])
def delete_client(client_id: str):
    try:
        client = client_service.retrieve_client_by_id(int(client_id))
        for a in client.client_accounts:
            bank_account_service.remove_account(a.account_number)
        client_service.remove_client(int(client_id))
        return "Deleted successfully", 205
    except TypeError:
        return f"The client with id {client_id} doesn't exist", 404


# ----------------Client + Bank Account combined methods--------------------#

# create new account for a given client
@app.route("/clients/<client_id>/accounts", methods=["POST"])
def create_client_account(client_id: str):
    body = request.json
    account = BankAccount(body["accountNumber"], body["accountType"], body["clientId"], body["balance"])

    try:
        client = client_service.retrieve_client_by_id(int(client_id))
        account.client_id = int(client_id)
        bank_account_service.add_account(account)
        client.client_accounts.append(account)
        return f"Successfully created account for client with id {client.client_id}", 201
    except TypeError:
        return f"The client with id {client_id} does not exist", 404


# get all accounts belonging to a client + endpoint below it
@app.route("/clients/<client_id>/accounts", methods=["GET"])
def get_all_client_accounts(client_id: str):
    try:
        client = client_service.retrieve_client_by_id(int(client_id))
    except TypeError:
        return f"The client with id {client_id} does not exist", 404

    maximum = request.args.get("amountLessThan")
    minimum = request.args.get("amountGreaterThan")
    client_accounts = []

    if maximum is not None and minimum is not None:
        client_accounts += bank_account_service.accounts_in_range(client_id, maximum, minimum)
        return f"Accounts with balances between 400 and 2000 belonging to client with id {client.client_id}: {client_accounts}", 201
    else:
        accounts = bank_account_service.retrieve_all_accounts()

        for a in accounts:
            if a.client_id == int(client_id):
                client_accounts.append(a.as_json_dict())

        return f"Accounts belonging to client with id {client.client_id}: {client_accounts}", 201


# get specific account for a specific client
@app.route("/clients/<client_id>/accounts/<account_number>", methods=["GET"])
def get_client_account(client_id: str, account_number: str):
    try:
        client = client_service.retrieve_client_by_id(int(client_id))
    except TypeError:
        return f"The client with id {client_id} does not exist", 404

    try:
        account = bank_account_service.retrieve_account_by_account_number(int(account_number))
    except TypeError:
        return f"The account {account_number} doesn't exist", 404

    if account.client_id == client.client_id:
        return f"{account.as_json_dict()}"


# update account for a client
@app.route("/clients/<client_id>/accounts/<account_number>", methods=["PUT"])
def update_client_account(client_id: str, account_number: str):
    body = request.json
    updated_account = BankAccount(body["accountNumber"], body["accountType"], body["clientId"], body["balance"])
    updated_account.account_number = int(account_number)
    updated_account.client_id = int(client_id)

    # Check if the client and account exist
    try:
        client = client_service.retrieve_client_by_id(int(client_id))
    except TypeError:
        return f"The client with id {client_id} does not exist", 404

    try:
        account = bank_account_service.retrieve_account_by_account_number(int(account_number))
    except TypeError:
        return f"The account {account_number} doesn't exist", 404

    if account.client_id == client.client_id:
        bank_account_service.update_account(updated_account)
        return "Updated successfully"


# delete a client account
@app.route("/clients/<client_id>/accounts/<account_number>", methods=["DELETE"])
def delete_client_account(client_id: str, account_number: str):
    try:
        client = client_service.retrieve_client_by_id(int(client_id))
    except TypeError:
        return f"The client with id {client_id} does not exist", 404

    try:
        account = bank_account_service.retrieve_account_by_account_number(int(account_number))
    except TypeError:
        return f"The account {account_number} doesn't exist", 404

    if account.client_id == client.client_id:
        bank_account_service.remove_account(account.account_number)
        return "Deleted successfully", 205


# withdraw/deposit for a client account
@app.route("/clients/<client_id>/accounts/<account_number>", methods=["PATCH"])
def withdraw_or_deposit(client_id: str, account_number: str):
    body = dict(request.json)
    transaction = ""
    amount = 0

    for k, v in body.items():
        transaction = k
        amount = v
    try:
        client = client_service.retrieve_client_by_id(int(client_id))
    except TypeError:
        return f"The client with id {client_id} does not exist", 404

    try:
        account = bank_account_service.retrieve_account_by_account_number(int(account_number))
    except TypeError:
        return f"The account {account_number} doesn't exist", 404

    if bank_account_service.transact(account, transaction, amount):
        bank_account_service.update_account(account)
        return "Balance updated", 205
    else:
        return "Insufficient funds", 422


@app.route("/clients/<client_id>/accounts/<account_1>/transfer/<account_2>", methods=["PATCH"])
def transfer(client_id: str, account_1: str, account_2: str):
    body = dict(request.json)
    amount = 0

    for k, v in body.items():
        amount = v

    try:
        client = client_service.retrieve_client_by_id(int(client_id))
    except TypeError:
        return f"The client with id {client_id} does not exist", 404

    try:
        acc_1 = bank_account_service.retrieve_account_by_account_number(int(account_1))
    except TypeError:
        return f"The account {account_1} doesn't exist", 404

    try:
        acc_2 = bank_account_service.retrieve_account_by_account_number(int(account_2))
    except TypeError:
        return f"The account {account_2} doesn't exist", 404

    if bank_account_service.transfer(acc_1, acc_2, amount):
        bank_account_service.update_account(acc_1)
        bank_account_service.update_account(acc_2)
        return "Transfer successful", 205
    else:
        return "Insufficient funds", 422


if __name__ == '__main__':
    app.run()
