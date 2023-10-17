import pytest

from utils.instagram_utils import extractMetadataFromInstagramDict, convertIncomingInstagramMessageToProperFormat


@pytest.mark.parametrize("inputDict, expected_output", [
    (
            {"From": ["instagram:1234567890"], "Sender": "JohnDoe"},
            {"from": "instagram", "phoneNumber": "1234567890", "sender": "JohnDoe"}
    ),
    (
            {"From": ["facebook:0987654321"], "Sender": "JaneDoe"},
            {"from": "facebook", "phoneNumber": "0987654321", "sender": "JaneDoe"}
    ),
])
def test_extractMetadataFromInstagramDict(inputDict, expected_output):
    output = extractMetadataFromInstagramDict(inputDict)
    assert output == expected_output


@pytest.mark.parametrize("data, expected_output", [
    (
            {
                'entry': [{'messaging': [
                    {'message': {'text': 'Hello!'}, 'sender': {'id': '111'}, 'recipient': {'id': '222'}}]}],
                'object': 'instagram'
            },
            {
                "ProfileName": ["User"], "WaId": ["111"], "Body": ["Hello!"],
                "To": ["instagram:222"], "From": ["instagram:111"], "senderId": "111", "recipientId": "222",
                "Sender": "111"
            }
    ),
    (
            {
                'entry': [{'messaging': [
                    {'message': {'text': 'Hi there!'}, 'sender': {'id': '333'}, 'recipient': {'id': '444'}}]}],
                'object': 'facebook'
            },
            {
                "ProfileName": ["User"], "WaId": ["333"], "Body": ["Hi there!"],
                "To": ["facebook:444"], "From": ["facebook:333"], "senderId": "333", "recipientId": "444",
                "Sender": "333"
            }
    ),
])
def test_convertIncomingInstagramMessageToProperFormat(data, expected_output):
    output = convertIncomingInstagramMessageToProperFormat(data)
    assert output == expected_output


if __name__ == '__main__':
    pytest.main()
