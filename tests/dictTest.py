def getTwilioExample():
    return {'MessagingServiceSid': ['MG82027c85ad2c6b8aafc76b69d1bf3d10'], 'EventType': ['onMessageAdded'],
            'Attributes': ['{}'], 'DateCreated': ['2023-04-05T17:55:35.976Z'], 'Index': ['19'],
            'ChatServiceSid': ['IS3c6189c3038a4e9a9da2c61dc9fbed35'],
            'MessageSid': ['IMaa520c8dcd724a53ad944acedd8419d0'], 'AccountSid': ['AC034f7d97b8d5bc62dfa91b519ac43b0f'],
            'Source': ['WHATSAPP'], 'RetryCount': ['0'], 'Author': ['whatsapp:+5585999171902'],
            'ParticipantSid': ['MBbd9578ed3f2649d0a7c75876952fa293'], 'Body': ['oi'],
            'ConversationSid': ['CH220f52f7f51d49d8a1368fc37d8d9d2a']}


def __main():
    d1 = getTwilioExample()
    sender = d1['Author'][0].split(':')[1]
    content = d1['Body'][0]
    return


if __name__ == '__main__':
    __main()
