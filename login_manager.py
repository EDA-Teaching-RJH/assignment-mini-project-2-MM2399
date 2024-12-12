import re
import csv

def main():
    session = login()
    if session is True:
        print ('Login successful.')
    else:
        print ('Login failed.')

def login(email = None, password = None):
    if email is None and password is None:
        while True:
            email = input('Enter email >').strip().lower()
            if check_email_exists(email) is True:
                password = input('Enter password >')
                if check_password_correct(email, password) is True:
                    return True
    if email is None:
        print ('Expected email in first parameter if using function parameters.')
        return False
    if password is None:
        print ('Expected password in second parameter if using function parameters.')
        return False
    return False

def check_email_syntax(email):
    email_syntax_key = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_syntax_key, email.strip().lower())

def check_password_syntax(password):
    password_syntax_key =  r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*\d).{8,}$'
    return re.match(password_syntax_key, password.strip())

def check_email_exists(email, file_name = 'logins.csv'):
    try:
        with open(file_name, 'r', newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip().lower() == email.strip().lower():
                    return True
                
    except FileNotFoundError:
        return False
    return False
         
def check_password_exists(password, file_name = 'logins.csv'):
    try:
        with open(file_name, 'r', newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1].strip() == password.strip():
                    return True
    
    except FileNotFoundError:
        return False
    
def check_email_valid(email):
    verify_email = check_email_syntax(email)
    if not verify_email:
        return None
    email_exists = check_email_exists(email)
    if email_exists:
        return False
    return True

def check_password_valid(password):
    password = password.strip()
    verify_password = check_password_syntax(password)
    if not verify_password:
        return None
    password_exists = check_password_exists(verify_password)
    if password_exists:
        return False
    return True

def check_password_correct(email, password, file_name = 'logins.csv'):
    try:
        with open(file_name, 'r', newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip().lower() == email.strip().lower():
                    if row[1].strip() == password.strip():
                        return True
    
    except FileNotFoundError:
        return False
    return False

def write_to_csv(email, password, file_name = 'logins.csv'):
    with open(file_name, 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow([email.strip().lower(), password.strip()])

def make_email(email = None):
    if email is None:
        while True:
            email = input('Enter email >').strip().lower()
            verify_email = check_email_valid(email)
            if verify_email is None:
                print('Email syntax not valid.') 
                continue
            elif not verify_email:
                print ('Email already exists.')
                continue
            return email
                
    verify = check_email_valid(email)
    if verify is None:
        raise NameError('Email syntax not valid.')
    return email.strip().lower()
        
def make_password(password = None):
    if password == None:
        while True:
            password = input('Enter password >').strip()
            verify_password = check_password_valid(password)
            if verify_password == None:
                print ('Password syntax invalid. Ensure it contains at least:')
                print ('-At least 1 capital letter\n-At least 1 Number\n-At least 1 symbol')
                continue
            return password.strip()
                
    verify = check_password_valid(password)
    if verify == None:
        raise NameError('Password syntax invalid.')
    return password  

def make_login(email = None, password = None):
    if email is None:
       email = make_email()
    else:
        email = email.strip().lower()
        email_check = check_email_valid(email)
    if password is None:
        password = make_password()
    else:
        password = password.strip()
        password_check = check_password_valid(password)

    try:
        if email_check is None:
            print('Invalid email syntax.')
            return
        elif not email_check:
            print('Email already exists.')
            return

        if password_check is None:
            print('Invalid password syntax.')
            return
        elif not password_check:
            print('Password already exists.')
            return
    except NameError:
        write_to_csv(email, password)
        print(f'Added {email} to database.')
    
if __name__ == '__main__':
    main()