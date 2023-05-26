import os
from pathlib import Path


def getMainFolderPath() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def getFirebaseSDKPath() -> Path:
    return getMainFolderPath() / 'firebaseFolder/firebase_sdk.json'


def getSpeisekartePath() -> Path:
    return getMainFolderPath() / "data/speisekarte.json"


def __main():
    sdkFile = getFirebaseSDKPath()
    existingSdkFile = sdkFile.exists()
    print(existingSdkFile)
    return existingSdkFile


if __name__ == '__main__':
    __main()
