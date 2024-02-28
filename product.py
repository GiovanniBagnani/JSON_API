from database import Connection

class Product:
    def __init__(self, id, nome, marca, prezzo):
        self.id = id
        self.nome = nome
        self.marca = marca
        self.prezzo = prezzo
    
    def get_id(self):
        return self.id
    
    def set_nome(self, nome):
        self.nome = nome
    def get_nome(self):
        return self.nome
    
    def set_marca(self, marca):
        self.marca = marca
    def get_marca(self):
        return self.marca
    
    def set_prezzo(self, prezzo):
        self.prezzo = prezzo
    def get_prezzo(self):
        return self.prezzo

    @staticmethod
    def fetch_all():
        #connessione al database
        #db = Connection('192.168.2.200', 'bagnani_giovanni', 'fictional.Armstrongs.chain.', 'bagnani_giovanni_api')
        db = Connection('127.0.0.1', 'giovanni', '123', 'json_api')
        #db = Connection('127.0.0.1', 'user', '123', 'json_api')
        db.connect()
        #esecuzione della query
        #sql = "SELECT * FROM bagnani_giovanni_api.products"
        sql = "SELECT * FROM json_api.products"
        rows = db.execute_query(sql)
        products = []
        i = 0
        for row in rows:
            product = Product(row[0], row[1], row[3], row[2]) #row[1] = nome, row[2] = prezzo, row[3] = marca
            products.append(product)
            i+=1
        return products
    
    @staticmethod
    def find_by_id(product_id):
        #connessione al database
        #db = Connection('192.168.2.200', 'bagnani_giovanni', 'fictional.Armstrongs.chain.', 'bagnani_giovanni_api')
        db = Connection('127.0.0.1', 'giovanni', '123', 'json_api')
        #db = Connection('127.0.0.1', 'user', '123', 'json_api')
        db.connect()
        sql = f"SELECT * FROM json_api.products WHERE id = {product_id}"
        row = db.execute_query(sql)
        if row:
            return Product(row[0][0], row[0][1], row[0][3], row[0][2])
        else:
            return None

    @staticmethod
    def insert_product(nome, marca, prezzo):
        # Connessione al database
        #db = Connection('127.0.0.1', 'user', '123', 'json_api')
        db = Connection('127.0.0.1', 'giovanni', '123', 'json_api')
        cursor = db.connect()
        
        # Esecuzione della query
        sql = "INSERT INTO json_api.products (nome, marca, prezzo) VALUES (%s, %s, %s)"
        cursor.execute (sql, (nome, marca, prezzo))
    
        # Commit delle modifiche e chiusura della connessione
        db.connection.commit()
        db.connection.close()
        # Recupero l'ID dell'elemento appena inserito
        last_insert_id = cursor.lastrowid
        
        # Creazione e restituzione dell'oggetto Product
        return Product(last_insert_id, nome, marca, prezzo)
    
    @staticmethod
    def update (update_data, product_id):
        db = Connection('127.0.0.1', 'giovanni', '123', 'json_api')
        db.connect()
        sql = "UPDATE products SET "
        val = []
        for key, value in update_data.items():
            if key in ["nome", "prezzo", "marca"]:
                sql += f"{key} = %s, "
                val.append(value)

        sql = sql[:-2]
        sql += " WHERE id = %s"
        val.append(product_id)

        db.cursor.execute(sql, val)
        db.connection.commit()
        db.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        return db.cursor.fetchone()

    @staticmethod
    def delete_by_id(product_id):
        # Connessione al database
        db = Connection('127.0.0.1', 'giovanni', '123', 'json_api')
        db.connect()
        db.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        existing_product = db.cursor.fetchone()
        if(existing_product):
            # Esecuzione della query per eliminare il prodotto
            sql = "DELETE FROM json_api.products WHERE id = %s"
            db.cursor.execute(sql, (product_id,))
            db.connection.commit()
            db.connection.close()
            return True
        else:
            return False

