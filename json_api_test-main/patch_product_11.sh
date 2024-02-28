curl -X PATCH -H "Content-Type: application/json" -d '{
  "data": {
    "type": "product",
    "attributes": {
      "marca": "nuova_marca",
      "nome": "nuovo_nome",
      "prezzo": "11"
    }
  }
}' http://127.0.0.1:8081/products/113
