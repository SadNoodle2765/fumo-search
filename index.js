require('dotenv').config()
const path = require('path')
const express = require('express')
const cors = require('cors')
const morgan = require('morgan')
const fumoModule = require('./models/fumo')
const Fumo = fumoModule.Fumo
const SavedFumo = fumoModule.SavedFumo
const Vote = fumoModule.Vote
const ExchangeRate = require('./models/exchangeRate')

const app = express()
app.use(express.json())
app.use(cors())
app.use(morgan('tiny'));
app.use(express.static('build'))

// const {PythonShell} = require('python-shell')

app.get('/search', (request, response) => {
    response.sendFile('index.html', {root: path.join(__dirname, 'build/')})
})

app.get('/saved', (request, response) => {
    response.sendFile('index.html', {root: path.join(__dirname, 'build/')})
})

app.get('/alerter', (request, response) => {
    response.sendFile('index.html', {root: path.join(__dirname, 'build/')})
})

app.get('/api/vote', (request, response) => {
    const queries = request.query
    const userName = request.query.userName

    if (!queries.hasOwnProperty('userName')) {
        Vote.find({}).then(result => {
            response.json(result)
        })
    } else {
        Vote.findOne({userName: userName}).then(result => {
            response.json(result)
        })
    }
})

app.post('/api/vote', (request, response) => {
    const body = request.body
    const userName = body.userName
    const fumo = body.fumo

    console.log(userName, fumo)

    Vote.findOneAndUpdate({userName: userName}, {$set: {fumo: fumo}}, {upsert: true}, (err, doc) => {            // upsert makes it so it adds document if username doesn't exist
        if (err) return response.send(500, {error: err})
        return response.send('Saved successfully')
    })
})

app.get('/api/fumo', (request, response) => {

    const queries = request.query

    const fumoName = request.query.fumoName

    if (!queries.hasOwnProperty('fumoName') || fumoName == "") {            // If there's no fumoName or the fumoName is empty, return all the fumos
        Fumo.find({}).then(result => {
            response.json(result)
        })
    } else {
        Fumo.find({fumoName: fumoName}).then(result => {
            response.json(result)
        })
    }
})

app.get('/api/exchangerate', (request, response) => {
    const currency = request.query.currency

    if (currency == "all") {
        ExchangeRate.find({}).then(result => {
            response.json(result)
        })
    } else {
        ExchangeRate.find({currency: currency}).then(result => {
            response.json(result)
        })
    }
})

app.get('/api/savedfumos', (request, response) =>  {
    const userName = request.query.userName

    SavedFumo.findOne({userName: userName}).then(result => {
        response.json(result)
    })
}) 

app.post('/api/savedfumos', (request, response) => {
    const body = request.body
    const userName = body.userName
    const link = body.link

    SavedFumo.findOneAndUpdate({userName: userName}, {$addToSet: {links: link}}, {upsert: true}, (err, doc) => {            // upsert makes it so it adds document if username doesn't exist
        if (err) return response.send(500, {error: err})
        return response.send('Saved successfully')
    })
})

app.delete('/api/savedfumos', (request, response) => {
    const body = request.body
    const userName = body.userName
    const link = body.link

    SavedFumo.findOneAndUpdate({userName: userName}, {$pull: {links: link}}, (err, doc) => {
        if (err) return response.send(500, {error: err})
        return response.send('Removed link successfully')
    })
})


// app.get('/updateDB', (request, response) => {
//     response.send('Updating DB')
//     let options = {
//         mode: 'text',
//         pythonOptions: ['-u'],
//         scriptPath: './python',
//         args: ['SadNoodle']
//     }

//     PythonShell.run('main.py', options, (err, result) => {
//         if (err) throw err;

//         console.log('result: ', result.toString())
//     })
//     // response.end('Finished Updating.')
// })



const PORT = process.env.PORT || 3001
app.listen(PORT)
console.log(`Server running on port ${PORT}`)