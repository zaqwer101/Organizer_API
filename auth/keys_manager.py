import rsa
import os
###
# Это, наверное, будет часть сервиса авторизации.
# Будем 1) проверять зашифрованную мессагу, и если она совпадает с заданной при запуске приложения
# Если всё совпало, генерируем токен авторизации, с которым делаем все остальные запросы
# Через час инактива токен сгорает. Их можно хранить в Redis
###
def load_keys():
    private = rsa.PrivateKey.load_pkcs1(open('private', 'r').read().encode())
    public  = rsa.PublicKey.load_pkcs1(open('public', 'r').read().encode())
    return private, public

def generate_keys():
    (pubkey, privkey) = rsa.newkeys()
    pubkey_pem = pubkey.save_pkcs1()  # (format='PEM')
    privkey_pem = privkey.save_pkcs1()
    os.remove('public')
    os.remove('private')
    open('public', 'w').write(pubkey_pem.decode('utf-8'))
    open('private', 'w').write(privkey_pem.decode('utf-8'))

def encrypt(message):
    return rsa.encrypt(message.encode(), load_keys()[1])

def decrypt(message):
    return rsa.decrypt(message, load_keys()[0]).decode('utf-8')
