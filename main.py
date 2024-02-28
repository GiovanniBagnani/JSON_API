from database import Connection
from class_http import RequestHandler
from product import Product
#import class_http
#import mysql.connector

"""
#connessione al database
db = Connection('192.168.2.200', 'bagnani_giovanni', 'fictional.Armstrongs.chain.', 'bagnani_giovanni_api')
db.connect()
#esecuzione della query
sql = "SELECT * FROM bagnani_giovanni_api.products"
rows = db.execute_query(sql)
#controllo il risultato stampandolo
print("Read", len(rows), "row(s) of data.")
products = []
i = 0
for row in rows:
    print(row)
    product = Product(i, row[1], row[2], row[3])
    products.append(product)
    i+=1
#stampe per verifiche del codice
print(len(products))
#RequestHandler.do_GET()
print(products[1].get_brand())
"""

# Creazione di un'istanza di MyHTTPRequestHandler
request_handler = RequestHandler()
# Chiamata al metodo do_GET con il parametro products
request_handler.do_GET(products)

"""
#connection = mysql.connector.connect(host='192.168.2.200',database='bagnani_giovanni_api',user='bagnani_giovanni',password='fictional.Armstrongs.chain.')
db = Connection.connect
sql = "SELECT nome, marca, prezzo FROM bagnani_giovanni_api.products"
cursor = db.cursor()
cursor.execute(sql)
#cursor = connection.cursor()
rows = cursor.fetchall()
print("Read",cursor.rowcount,"row(s) of data.")
"""

"""
products = ["codice", "location", "content_type", "dati"]
dati = ["tipo", "id", "attributi"]
attributi = ["marca", "nome", "prezzo"]
"""