# glose-api

Le script app.js présenté ici permet la création d'une API sur un serveur local (port 3000), répondant aux 4 endpoints demandés suivants:
- POST ping: enregistrer un ping
- GET pings: récupérer tous les pings
- GET users/:idUser/pings: récupérer tous les pings d'un utilisateur
- GET books/:idBook/pings: récupérer tous les pings d'un livre

En plus, un endpoint 'GET pings/:id: récupérer un ping donné' a été ajouté.

Les pings doivent être entrés sous la forme:
{idUser = ; idBook = ; progress = ; timestamp = }
