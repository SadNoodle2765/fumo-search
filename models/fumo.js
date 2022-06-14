const mongoose = require('mongoose')


const url = process.env.MONGODB_URL


mongoose.connect(url)
    .then(result => {
        console.log('connected to MongoDB (fumo database)')
    })
    .catch((error) => {
        console.log('error connecting to MongoDB:', error.message)
    })

const fumoSchema = new mongoose.Schema({
    title: String,
    fumoName: String,
    fumoTypes: Array,
    price: Number,
    buyoutPrice: Number,
    buyLink: String,
    imgLink: String,
    shop: String,
    isAuction: Boolean
})

const savedFumoSchema = new mongoose.Schema({
    userName: String,
    links: Array
})


fumoSchema.set('toJSON', {
    transform: (document, returnedObject) => {
        returnedObject.id = returnedObject._id.toString()
        delete returnedObject._id
        delete returnedObject.__v
    }
})

module.exports = {
    Fumo: mongoose.model('Fumo', fumoSchema),
    SavedFumo: mongoose.model('SavedFumo', savedFumoSchema)
}