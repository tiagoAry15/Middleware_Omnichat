from firebaseFolder.firebaseConnection import FirebaseConnection


class FirebaseUser:
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        self.firebaseConnection = inputFirebaseConnection
        self.firebaseConnection.changeDatabaseConnection("users")

    def getAllUsers(self):
        return self.firebaseConnection.readData()

    def existingUser(self, inputUserData: dict) -> bool:  # sourcery skip: use-any, use-next
        allUsers = self.getAllUsers()
        for uniqueId, userData in allUsers.items():
            if userData["email"] == inputUserData["email"]:
                return True
        return False

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


def __main():
    fc = FirebaseConnection()
    fu = FirebaseUser(fc)
    q = fu.createUser({"email": "user@example.com", "password": "password"})
    return


if __name__ == '__main__':
    __main()
