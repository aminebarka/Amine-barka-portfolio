const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

content = content.replace("<h3>Projet de Fin d'etudes | Neopolis Development</h3>", "<h3>Graduation Project | Neopolis Development</h3>");
content = content.replaceAll("<h3>Projet Entrepreneurial</h3>", "<h3>Entrepreneurial Project</h3>");
content = content.replace("<h3>Initiative Personnelle</h3>", "<h3>Personal Initiative</h3>");
content = content.replace("<h3>Defi Technique Personnel</h3>", "<h3>Personal Technical Challenge</h3>");
content = content.replace("<h3>Mission Professionnelle | AURES Group</h3>", "<h3>Professional Mission | AURES Group</h3>");

fs.writeFileSync('index.html', content);
console.log('Done translating titles');
