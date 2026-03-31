import csv
import os

#TELEFONBOK (Beta-version för tillfället...)

FILNAMN = "telefonbok.csv"  #Namn på filen där kontakter sparas

#Funktion för att ladda kontakter från CSV-fil
def ladda_kontakter():
    my_dict = {}
    if os.path.exists(FILNAMN):
        with open(FILNAMN, 'r', encoding='utf-8') as fil:
            lasare = csv.reader(fil)
            for rad in lasare:
                if len(rad) == 2:
                    namn, nummer = rad
                    my_dict[namn] = nummer
    return my_dict

#Funktion för att spara kontakter till CSV-fil
def spara_kontakter(my_dict):
    with open(FILNAMN, 'w', encoding='utf-8', newline='') as fil:
        skrivare = csv.writer(fil)
        for namn, nummer in my_dict.items():
            skrivare.writerow([namn, nummer])

#Funktion till en Startmeny för att välja olika alternativ inom telefonboken 
def menu():
    print("\nTelefonbok")
    print("1. Lägg till kontakt")
    print("2. Sök efter kontakt")
    print("3. Uppdatera telefonnummer")
    print("4. Ta bort kontakt")
    print("5. Visa alla kontakter")
    print("6. Avsluta")

#Funktion för att lägga till nya kontakter
def add_contact(my_dict):
    namn = input("Ange namn: ")
    nummer = input("Ange telefonnummer: ")
    if namn in my_dict:
        print("Kontakten finns redan.") #Om namnet finns redan så läggs den inte till.
    else:
        my_dict[namn] = nummer
        spara_kontakter(my_dict)  #Sparar direkt till CSV-fil
        print(f"Kontakt {namn} har lagts till!") #Om namn inte finns läggs kontakten till med nummer

#Funktion för att söka efter kontakter
def search_contact(my_dict):
    namn = input("Ange namn att söka efter: ")
    if namn in my_dict: #Om namnet finns i telefonboken så skriver den ut telefonnummret
        print(f"{namn}: {my_dict[namn]}")
    else:
        print("Kontakten finns inte.")

#Funktion för att uppdatera nummret hos kontakter
def uppdate_number(my_dict):
    namn = input("Ange namn på kontakten du vill uppdatera: ")
    if namn in my_dict: #Om namnet finns i telefonboken kan du uppdatera nummret
        nytt_nummer = input("Ange nytt telefonnummer: ")
        my_dict[namn] = nytt_nummer
        spara_kontakter(my_dict)  #Sparar ändringen till CSV-fil
        print(f"Telefonnumret för {namn} har uppdaterats!")
    else:
        print("Kontakten finns inte.")

#Funktion för att ta bort kontakter
def remove_contact(my_dict):
    namn = input("Ange namn på kontakten du vill ta bort: ")
    if namn in my_dict:
        del my_dict[namn] #Om namnet finns i my_dict listan, så raderas den
        spara_kontakter(my_dict)  #Sparar ändringen till CSV-fil
        print(f"Kontakt {namn} har tagits bort!")
    else:
        print("Kontakten finns inte.") 

#Funktion för att visa alla kontakter
def show_all_contacts(my_dict):
    if my_dict: #Skriver ut alla kontakter
        print("\nAlla kontakter:")
        for namn, nummer in my_dict.items():
            print(f"{namn}: {nummer}")
    else:
        print("Telefonboken är tom.")

#Huvudprogrammet
def main_program():
    my_dict = ladda_kontakter()  #Laddar befintliga kontakter från CSV-fil
    while True:
        menu() #Använder sig av alternativen i menu() funktionen
        val = input("Välj ett alternativ: ")
        if val == "1":
            add_contact(my_dict)
        elif val == "2":
            search_contact(my_dict)
        elif val == "3":
            uppdate_number(my_dict)
        elif val == "4":
            remove_contact(my_dict)
        elif val == "5":
            show_all_contacts(my_dict)
        elif val == "6":
            print("Avslutar programmet...")
            break
        else:
            print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    main_program()