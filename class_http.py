import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from product import Product

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    # Metodo per gestire le richieste GET
    # Per fare la get: curl http://localhost:8081/products
    def do_GET(self):
        # Preparazione della risposta JSON
        if self.path == '/products':
            # Dati iniziali
            products = Product.fetch_all()
            product_data = []
            for product in products:
                product_item = {
                    "type": "products",
                    "id": str(product.id),
                    "attributes": {
                        "marca": product.marca,
                        "nome": product.nome,
                        "prezzo": str(product.prezzo)
                    }
                }
                product_data.append(product_item)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            #self.wfile.write(json.dumps({'data': products_json_serializable}).encode())
            self.wfile.write(json.dumps({'data': product_data}).encode())
        elif self.path.startswith('/products/'):
                # Ottenere l'ID del prodotto dall'URL
                product_id = self.path.split('/')[-1]
                """
                # Verificare se l'ID è un numero intero valido
                if not product_id.isdigit():
                    self.send_error(400, 'Invalid product ID')
                    return
                """

                
                # Recuperare il prodotto corrispondente all'ID
                product = Product.find_by_id(product_id)                
                if product:
                    product_data = {
                        "type": "products",
                        "id": str(product.id),
                        "attributes": {
                            "marca": product.marca,
                            "nome": product.nome,
                            "prezzo": product.prezzo
                        }
                    }
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'data': product_data}).encode())
                else:
                    self.send_error(404, f'Product with ID {product_id} not found')
  
    # Metodo per gestire le richieste POST
    # curl -d '{"id":"11", "name":"cesna","brand":"cesna","price":"100000"}' -X POST http://192.168.2.210:8000/products
    # Invoke-WebRequest -Uri "http://127.0.0.1:8081/products" -Method Post -Body '{"nome":"cesna","marca":"cesna","prezzo":"100000"}' -ContentType "application/json"
    def do_POST(self):
        if self.path == '/products':
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            # Dati iniziali
            products = Product.fetch_all()
            id = products[-1].id #id dell'ultimo prodotto
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_product = json.loads(post_data)['data']['attributes']       
            product = Product.insert_product(new_product["nome"], new_product["marca"], new_product["prezzo"])
            products.append(product)
            product_item = {
                    "type": "products",
                    "id": str(product.id),
                    "attributes": {
                        "marca": product.marca,
                        "nome": product.nome,
                        "prezzo": product.prezzo
                    }
            }

            self.wfile.write(json.dumps({"data": product_item}).encode())           
        else:
            self.send_error(404, 'Endpoint non trovato')



    # Metodo per gestire le richieste Patch
    def do_PATCH(self):
        if self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]
        
            # Recupera il prodotto dal database
            product = Product.find_by_id(product_id)
            if product is None:
                self.send_error(404, f'Product with ID {product_id} not found')
                return

            # Leggi i dati di aggiornamento dalla richiesta
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            update_product = json.loads(patch_data)['data']['attributes']
            updated_product = Product.update(update_product, product_id)
            #product = Product(product_id, update_product["nome"], update_product["marca"], update_product["prezzo"])
            
            product_item = {
                    "type": "products",
                    "id": str(product_id),
                    "attributes": {
                        "nome": updated_product[1],
                        "prezzo": updated_product[2],
                        "marca": updated_product[3]
                    }
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/vnd.api+json')
            self.end_headers()
            self.wfile.write(json.dumps({"data": product_item}).encode())
        else:
            self.send_error(404, 'Endpoint non trovato')

    # Metodo per gestire le richieste DELETE
    def do_DELETE(self):
        if self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]
            if(Product.delete_by_id(product_id)):
                self.send_response(204)  # 204 No Content - Operazione di eliminazione riuscita
                self.send_header('Content-type', 'application/vnd.api+json')
                self.end_headers()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/vnd.api+json')
                self.end_headers()
        else:
            self.send_error(404, 'Endpoint non trovato')

def run():
    port = 8081
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()