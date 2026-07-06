import re
import glob
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Translate titles
html = html.replace("Projet de Fin d'Études", "Graduation Project")
html = html.replace("Projet Entrepreneurial", "Entrepreneurial Project")
html = html.replace("Initiative Personnelle", "Personal Initiative")
html = html.replace("Défi Technique Personnel", "Personal Technical Challenge")
html = html.replace("Mission Professionnelle", "Professional Mission")
html = html.replace("Client — B Studio", "")
html = html.replace('<span class="project-badge badge-in-progress">🟡 En cours — 2026</span>', '')

# 2. Modify specific projects
def process_project(html_content, h2_title, new_desc, remove_b_studio, remove_features, new_link=None, add_img=None):
    # This is tricky with regex, better to use replace
    # We find the project block
    block_pattern = re.compile(r'(<div\s+class="project-item[^>]*>\s*<h2>' + re.escape(h2_title) + r'</h2>.*?</div>\s*)(?=<hr|</div>)', re.DOTALL)
    match = block_pattern.search(html_content)
    if not match: 
        print(f"Could not find project block for {h2_title}")
        return html_content
    
    block = match.group(1)
    
    if remove_b_studio:
        block = re.sub(r'<h3>.*?</h3>\s*', '', block) # We translated titles but B studio is already removed by string replacement above. Wait, string replacement leaves empty <h3></h3> if it was just "Client — B Studio". Let's remove empty h3s.
        block = re.sub(r'<h3>\s*</h3>\s*', '', block)
        
    if remove_features:
        block = re.sub(r'<ul class="features-list">.*?</ul>\s*', '', block, flags=re.DOTALL)
        
    # Replace description paragraph (find the paragraph that contains the text to be replaced)
    block = re.sub(r'<p>\s*(?:Site web unifié|Site web pour un camp|Refonte totale|Blog magazine).*?</p>', f'<p>\n             {new_desc}\n           </p>', block, flags=re.DOTALL)
    
    if new_link:
        if 'View Project' in block:
            block = re.sub(r'<a href="[^"]+"([^>]*class="project-link"[^>]*)>View Project →</a>', f'<a href="{new_link}"\\1>View Project →</a>', block)
        else:
            # insert before the last </div>
            link_html = f'\n           <p><a href="{new_link}" target="_blank" class="project-link">View Project →</a></p>'
            last_div_idx = block.rfind('</div>')
            if last_div_idx != -1:
                block = block[:last_div_idx] + link_html + '\n         ' + block[last_div_idx:]
            
    if add_img and '<div class="image' not in block:
        img_html = f'\n           <div class="image">\n             <img\n               src="{add_img}"\n               alt="{h2_title}"\n               loading="lazy"\n             />\n           </div>'
        # Insert before the last </div>
        last_div_idx = block.rfind('</div>')
        if last_div_idx != -1:
            # if we just inserted a link, the last </div> is the same, so we insert before link if possible.
            # let's just use string replace on the original block and insert before <p><a href=
            if '<p><a href="' in block:
                block = block.replace('<p><a href="', img_html + '\n           <p><a href="')
            else:
                block = block[:last_div_idx] + img_html + '\n         ' + block[last_div_idx:]

    html_content = html_content.replace(match.group(1), block)
    return html_content

html = process_project(html, "Eurafatours &amp; Domaine des Citronniers", 
    "Unified website for a travel agency (Eurafatours) and a luxury rural lodge (Domaine des Citronniers) in Béni Khiar, Nabeul. 14 custom PHP pages with premium design. CI/CD deployment via GitHub Actions → Hostinger.", 
    True, True)

html = process_project(html, "Camp Abdelmoula", 
    "Website for a luxury camp in the heart of the Tunisian Sahara in Tembaine, Douz. 51 tents including 27 royal ones. Cinematic design inspired by the desert with a sand/gold/night palette. Cross-branding with Défi du Désert Voyages.", 
    True, True, "https://camp-abdelmoula.com/", "/images/camp-abdelmoula.png")

html = process_project(html, "Défi du Désert Voyages", 
    "Complete redesign of a static HTML website from 2010 for an agency specializing in 4x4 tours, Quad & SSV Raids, and camel treks in southern Tunisia. Cinematic adventure design.", 
    True, True, "https://defidesert.com/")

html = process_project(html, "The Untold Layers", 
    "Multi-theme English magazine blog targeting an international audience. 9 categories: Lifestyle, Culture & Trends, Travel, Sports, Technology & AI, Entertainment, Fashion, Psychology, Digital Life. SEO strategy + AdSense monetization + affiliation.", 
    True, True)

# Clean up any empty h3 tags left over from simple string replacements
html = re.sub(r'<h3>\s*(?:<span[^>]*>\s*</span>)?\s*</h3>\s*', '', html)

# 3. Remove scroll animations
classes_to_remove = ["scroll-animate", "fade-in-up", "scale-in", "stagger", "slide-left", "slide-right", "animate-in"]
for cls in classes_to_remove:
    html = re.sub(rf'\b{cls}\b\s*', '', html)

# cleanup empty class attributes
html = html.replace('class=""', '')
html = html.replace('class=" "', '')

# remove the script tag for scroll animations
html = re.sub(r'<!-- Scroll Animations Script -->\s*<script>.*?</script>', '', html, flags=re.DOTALL)

# 4. Reorder projects
projects_section_pattern = re.compile(r'(<h1 id="projects">Projects</h1>\s*<hr />)(.*?)(<p(?: class="[^"]*")?>\s*These projects represent)', re.DOTALL)
match = projects_section_pattern.search(html)
if match:
    prefix = match.group(1)
    projects_content = match.group(2)
    suffix = match.group(3)
    
    parts = re.split(r'\s*<hr />\s*', projects_content)
    projects = [p.strip() for p in parts if p.strip()]
    
    eurafatours = [p for p in projects if 'Eurafatours &amp; Domaine des Citronniers' in p]
    camp = [p for p in projects if 'Camp Abdelmoula' in p]
    defi = [p for p in projects if 'Défi du Désert Voyages' in p]
    untold = [p for p in projects if 'The Untold Layers' in p]
    
    others = [p for p in projects if p not in eurafatours + camp + defi + untold]
    
    ordered_projects = eurafatours + camp + defi + untold + others
    
    new_projects_content = '\n         <hr />\n         '.join(ordered_projects)
    new_projects_content = '\n         ' + new_projects_content + '\n         <hr />\n\n         '
    
    html = html.replace(match.group(2), new_projects_content)

# 5. WhatsApp Button
whatsapp_html = """
    <a href="https://wa.me/21655532955" class="whatsapp-float" target="_blank" rel="noopener noreferrer" style="position: fixed; bottom: 20px; right: 20px; background-color: #25d366; color: white; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3); z-index: 1000; transition: transform 0.3s ease;">
      <svg viewBox="0 0 32 32" width="35" height="35" fill="currentColor">
        <path d="M16 2.3c-7.6 0-13.7 6.1-13.7 13.7 0 2.4.6 4.7 1.8 6.7L2.3 29.7l7.2-1.9c2 .1 4.2 1.7 6.5 1.7 7.6 0 13.7-6.1 13.7-13.7S23.6 2.3 16 2.3zm0 25.1c-2 0-3.9-.5-5.6-1.5l-.4-.2-4.1 1.1 1.1-4-.2-.4c-1.1-1.7-1.7-3.7-1.7-5.8 0-6.4 5.2-11.6 11.6-11.6s11.6 5.2 11.6 11.6-5.2 11.6-11.6 11.6z"/>
        <path d="M21.5 17.5c-.3-.1-1.8-.9-2.1-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-1 1.2-.2.2-.4.3-.7.1-.3-.1-1.3-.5-2.5-1.5-.9-.8-1.5-1.8-1.6-2.1-.1-.3 0-.5.2-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5s-.7-1.7-1-2.3c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.3-.3.3-1.1 1.1-1.1 2.7 0 1.6 1.1 3.1 1.3 3.3.2.3 2.3 3.5 5.5 4.9.8.3 1.4.5 1.8.7.8.2 1.5.2 2 .1.6-.1 1.8-.7 2.1-1.4.2-.7.2-1.3.1-1.4-.1-.1-.3-.2-.6-.3z"/>
      </svg>
    </a>
"""
html = html.replace("</body>", whatsapp_html + "  </body>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    print("Updated index.html")

# Update Markdown files
md_dir = os.path.join('src', 'file-system', 'home', 'user', 'projects')
md_files = glob.glob(os.path.join(md_dir, '*.md'))

for md_file in md_files:
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Apply translations
    md_content = md_content.replace("Projet de Fin d'Études", "Graduation Project")
    md_content = md_content.replace("Projet Entrepreneurial", "Entrepreneurial Project")
    md_content = md_content.replace("Initiative Personnelle", "Personal Initiative")
    md_content = md_content.replace("Défi Technique Personnel", "Personal Technical Challenge")
    md_content = md_content.replace("Mission Professionnelle", "Professional Mission")
    md_content = md_content.replace("## Client — B Studio\n\n", "")
    md_content = md_content.replace("## Client — B Studio", "")
    
    # Specific file updates
    filename = os.path.basename(md_file)
    if filename == '07-eurafrtours-citronniers.md':
        md_content = re.sub(r'Site web unifié.*?Hostinger\.', "Unified website for a travel agency (Eurafatours) and a luxury rural lodge (Domaine des Citronniers) in Béni Khiar, Nabeul. 14 custom PHP pages with premium design. CI/CD deployment via GitHub Actions → Hostinger.", md_content, flags=re.DOTALL)
        md_content = re.sub(r'Features:\n.*', '', md_content, flags=re.DOTALL)
    elif filename == '09-camp-abdelmoula.md':
        md_content = re.sub(r'Site web pour un camp.*?Voyages\.', "Website for a luxury camp in the heart of the Tunisian Sahara in Tembaine, Douz. 51 tents including 27 royal ones. Cinematic design inspired by the desert with a sand/gold/night palette. Cross-branding with Défi du Désert Voyages.", md_content, flags=re.DOTALL)
        md_content = re.sub(r'Features:\n(?:- .*\n)*', '', md_content, flags=re.DOTALL)
        if 'https://camp-abdelmoula.com/' not in md_content:
            md_content += "\nLink: [https://camp-abdelmoula.com/](https://camp-abdelmoula.com/)\n"
    elif filename == '08-defidesert.md':
        md_content = re.sub(r'Refonte totale.*?premium\.', "Complete redesign of a static HTML website from 2010 for an agency specializing in 4x4 tours, Quad & SSV Raids, and camel treks in southern Tunisia. Cinematic adventure design.", md_content, flags=re.DOTALL)
        md_content = re.sub(r'Features:\n(?:- .*\n)*', '', md_content, flags=re.DOTALL)
        if 'defidesert.com' not in md_content:
             md_content += "\nLink: [https://defidesert.com/](https://defidesert.com/)\n"
    elif filename == '10-the-untold-layers.md':
        md_content = re.sub(r'Blog magazine.*?affiliation\.', "Multi-theme English magazine blog targeting an international audience. 9 categories: Lifestyle, Culture & Trends, Travel, Sports, Technology & AI, Entertainment, Fashion, Psychology, Digital Life. SEO strategy + AdSense monetization + affiliation.", md_content, flags=re.DOTALL)
        md_content = re.sub(r'Features:\n(?:- .*\n)*', '', md_content, flags=re.DOTALL)
        
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
print("Updated markdown files")
