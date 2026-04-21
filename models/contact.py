#Modell för en kontakt med utökad information
class Contact:
    def __init__(self, name, phone_number, email="", address=""):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
    
    def to_tuple(self):
        #Gör om kontakten till tuple för CSV-sparning (5 fält nu)
        return (self.name, self.phone_number, self.email, self.address)
    
    def __str__(self):
        #Visar kontaktinformation snyggt
        result = f"\n--- {self.name} ---"
        result += f"\nTelefon: {self.phone_number}"
        if self.email:
            result += f"\nEmail: {self.email}"
        if self.address:
            result += f"\nAdress: {self.address}"
        result += "\n" + "-" * 20
        return result
    
    def basic_info(self):
        #Visar bara namn och telefon (för listvy)
        return f"{self.name}: {self.phone_number}"
    
    @staticmethod
    def from_tuple(tuple_data):
        #Skapar en kontakt från en tuple (namn, telefon, email, adress)
        #Hanterar gamla filer som bara har 2 fält
        if len(tuple_data) == 2:
            return Contact(tuple_data[0], tuple_data[1], "", "")
        elif len(tuple_data) == 3:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], "")
        else:
            return Contact(tuple_data[0], tuple_data[1], tuple_data[2], tuple_data[3])