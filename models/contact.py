#Modell för en kontakt med utökad information
from datetime import datetime
import re

class Contact:
    def __init__(self, name, phone_number, email="", address="", birth_date="", job_title="", notes=""):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birth_date = birth_date
        self.job_title = job_title
        self.notes = notes
    
    def to_tuple(self):
        #Gör om kontakten till tuple för CSV-sparning (7 fält nu)
        return (self.name, self.phone_number, self.email, self.address, 
                self.birth_date, self.job_title, self.notes)
    
    def __str__(self):
        #Visar kontaktinformation snyggt
        result = f"\n{'='*40}"
        result += f"\n{self.name.upper()}"
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
        #Visar bara namn och telefon (för listvy)
        return f"{self.name}: {self.phone_number}"
    
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
        if len(tuple_data) == 2:
            return Contact(tuple_data[0], tuple_data[1], "", "", "", "", "")
        elif len(tuple_data) == 3:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], "", "", "", "")
        elif len(tuple_data) == 4:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], "", "", "")
        elif len(tuple_data) == 5:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], 
                          tuple_data[4], "", "")
        elif len(tuple_data) == 6:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], 
                          tuple_data[4], tuple_data[5], "")
        else:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3], 
                          tuple_data[4], tuple_data[5], tuple_data[6])