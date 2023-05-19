import os
from pathlib import Path


def getMainFolderPath() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def getFirebaseSDKPath() -> Path:
    return getMainFolderPath() / 'firebaseFolder/firebase_sdk.json'


def __main():
    mainFolder = getFirebaseSDKPath()
    print(mainFolder)
    return mainFolder


if __name__ == '__main__':
    __main()
