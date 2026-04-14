#Modell för en kontakt (kommer att utökas med adress, email etc)
class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
    
    def to_tuple(self):
        #Gör om kontakten till tuple för CSV-sparning
        return (self.name, self.phone_number)
    
    def __str__(self):
        return f"{self.name}: {self.phone_number}"
    
    @staticmethod
    def from_tuple(tuple_data):
        #Skapar en kontakt från en tuple (namn, telefonnummer)
        return Contact(tuple_data[0], tuple_data[1])