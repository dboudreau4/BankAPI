from typing import List

from daos.client_dao import ClientDAO
from entities.client import Client


class ClientDAOLocal(ClientDAO):

    id_maker = 0
    client_table = {}

    def create_client(self, client: Client) -> Client:
        ClientDAOLocal.id_maker += 1
        client.client_id = ClientDAOLocal.id_maker
        ClientDAOLocal.client_table[ClientDAOLocal.id_maker] = client
        return client

    def get_client(self, client_id: int) -> Client:
        client = ClientDAOLocal.client_table[client_id]
        return client

    def get_all_clients(self) -> List[Client]:
        client_list = list(ClientDAOLocal.client_table.values())
        return client_list

    def update_client(self, client: Client) -> Client:
        ClientDAOLocal.client_table[client.client_id] = client
        return client

    def delete_client(self, client_id: int) -> bool:
        try:
            del ClientDAOLocal.client_table[client_id]
            return True
        except KeyError:
            return False



