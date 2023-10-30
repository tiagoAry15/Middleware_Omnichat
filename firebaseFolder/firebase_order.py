import datetime

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from utils.decorators.singleton_decorator import singleton


@singleton
class FirebaseOrder(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("orders")

    def getAllOrders(self):
        return self.firebaseConnection.readData()

    def createOrder(self, order_data):
        now = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S_%f")[:-3]
        return self.firebaseConnection.writeData(path=now, data=order_data)

    def getOrder(self, order_unique_id: str):
        return self.firebaseConnection.getValue(order_unique_id)

    def updateOrder(self, order_unique_id: str, order_data: dict):
        order = self.getOrder(order_unique_id)
        for key in order_data.keys():
            order[key] = order_data[key]
        return self.firebaseConnection.setValue(order_unique_id, order)

    def deleteOrder(self, order_unique_id: str):
        return self.firebaseConnection.deleteData(order_unique_id)


def __main():
    fc = FirebaseConnection()
    fo = FirebaseOrder(fc)
    # dummy_dict = {'address': 'Rua da Paz 1428',
    #               'communication': 'joao@example.com',
    #               'customerName': 'João',
    #               'observation': 'None',
    #               'pizzaName': 'Calabresa',
    #               'platform': 'Instagram',
    #               'status': 'Em preparação',
    #               'timestamp': '2023-10-23 09:03:16.508'}
    # fo.createOrder(dummy_dict)
    # fo.updateOrder("29_Oct_2023_22_20_43_518", {"customerName": "Bill"})
    # fo.deleteOrder("29_Oct_2023_22_20_43_518")
    return


if __name__ == "__main__":
    __main()
