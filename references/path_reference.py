import os
from pathlib import Path


def getMainFolderPath() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def getFirebaseSDKPath() -> Path:
    return getMainFolderPath() / 'firebaseFolder/firebase_sdk.json'


def getSpeisekartePath() -> Path:
    return getMainFolderPath() / "data/speisekarte.json"


def getEnvPath() -> Path:
    return getMainFolderPath() / '.env'


def getTokenJsonPath() -> Path:
    return getMainFolderPath() / 'tokens/token.json'


def getDialogflowJsonPath() -> str:
    return str(getMainFolderPath() / 'dialogflow.json')


def getWebdriverPath() -> Path:
    return getMainFolderPath() / 'webscrapping/geckodriver.exe'


def getFirebaseCacheFilesPath() -> Path:
    return getMainFolderPath() / 'firebaseCache/cache_files'


def __main():
    sdkFile = getDialogflowJsonPath()
    existingSdkFile = sdkFile.exists()
    print(existingSdkFile)
    return existingSdkFile


if __name__ == '__main__':
    __main()
