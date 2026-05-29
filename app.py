#Flask webbapplikation för telefonboken - Här startar du programmet!
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from services.file_handler import load_contacts, save_contacts
from models.contact import Contact
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'din_hemliga_nyckel_här_123'  #Behövs för flash-meddelanden

def validate_phone_number(phone_number):
    pattern = r'^[\+\d\s\-]+$'
    if not phone_number:
        return False
    return bool(re.match(pattern, phone_number))

def validate_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_birth_date(birth_date):
    if not birth_date:
        return True
    try:
        datetime.strptime(birth_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@app.route('/')
def index():
    #Hemsida - visa alla kontakter
    contacts = load_contacts()
    return render_template('index.html', contacts=contacts.values())

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    #Lägg till ny kontakt
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        birth_date = request.form.get('birth_date', '').strip()
        job_title = request.form.get('job_title', '').strip()
        notes = request.form.get('notes', '').strip()
        
        #Validering
        errors = []
        if not name:
            errors.append("Namn kan inte vara tomt")
        if not phone_number:
            errors.append("Telefonnummer kan inte vara tomt")
        elif not validate_phone_number(phone_number):
            errors.append("Ogiltigt telefonnummerformat")
        if email and not validate_email(email):
            errors.append("Ogiltig email-format")
        if birth_date and not validate_birth_date(birth_date):
            errors.append("Ogiltigt datumformat (använd YYYY-MM-DD)")
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add_contact.html')
        
        #Skapa och spara kontakt
        contacts = load_contacts()
        new_contact = Contact(name, phone_number, email, address, birth_date, job_title, notes)
        contacts[new_contact.contact_id] = new_contact
        save_contacts(contacts)
        
        flash(f"Kontakt {name} har lagts till med ID {new_contact.contact_id}!", 'success')
        return redirect(url_for('index'))
    
    return render_template('add_contact.html')

@app.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    #Redigera befintlig kontakt
    contacts = load_contacts()
    
    if contact_id not in contacts:
        flash("Kontakten finns inte!", 'error')
        return redirect(url_for('index'))
    
    contact = contacts[contact_id]
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        birth_date = request.form.get('birth_date', '').strip()
        job_title = request.form.get('job_title', '').strip()
        notes = request.form.get('notes', '').strip()
        
        #Validering
        errors = []
        if not name:
            errors.append("Namn kan inte vara tomt")
        if not phone_number:
            errors.append("Telefonnummer kan inte vara tomt")
        elif not validate_phone_number(phone_number):
            errors.append("Ogiltigt telefonnummerformat")
        if email and not validate_email(email):
            errors.append("Ogiltig email-format")
        if birth_date and not validate_birth_date(birth_date):
            errors.append("Ogiltigt datumformat (använd YYYY-MM-DD)")
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('edit_contact.html', contact=contact)
        
        #Uppdatera kontakt
        contact.name = name
        contact.phone_number = phone_number
        contact.email = email
        contact.address = address
        contact.birth_date = birth_date
        contact.job_title = job_title
        contact.notes = notes
        
        save_contacts(contacts)
        flash(f"Kontakt {name} har uppdaterats!", 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_contact.html', contact=contact)

@app.route('/delete/<int:contact_id>')
def delete_contact(contact_id):
    #Ta bort kontakt
    contacts = load_contacts()
    
    if contact_id in contacts:
        contact_name = contacts[contact_id].name
        del contacts[contact_id]
        save_contacts(contacts)
        flash(f"Kontakt {contact_name} har tagits bort!", 'success')
    else:
        flash("Kontakten finns inte!", 'error')
    
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    #Sök efter kontakter - FÖRBÄTTRAD VERSION!
    results = []
    query = ""
    search_type = "name"  # name, phone, email, job
    
    if request.method == 'POST':
        query = request.form.get('query', '').strip().lower()
        search_type = request.form.get('search_type', 'name')
        contacts = load_contacts()
        
        if query:
            for contact in contacts.values():
                if search_type == "name":
                    if query in contact.name.lower():
                        results.append(contact)
                elif search_type == "phone":
                    if query in contact.phone_number.lower():
                        results.append(contact)
                elif search_type == "email":
                    if query in contact.email.lower():
                        results.append(contact)
                elif search_type == "job":
                    if query in contact.job_title.lower():
                        results.append(contact)
                elif search_type == "all":
                    if (query in contact.name.lower() or 
                        query in contact.phone_number.lower() or 
                        query in contact.email.lower() or 
                        query in contact.job_title.lower() or
                        query in contact.notes.lower()):
                        results.append(contact)
    
    return render_template('search.html', query=query, results=results, search_type=search_type)

@app.route('/api/contacts')
def api_contacts():
    #API endpoint för att hämta alla kontakter (för AJAX)
    contacts = load_contacts()
    contacts_list = []
    for contact in contacts.values():
        contacts_list.append({
            'id': contact.contact_id,
            'name': contact.name,
            'phone': contact.phone_number,
            'email': contact.email,
            'address': contact.address,
            'birth_date': contact.birth_date,
            'job_title': contact.job_title,
            'notes': contact.notes
        })
    return jsonify(contacts_list)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)