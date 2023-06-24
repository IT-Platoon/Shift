const express = require('express');
const serveStatic = require("serve-static")
// var cors = require('cors')
const path = require('path');
app = express();
app.use(serveStatic(path.join(__dirname, 'dist')));
// app.use(cors())
const port = process.env.PORT || 3000;
app.listen(port);
