import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the projects section
# Everything between <h1 id="projects">Projects</h1><hr /> and <p >\s*These projects represent
pattern = re.compile(r'(<h1 id="projects">Projects</h1>\s*<hr />\s*)(.*?)\s*(<p(?:[^>]*)>\s*These projects represent)', re.DOTALL)

match = pattern.search(html)
if match:
    prefix = match.group(1)
    projects_content = match.group(2)
    suffix = match.group(3)
    
    # split projects_content by <hr />
    parts = re.split(r'\s*<hr />\s*', projects_content)
    projects = [p.strip() for p in parts if p.strip()]
    
    # find the specific projects
    eurafatours = [p for p in projects if 'Eurafatours &amp; Domaine des Citronniers' in p]
    camp = [p for p in projects if 'Camp Abdelmoula' in p]
    defi = [p for p in projects if 'Défi du Désert Voyages' in p]
    untold = [p for p in projects if 'The Untold Layers' in p]
    
    others = [p for p in projects if p not in eurafatours + camp + defi + untold]
    
    # Put the 3 requested ones at the top, followed by untold (since it's a B-studio project too, usually grouped), then others
    ordered_projects = eurafatours + camp + defi + untold + others
    
    new_projects_content = '\n         <hr />\n         '.join(ordered_projects)
    
    # replace back
    new_html = html[:match.start(2)] + new_projects_content + '\n\n         ' + html[match.start(3):]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully reordered projects in index.html")
else:
    print("Could not find the projects section using regex.")
