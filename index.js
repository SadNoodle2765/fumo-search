require('dotenv').config()
const express = require('express')
const cors = require('cors')
const Fumo = require('./models/fumo')

const app = express()
app.use(express.json())
app.use(cors())
app.use(express.static('build'))

const {PythonShell} = require('python-shell')

app.get('/api/fumo', (request, response) => {

    const fumoType = request.query.fumoType

    if (fumoType == "") {
        response.json([])
    } else {
        Fumo.find({fumoType: fumoType}).then(result => {
            response.json(result)
        })
    }
})

app.get('/updateDB', (request, response) => {
    response.send('Updating DB')
    let options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: './python',
        args: ['SadNoodle']
    }

    PythonShell.run('main.py', options, (err, result) => {
        if (err) throw err;

        console.log('result: ', result.toString())
        response.send(result.toString())
    })
    // response.end('Finished Updating.')
})



const PORT = process.env.PORT || 8000
app.listen(PORT)
console.log(`Server running on port ${PORT}`)