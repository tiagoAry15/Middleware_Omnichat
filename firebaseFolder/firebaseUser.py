from dialogFlowSession import singleton, update_connection_decorator
from firebaseFolder.firebaseConnection import FirebaseConnection


@singleton
class FirebaseUser:
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        self.firebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("users")

    def __getattribute__(self, name):
        if name == "updateConnection":
            return object.__getattribute__(self, name)

        attr = super().__getattribute__(name)
        if callable(attr) and not name.startswith("__"):
            def wrapper(*args, **kwargs):
                self.updateConnection()
                return attr(*args, **kwargs)

            return wrapper
        return attr

    def getAllUsers(self):
        return self.firebaseConnection.readData()

    def getUniqueIdByPhoneNumber(self, phoneNumber: str) -> str or None:
        # sourcery skip: use-next
        allUsers = self.getAllUsers()
        if allUsers is None:
            return None
        for uniqueId, userData in allUsers.items():
            if userData["phoneNumber"] == phoneNumber:
                return uniqueId
        return None

    def existingUser(self, inputUserData: dict) -> bool:
        uniqueId = self.getUniqueIdByPhoneNumber(inputUserData["phoneNumber"])
        return uniqueId is not None

    def createUser(self, userData: dict) -> bool:
        existingUser = self.existingUser(userData)
        return (
            False if existingUser
            else self.firebaseConnection.writeData(data=userData)
        )

    def updateUser(self, userData: dict) -> bool:
        existingUser = self.existingUser(userData)
        return (
            self.firebaseConnection.overWriteData(data=userData)
            if existingUser
            else False
        )

    def deleteUser(self, userData: dict) -> bool:
        existingUser = self.existingUser(userData)
        return (
            self.firebaseConnection.deleteData(data=userData)
            if existingUser
            else False
        )


def __createDummyUsers():
    fc = FirebaseConnection()
    fu = FirebaseUser(fc)
    dummyPot = [{"phoneNumber": "+558597648593", "name": "Pedro"},
                {"phoneNumber": "+558576481232", "name": "Ana Oliveira"},
                {"phoneNumber": "+558549854871", "name": "Carolina Lima"}]
    for user in dummyPot:
        fu.createUser(user)


def __main():
    __createDummyUsers()
    # fc = FirebaseConnection()
    # fu = FirebaseUser(fc)
    # print(fu.existingUser({"phoneNumber": "+558597648593"}))
    # fu.deleteUser({"email": "user@example.com", "password": "password"})
    return


if __name__ == '__main__':
    __main()
