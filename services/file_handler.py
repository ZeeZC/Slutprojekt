#Hantering av CSV-fil för kontakter
import csv
import os
from models.contact import Contact

FILENAME = "data/telefonbok.csv"

def load_contacts():
    #Laddar alla kontakter från CSV-fil
    contacts = {}  #Använder ID som nyckel istället för namn
    
    #Skapa data-mappen om den inte finns
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:  #Minst ID och namn
                    contact = Contact.from_tuple(row)
                    contacts[contact.contact_id] = contact  #Lagrar med ID som nyckel
    
    #Uppdatera nästa lediga ID baserat på laddade kontakter
    Contact.set_next_id_from_contacts(contacts)
    return contacts

def save_contacts(contacts):
    #Sparar alla kontakter till CSV-fil
    
    #Skapa data-mappen om den inte finns
    os.makedirs("data", exist_ok=True)
    
    with open(FILENAME, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for contact in contacts.values():
            writer.writerow(contact.to_tuple())