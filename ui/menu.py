#All meny-logik och användargränssnitt
from services.file_handler import load_contacts, save_contacts
from models.contact import Contact
import re

def show_menu():
    #Funktion till en Startmeny för att välja olika alternativ inom telefonboken
    print("\n" + "="*40)
    print("TELEFONBOK")
    print("="*40)
    print("1. Lägg till kontakt")
    print("2. Sök efter kontakt")
    print("3. Uppdatera telefonnummer")
    print("4. Uppdatera email eller adress")
    print("5. Ändra namn på kontakt")
    print("6. Ta bort kontakt")
    print("7. Visa alla kontakter")
    print("8. Avsluta")
    print("="*40)

def validate_phone_number(phone_number):
    #Validerar att telefonnumret endast innehåller siffror, +, mellanslag och bindestreck
    pattern = r'^[\+\d\s\-]+$'
    return bool(re.match(pattern, phone_number))

def add_contact(contacts):
    #Funktion för att lägga till nya kontakter med frivillig email och adress
    name = input("Ange namn: ").strip()
    if not name:
        print("Namn kan inte vara tomt!")
        return
    
    #Kontrollera om namnet redan finns (case-insensitive)
    if name.lower() in contacts:
        print("Kontakten finns redan.") #Om namnet finns redan så läggs den inte till.
        return
    
    phone_number = input("Ange telefonnummer: ").strip()
    if not phone_number:
        print("Telefonnummer kan inte vara tomt!")
        return
    
    if not validate_phone_number(phone_number):
        print("Varning: Telefonnumret innehåller ogiltiga tecken. Endast siffror, +, mellanslag och bindestreck rekommenderas.")
    
    email = input("Ange email (valfritt, tryck Enter för att hoppa över): ").strip()
    address = input("Ange adress (valfritt, tryck Enter för att hoppa över): ").strip()
    
    contacts[name.lower()] = Contact(name, phone_number, email, address)
    save_contacts(contacts)
    print(f"Kontakt {name} har lagts till!") #Om namn inte finns läggs kontakten till med nummer

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
    
    if found: #Om namnet finns i telefonboken så skriver den ut telefonnummret
        print(f"\nHittade {len(found)} kontakt(er):")
        for contact in found:
            print(contact.basic_info())
            
        #Fråga om man vill se mer detaljer
        if len(found) == 1:
            visa_detaljer = input("\nVill du se fullständig information? (j/n): ").lower()
            if visa_detaljer == 'j':
                print(found[0])
    else:
        print("Kontakten finns inte.")

def update_phone_number(contacts):
    #Funktion för att uppdatera nummret hos kontakter
    name = input("Ange namn på kontakten du vill uppdatera: ").strip()
    if name.lower() in contacts: #Om namnet finns i telefonboken kan du uppdatera nummret
        contact = contacts[name.lower()]
        print(f"Nuvarande telefonnummer för {contact.name}: {contact.phone_number}")
        new_number = input("Ange nytt telefonnummer: ").strip()
        
        if not new_number:
            print("Telefonnummer kan inte vara tomt!")
            return
            
        if not validate_phone_number(new_number):
            print("Varning: Telefonnumret innehåller ogiltiga tecken.")
        
        contact.phone_number = new_number
        save_contacts(contacts)
        print(f"Telefonnumret för {contact.name} har uppdaterats!")
    else:
        print("Kontakten finns inte.")

def update_email_or_address(contacts):
    #Ny funktion för att uppdatera email eller adress
    name = input("Ange namn på kontakten du vill uppdatera: ").strip()
    if name.lower() in contacts:
        contact = contacts[name.lower()]
        print(f"\nNuvarande information för {contact.name}:")
        print(f"Email: {contact.email if contact.email else '(inte angivet)'}")
        print(f"Adress: {contact.address if contact.address else '(inte angivet)'}")
        
        print("\nVad vill du uppdatera?")
        print("1. Email")
        print("2. Adress")
        print("3. Båda")
        choice = input("Välj alternativ: ")
        
        if choice == "1":
            new_email = input("Ange ny email (tryck Enter för att ta bort): ").strip()
            contact.email = new_email
            print("Email har uppdaterats!")
        elif choice == "2":
            new_address = input("Ange ny adress (tryck Enter för att ta bort): ").strip()
            contact.address = new_address
            print("Adress har uppdaterats!")
        elif choice == "3":
            new_email = input("Ange ny email: ").strip()
            new_address = input("Ange ny adress: ").strip()
            contact.email = new_email
            contact.address = new_address
            print("Email och adress har uppdaterats!")
        else:
            print("Ogiltigt val!")
            return
        
        save_contacts(contacts)
    else:
        print("Kontakten finns inte.")

def change_contact_name(contacts):
    #Ny funktion för att ändra namn på en kontakt
    old_name = input("Ange nuvarande namn på kontakten: ").strip()
    if old_name.lower() in contacts:
        contact = contacts[old_name.lower()]
        print(f"Nuvarande namn: {contact.name}")
        new_name = input("Ange nytt namn: ").strip()
        
        if not new_name:
            print("Namn kan inte vara tomt!")
            return
            
        if new_name.lower() in contacts and new_name.lower() != old_name.lower():
            print("Det finns redan en kontakt med det namnet!")
            return
        
        #Ta bort gammal och lägg till ny med nytt namn
        del contacts[old_name.lower()]
        contact.name = new_name
        contacts[new_name.lower()] = contact
        save_contacts(contacts)
        print(f"Namnet har ändrats från {old_name} till {new_name}!")
    else:
        print("Kontakten finns inte.")

def remove_contact(contacts):
    #Funktion för att ta bort kontakter
    name = input("Ange namn på kontakten du vill ta bort: ").strip()
    if name.lower() in contacts:
        contact = contacts[name.lower()]
        print(f"\nKontaktinformation för {contact.name}:")
        print(contact.basic_info())
        confirm = input("Är du säker på att du vill ta bort denna kontakt? (j/n): ").lower()
        
        if confirm == 'j':
            del contacts[name.lower()] #Om namnet finns i contacts listan, så raderas den
            save_contacts(contacts)
            print(f"Kontakt {contact.name} har tagits bort!")
        else:
            print("Borttagning avbröts.")
    else:
        print("Kontakten finns inte.")

def show_all_contacts(contacts):
    #Funktion för att visa alla kontakter (sorterade)
    if contacts: #Skriver ut alla kontakter
        print("\n" + "="*40)
        print("ALLA KONTAKTER")
        print("="*40)
        #Sortera efter namn
        sorted_contacts = sorted(contacts.values(), key=lambda x: x.name.lower())
        for i, contact in enumerate(sorted_contacts, 1):
            print(f"{i}. {contact.basic_info()}")
        print("="*40)
        print(f"Totalt antal kontakter: {len(contacts)}")
        
        #Fråga om man vill se detaljer för någon kontakt
        show_details = input("\nVill du se detaljer för en kontakt? (ja/nej): ").lower()
        if show_details in ['ja', 'j']:
            name = input("Ange namn på kontakten: ").strip()
            if name.lower() in contacts:
                print(contacts[name.lower()])
            else:
                print("Kontakten finns inte.")
    else:
        print("Telefonboken är tom.")

def run_program():
    #Huvudprogrammet
    contacts = load_contacts()
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
            change_contact_name(contacts)
        elif choice == "6":
            remove_contact(contacts)
        elif choice == "7":
            show_all_contacts(contacts)
        elif choice == "8":
            print("Avslutar programmet...")
            break
        else:
            print("Ogiltigt val, försök igen.")