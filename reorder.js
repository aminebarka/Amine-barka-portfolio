const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');

let newContent = content.replace(/\s*<h3>Client — B Studio<\/h3>/g, '');

const startMarker = '<h1 id=\"projects\">Projects</h1>';
const startIndex = newContent.indexOf(startMarker);
if (startIndex !== -1) {
    const hrIndex = newContent.indexOf('<hr />', startIndex);
    const endMarker = '<p class=\"scroll-animate fade-in-up\">';
    const endIndex = newContent.indexOf(endMarker, hrIndex);
    
    let projectsBlock = newContent.substring(hrIndex, endIndex);
    let parts = projectsBlock.split('<hr />');
    
    let topParts = [];
    let bottomParts = [];
    
    for (let i = 1; i < parts.length; i++) {
        if (!parts[i].trim()) continue;
        if (parts[i].includes('Eurafatours') || parts[i].includes('Camp Abdelmoula') || parts[i].includes('Defi du Desert') || parts[i].includes('The Untold Layers')) {
            topParts.push(parts[i]);
        } else {
            bottomParts.push(parts[i]);
        }
    }
    
    let newProjectsBlock = '\         <hr />' + topParts.join('<hr />') + bottomParts.join('<hr />') + '\\         ';
    
    newContent = newContent.substring(0, hrIndex) + newProjectsBlock + newContent.substring(endIndex);
    fs.writeFileSync('index.html', newContent);
    console.log('Success');
} else {
    console.log('Start marker not found');
}
