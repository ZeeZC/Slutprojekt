#All meny-logik och användargränssnitt
from services.file_handler import load_contacts, save_contacts
from models.contact import Contact
import re
from datetime import datetime

def show_menu():
    #Funktion till en Startmeny för att välja olika alternativ inom telefonboken
    print("\n" + "="*40)
    print("TELEFONBOK")
    print("="*40)
    print("1. Lägg till kontakt")
    print("2. Sök efter kontakt")
    print("3. Uppdatera telefonnummer")
    print("4. Uppdatera email eller adress")
    print("5. Uppdatera födelsedatum eller jobbtitel")
    print("6. Ändra namn på kontakt")
    print("7. Lägg till/redigera anteckningar")
    print("8. Ta bort kontakt")
    print("9. Visa alla kontakter")
    print("10. Avsluta")
    print("="*40)

def validate_phone_number(phone_number):
    #Validerar att telefonnumret endast innehåller siffror, +, mellanslag och bindestreck
    pattern = r'^[\+\d\s\-]+$'
    if not phone_number:
        return False
    return bool(re.match(pattern, phone_number))

def validate_email(email):
    #Validerar email-format
    if not email:
        return True  #Tomt är okej (valfritt)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_birth_date(birth_date):
    #Validerar födelsedatum (format YYYY-MM-DD)
    if not birth_date:
        return True  #Tomt är okej (valfritt)
    try:
        datetime.strptime(birth_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def select_contact_by_name(contacts, name):
    #Hjälpfunktion: Visa alla kontakter med ett visst namn och låt användaren välja
    matching = [c for c in contacts.values() if c.name.lower() == name.lower()]
    
    if not matching:
        return None
    
    if len(matching) == 1:
        return matching[0]
    
    #Flera kontakter med samma namn
    print(f"\n⚠️ Det finns {len(matching)} kontakter med namnet '{name}':")
    for i, contact in enumerate(matching, 1):
        print(f"  {i}. {contact.basic_info()}")
    
    while True:
        try:
            val = input("Välj vilken kontakt du menar (ange nummer): ")
            if not val:
                return None
            idx = int(val) - 1
            if 0 <= idx < len(matching):
                return matching[idx]
            else:
                print("Ogiltigt val, försök igen.")
        except ValueError:
            print("Ange ett giltigt nummer!")
        except KeyboardInterrupt:
            return None

def get_contact_by_id(contacts):
    #Hjälpfunktion: Hämta kontakt via ID
    try:
        contact_id = int(input("Ange kontaktens ID: "))
        if contact_id in contacts:
            return contacts[contact_id]
        else:
            print(f"❌ Ingen kontakt med ID {contact_id} hittades.")
            return None
    except ValueError:
        print("❌ Ogiltigt ID! Ange ett nummer.")
        return None

def add_contact(contacts):
    #Funktion för att lägga till nya kontakter med alla fält
    name = input("Ange namn: ").strip()
    if not name:
        print("Namn kan inte vara tomt!")
        return
    
    #Telefonnummer (obligatoriskt)
    while True:
        phone_number = input("Ange telefonnummer: ").strip()
        if not phone_number:
            print("Telefonnummer kan inte vara tomt!")
            continue
        if not validate_phone_number(phone_number):
            print("Fel: Telefonnumret får bara innehålla siffror, +, mellanslag och bindestreck.")
            continue
        break
    
    #Email (valfritt med validering)
    while True:
        email = input("Ange email (valfritt, tryck Enter för att hoppa över): ").strip()
        if not validate_email(email):
            print("Fel: Ogiltig email-format. Exempel: namn@domän.se")
            continue
        break
    
    address = input("Ange adress (valfritt, tryck Enter för att hoppa över): ").strip()
    
    #Födelsedatum (valfritt med validering)
    while True:
        birth_date = input("Ange födelsedatum (YYYY-MM-DD, valfritt, tryck Enter för att hoppa över): ").strip()
        if not birth_date:
            break
        if not validate_birth_date(birth_date):
            print("Fel: Ogiltigt datumformat. Använd YYYY-MM-DD (exempel: 1990-05-15)")
            continue
        break
    
    job_title = input("Ange jobbtitel (valfritt, tryck Enter för att hoppa över): ").strip()
    notes = input("Ange anteckningar (valfritt, tryck Enter för att hoppa över): ").strip()
    
    new_contact = Contact(name, phone_number, email, address, birth_date, job_title, notes)
    contacts[new_contact.contact_id] = new_contact
    save_contacts(contacts)
    print(f"\n✅ Kontakt {name} har lagts till med ID {new_contact.contact_id}!")

def search_contact(contacts):
    #Funktion för att söka efter kontakter (delsträngssökning)
    search_term = input("Ange namn eller del av namn att söka efter: ").strip().lower()
    if not search_term:
        print("Ange ett sökord!")
        return
    
    found = []
    for contact in contacts.values():
        if search_term in contact.name.lower():
            found.append(contact)
    
    if found:
        print(f"\n🔍 Hittade {len(found)} kontakt(er):")
        for contact in found:
            print(f"  {contact.basic_info()}")
            
        #Fråga om man vill se mer detaljer
        visa_detaljer = input("\nVill du se fullständig information för någon kontakt? (j/n): ").lower()
        if visa_detaljer == 'j':
            selected = get_contact_by_id(contacts)
            if selected:
                print(selected)
    else:
        print("❌ Ingen kontakt hittades.")

def update_phone_number(contacts):
    #Funktion för att uppdatera nummret hos kontakter
    name = input("Ange namn på kontakten du vill uppdatera: ").strip()
    if not name:
        print("Ange ett namn!")
        return
    
    contact = select_contact_by_name(contacts, name)
    if not contact:
        print("❌ Kontakten finns inte.")
        return
    
    print(f"Nuvarande telefonnummer för {contact.name}: {contact.phone_number}")
    
    while True:
        new_number = input("Ange nytt telefonnummer: ").strip()
        if not new_number:
            print("Telefonnummer kan inte vara tomt!")
            continue
        if not validate_phone_number(new_number):
            print("Fel: Telefonnumret får bara innehålla siffror, +, mellanslag och bindestreck.")
            continue
        break
    
    contact.phone_number = new_number
    save_contacts(contacts)
    print(f"✅ Telefonnumret för {contact.name} (ID {contact.contact_id}) har uppdaterats!")

def update_email_or_address(contacts):
    #Funktion för att uppdatera email eller adress
    name = input("Ange namn på kontakten du vill uppdatera: ").strip()
    if not name:
        print("Ange ett namn!")
        return
    
    contact = select_contact_by_name(contacts, name)
    if not contact:
        print("❌ Kontakten finns inte.")
        return
    
    print(f"\n📋 Nuvarande information för {contact.name} (ID {contact.contact_id}):")
    print(f"Email: {contact.email if contact.email else '(inte angivet)'}")
    print(f"Adress: {contact.address if contact.address else '(inte angivet)'}")
    
    print("\nVad vill du uppdatera?")
    print("1. Email")
    print("2. Adress")
    print("3. Båda")
    choice = input("Välj alternativ: ")
    
    if choice == "1":
        while True:
            new_email = input("Ange ny email (tryck Enter för att ta bort): ").strip()
            if not validate_email(new_email):
                print("Fel: Ogiltig email-format.")
                continue
            break
        contact.email = new_email
        print("✅ Email har uppdaterats!")
    elif choice == "2":
        new_address = input("Ange ny adress (tryck Enter för att ta bort): ").strip()
        contact.address = new_address
        print("✅ Adress har uppdaterats!")
    elif choice == "3":
        while True:
            new_email = input("Ange ny email: ").strip()
            if not validate_email(new_email):
                print("Fel: Ogiltig email-format.")
                continue
            break
        new_address = input("Ange ny adress: ").strip()
        contact.email = new_email
        contact.address = new_address
        print("✅ Email och adress har uppdaterats!")
    else:
        print("Ogiltigt val!")
        return
    
    save_contacts(contacts)

def update_birth_date_or_job_title(contacts):
    #Funktion för att uppdatera födelsedatum eller jobbtitel
    name = input("Ange namn på kontakten du vill uppdatera: ").strip()
    if not name:
        print("Ange ett namn!")
        return
    
    contact = select_contact_by_name(contacts, name)
    if not contact:
        print("❌ Kontakten finns inte.")
        return
    
    print(f"\n📋 Nuvarande information för {contact.name} (ID {contact.contact_id}):")
    print(f"Födelsedatum: {contact.birth_date if contact.birth_date else '(inte angivet)'}")
    print(f"Jobbtitel: {contact.job_title if contact.job_title else '(inte angivet)'}")
    
    print("\nVad vill du uppdatera?")
    print("1. Födelsedatum")
    print("2. Jobbtitel")
    print("3. Båda")
    choice = input("Välj alternativ: ")
    
    if choice == "1":
        while True:
            new_birth_date = input("Ange nytt födelsedatum (YYYY-MM-DD, tryck Enter för att ta bort): ").strip()
            if not new_birth_date:
                break
            if not validate_birth_date(new_birth_date):
                print("Fel: Ogiltigt datumformat. Använd YYYY-MM-DD")
                continue
            break
        contact.birth_date = new_birth_date
        print("✅ Födelsedatum har uppdaterats!")
    elif choice == "2":
        new_job_title = input("Ange ny jobbtitel (tryck Enter för att ta bort): ").strip()
        contact.job_title = new_job_title
        print("✅ Jobbtitel har uppdaterats!")
    elif choice == "3":
        while True:
            new_birth_date = input("Ange nytt födelsedatum (YYYY-MM-DD): ").strip()
            if not validate_birth_date(new_birth_date):
                print("Fel: Ogiltigt datumformat. Använd YYYY-MM-DD")
                continue
            break
        new_job_title = input("Ange ny jobbtitel: ").strip()
        contact.birth_date = new_birth_date
        contact.job_title = new_job_title
        print("✅ Födelsedatum och jobbtitel har uppdaterats!")
    else:
        print("Ogiltigt val!")
        return
    
    save_contacts(contacts)

def update_notes(contacts):
    #Funktion för att lägga till/redigera anteckningar
    name = input("Ange namn på kontakten du vill redigera anteckningar för: ").strip()
    if not name:
        print("Ange ett namn!")
        return
    
    contact = select_contact_by_name(contacts, name)
    if not contact:
        print("❌ Kontakten finns inte.")
        return
    
    print(f"\n📝 Nuvarande anteckningar för {contact.name} (ID {contact.contact_id}):")
    print(contact.notes if contact.notes else "(inga anteckningar)")
    
    new_notes = input("\nAnge nya anteckningar (tryck Enter för att ta bort alla): ").strip()
    contact.notes = new_notes
    save_contacts(contacts)
    print("✅ Anteckningar har uppdaterats!")

def change_contact_name(contacts):
    #Funktion för att ändra namn på en kontakt
    name = input("Ange nuvarande namn på kontakten: ").strip()
    if not name:
        print("Ange ett namn!")
        return
    
    contact = select_contact_by_name(contacts, name)
    if not contact:
        print("❌ Kontakten finns inte.")
        return
    
    print(f"Nuvarande namn: {contact.name} (ID {contact.contact_id})")
    new_name = input("Ange nytt namn: ").strip()
    
    if not new_name:
        print("Namn kan inte vara tomt!")
        return
    
    contact.name = new_name
    save_contacts(contacts)
    print(f"✅ Namnet har ändrats till {new_name} (ID {contact.contact_id})!")

def remove_contact(contacts):
    #Funktion för att ta bort kontakter
    name = input("Ange namn på kontakten du vill ta bort: ").strip()
    if not name:
        print("Ange ett namn!")
        return
    
    contact = select_contact_by_name(contacts, name)
    if not contact:
        print("❌ Kontakten finns inte.")
        return
    
    print(f"\n📋 Kontaktinformation för {contact.name} (ID {contact.contact_id}):")
    print(contact)
    confirm = input("Är du säker på att du vill ta bort denna kontakt? (j/n): ").lower()
    
    if confirm == 'j':
        del contacts[contact.contact_id]
        save_contacts(contacts)
        print(f"✅ Kontakt {contact.name} (ID {contact.contact_id}) har tagits bort!")
    else:
        print("Borttagning avbröts.")

def show_all_contacts(contacts):
    #Funktion för att visa alla kontakter (sorterade efter namn)
    if contacts:
        print("\n" + "="*40)
        print("📒 ALLA KONTAKTER")
        print("="*40)
        #Sortera efter namn
        sorted_contacts = sorted(contacts.values(), key=lambda x: x.name.lower())
        for contact in sorted_contacts:
            #Visa om kontakt har födelsedag snart (inom 30 dagar)
            age_info = ""
            if contact.birth_date:
                today = datetime.now()
                try:
                    birth = datetime.strptime(contact.birth_date, "%Y-%m-%d")
                    #Kolla om födelsedagen är inom 30 dagar
                    next_birthday = birth.replace(year=today.year)
                    if next_birthday < today:
                        next_birthday = next_birthday.replace(year=today.year + 1)
                    days_until = (next_birthday - today).days
                    if days_until <= 30:
                        age_info = " 🎂"
                except:
                    pass
            print(f"  {contact.basic_info()}{age_info}")
        print("="*40)
        print(f"📊 Totalt antal kontakter: {len(contacts)}")
        
        #Fråga om man vill se detaljer för någon kontakt
        show_details = input("\nVill du se detaljer för en kontakt? (ja/nej): ").lower()
        if show_details in ['ja', 'j']:
            selected = get_contact_by_id(contacts)
            if selected:
                print(selected)
    else:
        print("📭 Telefonboken är tom.")

def run_program():
    #Huvudprogrammet
    contacts = load_contacts()
    print(f"\n📞 Välkommen till Telefonboken!")
    print(f"📁 Laddade {len(contacts)} kontakter från filen.")
    
    while True:
        show_menu()
        choice = input("Välj ett alternativ: ")
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact(contacts)
        elif choice == "3":
            update_phone_number(contacts)
        elif choice == "4":
            update_email_or_address(contacts)
        elif choice == "5":
            update_birth_date_or_job_title(contacts)
        elif choice == "6":
            change_contact_name(contacts)
        elif choice == "7":
            update_notes(contacts)
        elif choice == "8":
            remove_contact(contacts)
        elif choice == "9":
            show_all_contacts(contacts)
        elif choice == "10":
            print("👋 Avslutar programmet...")
            print(f"💾 {len(contacts)} kontakter sparades.")
            break
        else:
            print("❌ Ogiltigt val, försök igen.")