var restify = require('restify')

  // Get a persistence engine for the ping
  , pingSave = require('save')('ping')
  // Create the restify server
  , server = restify.createServer({ name: 'my-api' })
  
// Start the server listening on port 3000
server.listen(3000, function () {
  console.log('%s listening at %s', server.name, server.url)
})


server
  // Allow the use of POST
  .use(restify.fullResponse())
  // Maps req.body to req.params so there is no switching between them
  .use(restify.bodyParser())

  // Get all pings in the system
server.get('/pings', function (req, res, next) {
  // Find every entity within the given collection
  pingSave.find({}, function (error, pings) {
    // Return all of the pings in the system
    res.send(pings)
  })
})


// Create a new ping
server.post('/pings', function (req, res, next) {
  // Make sure name is defined
  if (req.params.idUser === undefined) {
    // If there are any errors, pass them to next in the correct format
    return next(new restify.InvalidArgumentError('idUser must be supplied'))
  }
  //Make sure idBook is defined
  if (req.params.idBook === undefined) {
    // If there are any errors, pass them to next in the correct format
    return next(new restify.InvalidArgumentError('idBook must be supplied'))
  }

  // Create the ping using the persistence engine
  pingSave.create({ idUser: req.params.idUser, idBook: req.params.idBook, progress: req.params.progress, timestamp: req.params.timestamp }, function (error, ping) {
    // If there are any errors, pass them to next in the correct format
    if (error) return next(new restify.InvalidArgumentError(JSON.stringify(error.errors)))
    // Send the ping if no issues
    res.send(201, ping)
  })
})


// Get a single ping by their id
server.get('/pings/:id', function (req, res, next) {
  // Find a single ping by their id within save
  pingSave.findOne({ _id: req.params.id }, function (error, ping) {
    // If there are any errors, pass them to next in the correct format
    if (error) return next(new restify.InvalidArgumentError(JSON.stringify(error.errors)))
    if (ping) {
      // Send the ping if no issues
      res.send(ping)
    } else {
      // Send 404 header if the user doesn't exist
      res.send(404)
    }
  })
})


// Get all pings of a user
server.get('/users/:idUser/pings', function (req, res, next) {
  // Find all pings by their idUser within save
  pingSave.find({idUser: req.params.idUser}, function (error, ping){
    // If there are any errors, pass them to next in the correct format
    if (error) return next(new restify.InvalidArgumentError(JSON.stringify(error.errors)))
    if (ping) {
      // Send the ping if no issues
      res.send(ping)
    } else {
      // Send 404 header if the user doesn't exist
      res.send(404)
    }
  })
})
	

// Get all pings of a book
server.get('/books/:idBook/pings', function (req, res, next) {
  // Find all pings by their idBook within save
  pingSave.find({idBook: req.params.idBook}, function (error, ping){
    // If there are any errors, pass them to next in the correct format
    if (error) return next(new restify.InvalidArgumentError(JSON.stringify(error.errors)))
    if (ping) {
      // Send the ping if no issues
      res.send(ping)
    } else {
      // Send 404 header if the user doesn't exist
      res.send(404)
    }
  })
})
