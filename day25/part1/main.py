class Crypto:

    def __init__(self, private_key=0):
        self.subject_number = 7
        self.seed = 7
        self.private_key = private_key;

    def transform(self):
        self.subject_number *= self.seed
        self.subject_number = self.subject_number % 20201227
        self.private_key += 1
        return self.subject_number

    def encrypt(self, msg):
        result = msg
        for i in range(self.private_key):
            result *= msg
            result = result % 20201227

        return result


if __name__ == '__main__':

    crypto_card = Crypto()
    crypto_door = Crypto()
    crypto_card_publickey = 0
    crypto_door_publickey = 0
    with open("input.txt") as inFile:
        crypto_card_publickey = int(inFile.readline().rstrip('\n'))
        while crypto_card.transform() != crypto_card_publickey:
            # print(crypto_card.subject_number)
            pass
        print(crypto_card.private_key)

        crypto_door_publickey = int(inFile.readline().rstrip('\n'))
        while crypto_door.transform() != crypto_door_publickey:
            # print(crypto_door.private_key)
            pass
        print(crypto_door.private_key)

    print(crypto_card.encrypt(crypto_door_publickey))
    print('----')
    print(crypto_door.encrypt(crypto_card_publickey))
