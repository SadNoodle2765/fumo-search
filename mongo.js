const mongoose = require('mongoose')


const url = `mongodb+srv://noodlebot:HskVtFvFpvHxOWOK@cluster0.36l2o.mongodb.net/fumoApp?retryWrites=true&w=majority`

mongoose.connect(url)

const fumoSchema = new mongoose.Schema({
    title: String,
    fumoType: String,
    price: Number,
    buyoutPrice: Number,
    buyLink: String,
    imgLink: String
})

const fumoModel = mongoose.model('fumos', fumoSchema)

// const note = new Note({
//   content: 'Hashiri Nio',
//   date: new Date(),
//   important: true,
// })

// note.save().then(result => {
//   console.log('note saved!')
//   mongoose.connection.close()
// })

fumoModel.find({fumoType: 'Sakuya'}).then(result => {
    result.forEach(fumo => {
        console.log(fumo)
    })
    mongoose.connection.close()
})