# glose-api

My first attempt at creating an API using javascript.

Script app.js creates an API on a local server with the 4 following endpoints:

- POST ping: save a ping
- GET pings: collect all pings
- GET users/:idUser/pings: collect all pings corresponding to the user
- GET books/:idBook/pings: collect all pings corresponding to the book

Additionnally, an endpoint 'GET pings/:id: collect a given ping' was added.

Pings have agree with the following format:
{idUser = ; idBook = ; progress = ; timestamp = }
