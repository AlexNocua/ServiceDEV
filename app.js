const express = require('express')
const app = express()
const port = 3000


app.set('views', './frontend/views')
// configuracio ndel motor de plantillas
app.set('view engine', 'ejs')

// configuracion de los archivos publicos de la aplicacion
app.use(express.static('public'))

app.get('/', (req, res) => {
    // res.send('Hola mundo')
    res.render('index', {
        message: 'funcionando'
    })
})

app.listen(port, () => {
    console.log('Primera aplicacion de express en el puerto ${port}');
})