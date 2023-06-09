from collections import namedtuple

PushReturn = namedtuple('PushReturn', 'key')


class MockedDbRef:
    def child(self, path):
        return self

    def get(self):
        return {'dummyData': 5}

    def push(self, data):
        return PushReturn(key='test_key')

    def set(self, data):
        return True

    def delete(self):
        return True


def __main():
    mdr = MockedDbRef()
    data = mdr.get()


if __name__ == '__main__':
    __main()
