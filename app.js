// TEST FILE - Security scanner validation only. DO NOT use in production.
// Purpose: Trigger Aikido SAST scanner with SQL injection and XSS patterns.

const express = require('express');
const app = express();

// SAST trigger #1: SQL injection via string concatenation
app.get('/user', (req, res) => {
  const userId = req.query.id;
  const query = 'SELECT * FROM users WHERE id = ' + userId;
  // db.execute(query) — intentionally unsafe, for scanner validation only
  res.send('Query: ' + query);
});

// SAST trigger #2: Reflected XSS — user input echoed directly into HTML
app.get('/search', (req, res) => {
  const term = req.query.q;
  res.send('<h1>Results for: ' + term + '</h1>');
});

app.listen(3000);
