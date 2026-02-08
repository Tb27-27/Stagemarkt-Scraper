import requests
from bs4 import BeautifulSoup
import json
import html
import re

def clean_html(raw_html):
    if not raw_html: return ""
    # Replace common HTML tags with newlines/markdown
    text = re.sub(r'<br\s*/?>', '\n', raw_html)
    text = re.sub(r'</p>', '\n\n', text)
    text = re.sub(r'<li>', '\n- ', text)
    text = re.sub(r'<[^<]+?>', '', text)
    return html.unescape(text).strip()

def scrape_vacancy(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error: Kon pagina niet ophalen. ({e})")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    json_ld_script = soup.find('script', type='application/ld+json')
    
    if not json_ld_script:
        print("❌ Error: Geen gestructureerde data gevonden op deze pagina.")
        return None

    data = json.loads(json_ld_script.string)
    job = {}
    
    # Extract JobPosting from Graph
    if "@graph" in data:
        for item in data["@graph"]:
            if item.get("@type") == "JobPosting":
                job = item
                break
    else:
        job = data

    # Get standard fields
    title = job.get("title", "Geen titel")
    description = clean_html(job.get("description", ""))
    skills = clean_html(job.get("skills", ""))
    full_text = f"{description}\n\n### Vaardigheden/Eisen:\n{skills}"
    
    # Get contact info
    loc = job.get("jobLocation", {})
    address_data = loc.get("address", {})
    address = f"{address_data.get('streetAddress', 'N/A')}, {address_data.get('postalCode', '')} {loc.get('name', '')}"
    phone = loc.get("telephone", "Niet vermeld")
    
    # The email is often hidden in the 'hiringOrganization' or the HTML itself
    email = "Niet vermeld (check website)"
    contact_person = "Niet vermeld"
    
    # Logic to find email/person in the HTML if not in JSON
    contact_section = soup.find('div', class_='text-sbb-body-sm')
    if contact_section:
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', contact_section.get_text())
        if email_match:
            email = email_match.group(0)
        
        person_tag = contact_section.find('strong')
        if person_tag:
            contact_person = person_tag.get_text()

    # Get Recognition Code (Leerbedrijf ID)
    recognition_code = "N/A"
    id_tag = soup.find(string=re.compile("Leerbedrijf ID"))
    if id_tag:
        recognition_code = id_tag.split("ID")[-1].strip()

    return {
        "url": url,
        "title": title,
        "text": full_text,
        "person": contact_person,
        "phone": phone,
        "email": email,
        "address": address,
        "code": recognition_code
    }

def main():
    print("--- 🎓 Keuzedeel Solliciteren Automator ---")
    student_nr = input("Voer je studentnummer in: ")
    full_name = input("Voer je voor- en achternaam in: ")
    
    filename = f"Keuzedeel Solliciteren {student_nr} {full_name}.md"
    count = 0

    print(f"\n✅ Bestand wordt aangemaakt: {filename}")
    
    while count < 8:
        print(f"\n--- Vacature {count + 1} van 8 ---")
        url = input("Paste de Stagemarkt URL (of type 'stop' om af te sluiten): ")
        
        if url.lower() == 'stop':
            break
            
        result = scrape_vacancy(url)
        
        if result:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"## Vacature {count + 1}: {result['title']}\n\n")
                f.write(f"1. **URL:** {result['url']}\n\n")
                f.write(f"2. **Vacature tekst:**\n{result['text']}\n\n")
                f.write(f"3. **Contactpersoon:** {result['person']}\n\n")
                f.write(f"4. **Telefoonnummer:** {result['phone']}\n\n")
                f.write(f"5. **E-mailadres:** {result['email']}\n\n")
                f.write(f"6. **Bezoekadres:** {result['address']}\n\n")
                f.write(f"### 🖋️ Persoonlijke Reflectie (Zelf invullen):\n")
                f.write(f"**a) Passend bij opleiding/afstudeerrichting:** \n*(Vul hier in waarom dit past bij jouw studie...)*\n\n")
                f.write(f"**b) Erkenningscode:** Het bedrijf heeft code: `{result['code']}`. \n\n")
                f.write(f"**c) Inhoud/Leerdoelen:** \n*(Vul hier in waarom dit de juiste ontwikkelrichting is voor jou...)*\n\n")
                f.write(f"---\n\n")
            
            count += 1
            print(f"✅ Vacature {count} succesvol toegevoegd aan het bestand!")
        
    print(f"\n🎉 Klaar! Je kunt nu '{filename}' openen, de reflectievragen beantwoorden en het opslaan als PDF.")

if __name__ == "__main__":
    main()