curl -X POST -H "Content-Type: application/json" -d '{
  "data": {
    "type": "product",
    "attributes": {
      "marca": "Adidas",         
      "nome": "superstar",
      "prezzo": "11110"
    }
  }
}' http://127.0.0.1:8081/products 
