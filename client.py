# coding: utf-8
import hashlib, json
import uuid
import time
import random
import requests

uuidcapteur = uuid.uuid3(uuid.NAMESPACE_DNS, "Pauvre Ferrari")
print(type(uuidcapteur))
blockchain = []
prev_temp = 0
gps_coordinates = (51, 38)

ts = time.gmtime()
prev_temp = round(random.uniform(-5,10),1)
block_genesis = {
 'prev_hash': None,
 'transactions': [str(uuidcapteur), prev_temp, time.strftime("%x %X", ts), gps_coordinates]
}

block_genesis_serialized = json.dumps(block_genesis).encode('utf-8')

block_genesis_hash = hashlib.sha256(block_genesis_serialized).hexdigest()

blockchain.append(block_genesis_hash)

print(block_genesis_serialized)

def make_block():
    ts = time.gmtime()
    block = {
    'prev_hash': blockchain[len(blockchain) - 1],
    'transactions': [str(uuidcapteur), prev_temp, time.strftime("%x %X", ts), gps_coordinates]
    }

    blockgenesis_serialized = json.dumps(block_genesis).encode('utf-8')
    blockchain_dump = json.dumps(blockchain).encode('utf-8')

    dt = {
    'blockchain': blockchain_dump,
    'block': blockgenesis_serialized
    }

    block_hash = requests.post("http://127.0.0.1:5000", data=dt)

    print(block_hash.text)

    tab = block_hash.text

    tab = tab.replace('{', '')
    tab = tab.replace('}', '')
    tab = tab.replace('"', '')
    tab = tab.replace(':', '')
    tab = tab.replace(' ', '')
    tab = tab.replace('hash', '')
    tab = tab.replace('timer', '')
    tab = tab.replace('nonce', '')

    l = list(tab.split(","))

    blockchain.append(l[0])

    print(blockchain[len(blockchain) - 1])
    
def check_temperature():
    global prev_temp
    temp = round(random.uniform(-5,10),1)
    if abs(temp - prev_temp) > 1:
        prev_temp = temp
        make_block()
        
#main function
while len(blockchain) < 4:
    check_temperature()

print(blockchain)
