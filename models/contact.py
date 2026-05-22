#Modell för en kontakt med utökad information
from datetime import datetime
import re

class Contact:
    _next_id = 1  #Klassvariabel för att hålla koll på nästa lediga ID
    
    def __init__(self, name, phone_number, email="", address="", birth_date="", job_title="", notes="", contact_id=None):
        #Om inget ID anges, skapa ett nytt unikt ID
        if contact_id is None:
            self.contact_id = Contact._next_id
            Contact._next_id += 1
        else:
            self.contact_id = contact_id
            #Uppdatera _next_id om det behövs
            if contact_id >= Contact._next_id:
                Contact._next_id = contact_id + 1
        
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birth_date = birth_date
        self.job_title = job_title
        self.notes = notes
    
    def to_tuple(self):
        #Gör om kontakten till tuple för CSV-sparning (8 fält nu: ID först)
        return (str(self.contact_id), self.name, self.phone_number, self.email, 
                self.address, self.birth_date, self.job_title, self.notes)
    
    def __str__(self):
        #Visar kontaktinformation snyggt
        result = f"\n{'='*40}"
        result += f"\n{self.name.upper()} (ID: {self.contact_id})"
        result += f"\n{'='*40}"
        result += f"\n📞 Telefon: {self.phone_number}"
        if self.email:
            result += f"\n✉️ Email: {self.email}"
        if self.address:
            result += f"\n🏠 Adress: {self.address}"
        if self.birth_date:
            result += f"\n🎂 Födelsedatum: {self.birth_date}"
            #Räkna ut ålder
            age = self.calculate_age()
            if age:
                result += f" ({age} år)"
        if self.job_title:
            result += f"\n💼 Jobbtitel: {self.job_title}"
        if self.notes:
            result += f"\n📝 Anteckningar: {self.notes}"
        result += f"\n{'='*40}"
        return result
    
    def basic_info(self):
        #Visar grundläggande info (för listvy)
        return f"ID {self.contact_id}: {self.name} - {self.phone_number}"
    
    def calculate_age(self):
        #Räknar ut ålder från födelsedatum
        if not self.birth_date:
            return None
        try:
            #Förväntar format YYYY-MM-DD
            birth = datetime.strptime(self.birth_date, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth.year
            #Kolla om födelsedagen har passerats i år
            if (today.month, today.day) < (birth.month, birth.day):
                age -= 1
            return age
        except:
            return None
    
    @staticmethod
    def from_tuple(tuple_data):
        #Skapar en kontakt från en tuple (hanterar olika versioner)
        #Ny version med ID först
        if len(tuple_data) == 8:
            return Contact(tuple_data[1], tuple_data[2], tuple_data[3], tuple_data[4],
                          tuple_data[5], tuple_data[6], tuple_data[7], int(tuple_data[0]))
        #Gamla versioner utan ID (för bakåtkompatibilitet)
        elif len(tuple_data) == 2:
            return Contact(tuple_data[0], tuple_data[1], "", "", "", "", "", None)
        elif len(tuple_data) == 3:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], "", "", "", "", None)
        elif len(tuple_data) == 4:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], "", "", "", None)
        elif len(tuple_data) == 5:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], 
                          tuple_data[4], "", "", None)
        elif len(tuple_data) == 6:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], 
                          tuple_data[4], tuple_data[5], "", None)
        elif len(tuple_data) == 7:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], 
                          tuple_data[4], tuple_data[5], tuple_data[6], None)
        else:
            return Contact("Unknown", "000", "", "", "", "", "", None)

    @staticmethod
    def set_next_id_from_contacts(contacts):
        #Uppdaterar _next_id baserat på befintliga kontakter (anropas vid laddning)
        if contacts:
            max_id = max(contact.contact_id for contact in contacts.values())
            Contact._next_id = max_id + 1