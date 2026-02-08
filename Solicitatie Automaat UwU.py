import requests
from bs4 import BeautifulSoup
import json
import html
import re

def clean_text(text):
    if not text: return "Niet vermeld"
    # Clean up whitespace and standard formatting
    return " ".join(text.split()).strip()

def scrape_vacancy(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # --- 1. JSON-LD Extraction ---
    json_ld_script = soup.find('script', type='application/ld+json')
    job_data = {}
    if json_ld_script:
        try:
            data = json.loads(json_ld_script.string)
            graph = data.get("@graph", [data])
            for item in graph:
                if item.get("@type") == "JobPosting":
                    job_data = item
                    break
        except:
            pass

    # --- 2. Improved Label Logic ---
    def get_info_by_label(label_text):
        # Look for labels specifically inside <strong> tags
        label_tag = soup.find('strong', string=re.compile(label_text, re.I))
        if label_tag:
            # Check the next sibling or parent text container
            parent = label_tag.find_parent('div')
            if parent:
                # Remove the label part and clean the rest
                val = parent.get_text(separator=" ").replace(label_tag.get_text(), "").strip()
                # If the result starts with a colon or whitespace, clean it
                val = re.sub(r'^[:\s]+', '', val)
                return clean_text(val)
        return None

    # Extraction
    contact_person_raw = get_info_by_label("Contact persoon")
    # Clean email from the contact person string if they are combined
    email = get_info_by_label("E-mail")
    contact_person = "Niet vermeld"
    
    if contact_person_raw:
        # If the email is inside the contact person string, separate them
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', contact_person_raw)
        if email_match and not email:
            email = email_match.group(0)
        # The person's name is usually the first line or bold part
        contact_person = contact_person_raw.split('E:')[0].strip()

    phone = get_info_by_label("Telefoonnummer")
    address = get_info_by_label("Adres")
    
    # Fallbacks
    if not phone: phone = job_data.get("jobLocation", {}).get("telephone", "Niet vermeld")
    if not address:
        addr = job_data.get("jobLocation", {}).get("address", {})
        address = f"{addr.get('streetAddress', '')}, {addr.get('postalCode', '')} {job_data.get('jobLocation', {}).get('name', '')}"

    # Fix recognition code regex (using raw string r"")
    recognition_code = "N/A"
    code_tag = soup.find(string=re.compile(r"ID \d+"))
    if code_tag:
        code_match = re.search(r"\d+", code_tag)
        if code_match:
            recognition_code = code_match.group()

    # Clean description HTML
    desc_val = job_data.get("description", "")
    clean_desc = re.sub(r'<[^<]+?>', '\n', desc_val)

    return {
        "url": url,
        "title": job_data.get("title", "Geen titel"),
        "text": html.unescape(clean_desc).strip(),
        "person": contact_person or "Niet vermeld",
        "phone": phone or "Niet vermeld",
        "email": email or "Niet vermeld",
        "address": address or "Niet vermeld",
        "code": recognition_code
    }

def main():
    print("--- 🎓 Keuzedeel Solliciteren Automator ---")
    student_nr = input("Voer je studentnummer in: ")
    full_name = input("Voer je voor- en achternaam in: ")
    
    # Filename exactly as requested
    filename = f"Keuzedeel Solliciteren {student_nr} {full_name}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Keuzedeel Solliciteren\n")
        f.write(f"**Naam:** {full_name}\n")
        f.write(f"**Studentnummer:** {student_nr}\n\n")
        f.write(f"---\n\n")

    count = 0
    max_vacancies = 8
    
    while count < max_vacancies:
        print(f"\n--- Vacature {count + 1} van {max_vacancies} ---")
        url = input("Paste de Stagemarkt URL (of type 'stop' om af te sluiten): ")
        
        if url.lower() == 'stop':
            break
            
        data = scrape_vacancy(url)
        
        if data:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"## Vacature {count + 1}: {data['title']}\n\n")
                f.write(f"1. **URL:** {data['url']}\n\n")
                f.write(f"2. **Vacature tekst:**\n{data['text']}\n\n")
                f.write(f"3. **Contactpersoon:** {data['person']}\n\n")
                f.write(f"4. **Telefoonnummer:** {data['phone']}\n\n")
                f.write(f"5. **E-mailadres:** {data['email']}\n\n")
                f.write(f"6. **Bezoekadres:** {data['address']}\n\n")
                f.write(f"### 🖋️ Reflectie\n")
                f.write(f"**a) Passend bij opleiding:** ...\n\n")
                f.write(f"**b) Erkenningscode:** `{data['code']}`\n\n")
                f.write(f"**c) Inhoud/Ontwikkelrichting:** ...\n\n")
                f.write(f"---\n\n")
            
            count += 1
            print(f"✅ Vacature {count} succesvol toegevoegd!")
        
    print(f"\n🎉 Klaar! Het bestand '{filename}' staat voor je klaar.")

if __name__ == "__main__":
    main()