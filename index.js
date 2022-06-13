require('dotenv').config()
const express = require('express')
const cors = require('cors')
const Fumo = require('./models/fumo')
const ExchangeRate = require('./models/exchangeRate')

const app = express()
app.use(express.json())
app.use(cors())
app.use(express.static('build'))

// const {PythonShell} = require('python-shell')

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