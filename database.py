import mysql.connector

class Connection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    
    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

#CREATE TABLE bagnani_giovanni_api.products ( id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, nome VARCHAR(100), marca VARCHAR(100), prezzo FLOAT );