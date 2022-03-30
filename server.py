import hashlib, json
import time
import tornado.ioloop
import tornado.web

def valid_proof(last_hash, transactions, nonce):

   guess = (str(transactions) + str(last_hash) + str(nonce)).encode()

   global guess_hash

   guess_hash = hashlib.sha256(guess).hexdigest()

   print(guess_hash)

   return guess_hash[0:2] == '00'

def pow(last_hash, transactions):

   nonce = 0

   while not valid_proof(last_hash, transactions, nonce):

       nonce += 1

   return nonce

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Just a test")

    def post(self):
        global guess_hash
        guess_hash = None
        blockchain = self.get_argument("blockchain")
        block = self.get_argument("block")
        blockchain_unserialized = json.loads(blockchain)
        block_unserialized = json.loads(block)
        print(block_unserialized["transactions"])
        start_time = time.time()
        nonce = pow(block_unserialized["prev_hash"], block_unserialized["transactions"])
        #print("Blockchain : %s \nBlock : %s" % (blockchain, block))
        #print("Nom : %s \nheure %s" % (user, passwd))
        #self.write("Nom : %s \nheure %s" % (user, passwd))
        end_time = time.time()
        total_time = end_time - start_time
        #guess_hash = json.dumps(guess_hash)
        #total_time = json.dumps(total_time)
        #nonce = json.dumps(nonce)
        data = {
            "hash": guess_hash,
            "timer": total_time,
            "nonce": nonce
        }
        data_serialized = json.dumps(data).encode('utf-8')
        print(guess_hash)
        print(total_time)
        print(nonce)
        self.write(data_serialized)

def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
