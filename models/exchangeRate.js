const mongoose = require('mongoose')

const url = process.env.MONGODB_URL


mongoose.connect(url)
    .then(result => {
        console.log('connected to MongoDB (exchange rate)')
    })
    .catch((error) => {
        console.log('error connecting to MongoDB:', error.message)
    })

const rateSchema = new mongoose.Schema({
    currency: String,
    value: Number
})


rateSchema.set('toJSON', {
    transform: (document, returnedObject) => {
        returnedObject.id = returnedObject._id.toString()
        delete returnedObject._id
        delete returnedObject.__v
    }
})

module.exports = mongoose.model('ExchangeRate', rateSchema)