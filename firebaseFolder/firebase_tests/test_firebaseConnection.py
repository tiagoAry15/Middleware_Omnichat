import os

import firebase_admin
import pytest
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv

from firebaseFolder.firebaseConnection import FirebaseConnection, getFirebaseCredentials
from firebaseFolder.firebase_tests.firebaseMock import MockedDbRef


class MockedFirebaseApp:
    pass


class MockedFirebaseCred:
    pass


@pytest.fixture
def firebase_connection() -> FirebaseConnection:
    load_dotenv()
    with patch('firebase_admin.initialize_app'), \
            patch('firebase_admin.credentials.Certificate'), \
            patch('firebase_admin.db.reference', return_value=MockedDbRef()):
        connection = FirebaseConnection()
    return connection


def test_readData(firebase_connection: FirebaseConnection):
    data = firebase_connection.readData("users")
    assert data == {'dummyData': 5}


def test_writeData(firebase_connection: FirebaseConnection):
    result = firebase_connection.writeData("users", {"testData": 10})
    assert result is True


def test_overWriteData(firebase_connection: FirebaseConnection):
    result = firebase_connection.overWriteData("users", {"testData": 10})
    assert result is True


def test_deleteData(firebase_connection: FirebaseConnection):
    with patch.object(firebase_connection, 'getUniqueIdByData') as mock_getUniqueId:
        mock_getUniqueId.return_value = 'test_key'
        result = firebase_connection.deleteData("users", {"testData": 10})
        assert result is True


def test_deleteAllData(firebase_connection: FirebaseConnection):
    result = firebase_connection.deleteAllData()
    assert result is True


def test_getUniqueIdByData(firebase_connection: FirebaseConnection):
    result = firebase_connection.getUniqueIdByData("users", {"testData": 10})
    assert result == 'test_key'


def test_getFirebaseCredentials():
    creds = getFirebaseCredentials()
    assert isinstance(creds, firebase_admin.credentials.Certificate)

