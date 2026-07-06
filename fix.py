import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix duplicates
pattern = re.compile(r'(<h1 id="projects">Projects</h1>\s*<hr />\s*)(.*?)\s*(<p(?:[^>]*)>\s*These projects represent)', re.DOTALL)
match = pattern.search(html)
if match:
    prefix = match.group(1)
    projects_content = match.group(2)
    suffix = match.group(3)
    
    parts = re.split(r'\s*<hr />\s*', projects_content)
    projects = [p.strip() for p in parts if p.strip()]
    
    # Remove duplicates preserving order
    unique_projects = []
    seen = set()
    for p in projects:
        # Extract title to use as key
        title_match = re.search(r'<h2>(.*?)</h2>', p)
        if title_match:
            title = title_match.group(1).strip()
            if title not in seen:
                seen.add(title)
                unique_projects.append(p)
        else:
            unique_projects.append(p)
            
    # Now modify the specific projects in the list
    for i, p in enumerate(unique_projects):
        if '<h2>The Untold Layers</h2>' in p:
            if '<div class="image' not in p:
                img_html = '\n           <div class="image ">\n             <img\n               src="/images/Theuntoldlayers.png"\n               alt="The Untold Layers"\n               loading="lazy"\n             />\n           </div>'
                # insert before the closing </div>
                last_div_idx = p.rfind('</div>')
                if last_div_idx != -1:
                    unique_projects[i] = p[:last_div_idx] + img_html + '\n         ' + p[last_div_idx:]
                    
        elif '<h2>Camp Abdelmoula</h2>' in p:
            # update image src
            unique_projects[i] = p.replace('/images/camp-abdelmoula.png', '/images/campabdelmoula.png')
            # The link is already https://camp-abdelmoula.com/, let's ensure it's there
            if 'https://camp-abdelmoula.com/' not in unique_projects[i]:
                 unique_projects[i] += '\n           <p><a href="https://camp-abdelmoula.com/" target="_blank" class="project-link">View Project →</a></p>'
                 
        elif '<h2>Défi du Désert Voyages</h2>' in p:
            # link should be https://defidesert.com/
            unique_projects[i] = re.sub(r'href="[^"]+"', 'href="https://defidesert.com/"', unique_projects[i])
            
    new_projects_content = '\n         <hr />\n         '.join(unique_projects)
    
    # replace back
    new_html = html[:match.start(2)] + new_projects_content + '\n\n         ' + html[match.start(3):]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully updated index.html")
else:
    print("Could not find the projects section using regex.")
