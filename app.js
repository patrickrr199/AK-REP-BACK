// TEST FILE ONLY — Deliberate SAST antipatterns for Aikido SAST scanner validation.
// SQL injection and XSS patterns included intentionally. DO NOT USE IN PRODUCTION.

const express = require('express');
const { Client } = require('pg');

const app = express();
app.use(express.urlencoded({ extended: true }));

const db = new Client({ connectionString: 'postgresql://localhost/test' });
db.connect();

// SAST trigger 1: SQL injection via string concatenation
app.get('/user', async (req, res) => {
  const userId = req.query.id;
  const query = 'SELECT * FROM users WHERE id = ' + userId;
  const result = await db.query(query);
  res.json(result.rows);
});

// SAST trigger 2: Reflected XSS — user input echoed into HTML without sanitization
app.get('/greet', (req, res) => {
  const name = req.query.name;
  res.send('<h1>Hello, ' + name + '</h1>');
});

app.listen(3000, () => console.log('Test server running on port 3000'));