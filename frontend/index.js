const express = require('express')
const path = require('path')
require('dotenv').config()

const app = express()
const PORT = process.env.PORT || 3000

const SUBMIT_URL = process.env.BACKEND_URL

// Add body parsing middleware
app.use(express.urlencoded({ extended: true }))
app.use(express.json())

app.set('view engine', 'ejs')
app.set('views', path.join(__dirname, 'views'))

app.get('/', (req, res) => {
  res.render('index', {
    title: 'Home',
    message: 'Hello from EJS!'
  })
})

app.post('/submit', async(req, res) => {
  // Handle form submission logic here
  try {
    const response = await fetch(SUBMIT_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "name": req.body.name,
        "email": req.body.email,
        "message": req.body.message
      })
    })

    const data = await response.json()
    res.json(data)
  } catch (error) {
    console.log(error)
    res.status(500).json({ error: error.message })
  }
})

app.listen(PORT, () => {
  console.log(`Server is running on port http://localhost:${PORT}`)
})