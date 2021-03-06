import hashlib
import crypt
import random
from uuid import uuid4

class PassHash:
    __algo = '$2a'
    __cost = '$10'

    def __unique_salt(self):
        randInt = self.rand()
        key = str(randInt).encode('utf-8')
        return hashlib.sha1(key).hexdigest()[0:22]

    def hash(self,password):
        key = f"{self.__algo}{self.__cost}${self.__unique_salt()}"
        return crypt.crypt(password,key)

    def generateApiKey(self):
        key = hashlib.md5(str(uuid4()))
        return key
    def rand():
        return random.randint(-2147483648,2147483647)

    def check_password(self,hash,password):
        full_salt = hash[0:29]
        new_hash = crypt.crypt(password,full_salt)
        return hash==new_hash
