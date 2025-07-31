from bs4 import BeautifulSoup

def parse_arma3_modlist_table(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    mod_entries = []

    for row in soup.find_all('tr', attrs={'data-type': 'ModContainer'}):
        name_tag = row.find('td', attrs={'data-type': 'DisplayName'})
        link_tag = row.find('a', attrs={'data-type': 'Link'})

        if name_tag and link_tag:
            name = name_tag.get_text(strip=True)
            url = link_tag['href']
            mod_id = url.split('id=')[-1] if 'id=' in url else None

            mod_entries.append({
                'name': name,
                'id': mod_id,
                'url': url
            })

    return mod_entries

# Example usage
if __name__ == '__main__':
    modlist = parse_arma3_modlist_table('3rdID Workshop(18).html')
    for mod in modlist:
        print(f"{mod['name']} - ID: {mod['id']}")

