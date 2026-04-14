#All meny-logik och användargränssnitt
from services.file_handler import load_contacts, save_contacts
from models.contact import Contact

def show_menu():
    #Funktion till en Startmeny för att välja olika alternativ inom telefonboken
    print("\nTelefonbok")
    print("1. Lägg till kontakt")
    print("2. Sök efter kontakt")
    print("3. Uppdatera telefonnummer")
    print("4. Ta bort kontakt")
    print("5. Visa alla kontakter")
    print("6. Avsluta")

def add_contact(contacts):
    #Funktion för att lägga till nya kontakter
    name = input("Ange namn: ")
    phone_number = input("Ange telefonnummer: ")
    if name in contacts:
        print("Kontakten finns redan.") #Om namnet finns redan så läggs den inte till.
    else:
        contacts[name] = Contact(name, phone_number)
        save_contacts(contacts)
        print(f"Kontakt {name} har lagts till!") #Om namn inte finns läggs kontakten till med nummer

def search_contact(contacts):
    #Funktion för att söka efter kontakter
    name = input("Ange namn att söka efter: ")
    if name in contacts: #Om namnet finns i telefonboken så skriver den ut telefonnummret
        print(contacts[name])
    else:
        print("Kontakten finns inte.")

def update_phone_number(contacts):
    #Funktion för att uppdatera nummret hos kontakter
    name = input("Ange namn på kontakten du vill uppdatera: ")
    if name in contacts: #Om namnet finns i telefonboken kan du uppdatera nummret
        new_number = input("Ange nytt telefonnummer: ")
        contacts[name].phone_number = new_number
        save_contacts(contacts)
        print(f"Telefonnumret för {name} har uppdaterats!")
    else:
        print("Kontakten finns inte.")

def remove_contact(contacts):
    #Funktion för att ta bort kontakter
    name = input("Ange namn på kontakten du vill ta bort: ")
    if name in contacts:
        del contacts[name] #Om namnet finns i contacts listan, så raderas den
        save_contacts(contacts)
        print(f"Kontakt {name} har tagits bort!")
    else:
        print("Kontakten finns inte.")

def show_all_contacts(contacts):
    #Funktion för att visa alla kontakter
    if contacts: #Skriver ut alla kontakter
        print("\nAlla kontakter:")
        for contact in contacts.values():
            print(contact)
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
        elif choice == "3"):
            update_phone_number(contacts)
        elif choice == "4":
            remove_contact(contacts)
        elif choice == "5":
            show_all_contacts(contacts)
        elif choice == "6":
            print("Avslutar programmet...")
            break
        else:
            print("Ogiltigt val, försök igen.")