import re
import csv

login_csv = 'logins.csv' #Define CSV to use globally.

def main():
    '''
    Runs the login program, mainly for testing purposes. Creates a login scenario.
    '''
    #Creates admin login and tests login.
    make_login('admin@admin.com','Admin123!')
    session = login()
    if session is True:
        print ('Login successful.')
    else:
        print ('Login failed.')

def login(email = None, password = None, csv_file = login_csv):
    '''
    Function to login. Uses logins.csv file to check login details.
    Automatically runs input request if no parameters given.

    Parameters: 
    email (str): Email to request login
    password (str): Password to request login of the email
    csv_file (str): CSV file location

    Returns:
    True: Login successful.
    False: Login failed.
    '''
    #If no parameters inputted.
    if email is None and password is None:
        while True:
            #Requests email and password input until correct.
            email = input('Enter email >').strip().lower()
            if check_email_exists(email) is True:
                password = input('Enter password >')
                if check_password_correct(email, password) is True:
                    return True
                else:
                    print ('Incorrect password')
            else:
                print ('Email not registered')
    
    #If parameter input of email is missing, raise NameError.
    if email is None or email == '':
        raise NameError('Expected email in first parameter if using function parameters.')
    
    #If parameter input of password is missing, raise NameError.
    if password is None or password =='':
        raise NameError('Expected password in second parameter if using function parameters.')
    
    #If the email exists, will check password is correct in the CSV file.
    if check_email_exists(email, csv_file):
        if check_password_correct(email, password, csv_file):
            return True
    #Returns false if the password is incorrect.
    return False

def check_email_syntax(email):
    '''
    Function to check email syntax is correct - {name}@{domain}.

    Parameters:
    email (str): Email to check the syntax for.

    Returns:
    email (str): Email matches syntax.
    None: Email does not match syntax.
    '''
    #Define email regex expression and return appropriate value.
    email_syntax_key = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_syntax_key, email.strip().lower())

def check_password_syntax(password):
    '''
    Function to check password syntax is correct. 
    - At least 8 characters.
    - At least 1 capital letter.
    - At least 1 special character.
    - At least 1 number.

    Parameters:
    password (str): Password to check the syntax for.

    Returns:
    password (str): Password matches syntax.
    None: Password does not match syntax.
    '''
    #Define password regex expression for required sytax and return appropriate value.
    password_syntax_key =  r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*\d).{8,}$'
    return re.match(password_syntax_key, password.strip())

def check_email_exists(email, csv_file = login_csv):
    '''
    Function to check if an email already exists in the CSV file.

    Parameters:
    email (str): Email to check existence in CSV file.
    csv_file (str): Location of the CSV file.

    Returns:
    True: Email exists in the CSV file.
    False: Email does not exist in the CSV file.
    '''
    try:
        #Opens CSV and searches row by row for the Email.
        with open(csv_file, 'r', newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip().lower() == email.strip().lower():
                    return True

    #If file does not exist.            
    except FileNotFoundError:
        return False
    return False
         
def check_password_exists(password, csv_file = login_csv):
    '''
    Function to check if a password already exists within the CSV file.

    Parameters:
    password (str): Password to check existence in CSV file.
    csv_file (str): CSV file location.

    Returns:
    True: Password exists in CSV file.
    False: Password does not exist in CSV file.
    '''
    try:
        #Open CSV file and search line by line for password.
        with open(csv_file, 'r', newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == password:
                    return True
    
    #If the file does not exist.
    except FileNotFoundError:
        return False
    
def check_email_valid(email, csv_file = login_csv):
    '''
    Function to check if an Email inputted is valid in all ways.
    Syntax check and existence in CSV file check.

    Parameters:
    email (str): Email to check validity of.
    csv_file (str): CSV file location.

    Returns:
    True: Email is valid.
    False: Email is not valid.
    '''
    #Check Email syntax.
    if not check_email_syntax(email):
        return None
    
    #Check Email existence.
    if check_email_exists(email, csv_file):
        return False
    
    return True

def check_password_valid(password):
    '''
    Function to check if a password inputted is valid in all ways.
    Added for futureproofing.

    Parameters:
    password (str): Password to check validity of.

    Returns:
    True: Password is valid.
    False: Password is not valid.
    '''
    #Runs password syntax check.
    if not check_password_syntax(password):
        return None
    return True

def check_password_correct(email, password, csv_file = login_csv):
    '''
    Function to check if a password associated with an Email is correct.

    Parameters:
    email (str): Email to find password in CSV file.
    password (str): Password to verify matches the Email in the CSV file.
    csv_file (str): Location of the CSV file.

    Returns:
    True: Password is a match.
    False: Password is not a match.
    '''
    try:
        #Run through CSV file to find Email. Compare password.
        with open(csv_file, 'r', newline = '') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip().lower() == email.strip().lower():
                    if row[1].strip() == password.strip():
                        return True
                    
    #If the file does not exist.
    except FileNotFoundError:
        return False
    return False

def write_to_csv(email, password, csv_file = login_csv):
    '''
    Function to append Email and Password to CSV file.

    Parameters:
    email (str): Email to append to CSV.
    password (str): Password to append to CSV.
    csv_file (str): CSV file location.

    Returns:
    True: Confirms file appended.
    '''
    #Opens CSV file and appends Email and password.
    with open(csv_file, 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow([email.strip().lower(), password.strip()])
        return True

def make_email(email = None):
    '''
    Function to allow creation of an Email using syntax checking.

    Parameters:
    email (str): Email to create.

    Returns:
    email (str): If Email is valid.
    NameError: Parameter input is not valid.
    '''
    #No parameter input.
    if email is None:
        #Request Email until syntax is valid.
        while True:
            email = input('Enter email >').strip().lower()
            verify_email = check_email_valid(email)
            if verify_email is None:
                print('Email syntax not valid.') 
                continue
            elif not verify_email:
                print ('Email already exists.')
                continue
            return email.strip().lower()

    #Parameter validity check.            
    if check_email_valid(email) is None:
        raise NameError('Email syntax not valid.')
    return email.strip().lower()
        
def make_password(password = None):
    '''
    Function to create password using syntax checking.

    Parameters:
    password (str): Password to create.

    Returns:
    password (str): Password once verified.
    NameError: Password parameter is invalid.
    '''
    if password == None:
        while True:
            password = input('Enter password >').strip()
            verify_password = check_password_valid(password)
            if verify_password == None:
                print ('Password syntax invalid. Ensure it contains at least:')
                print ('-At least 1 capital letter\n-At least 1 Number\n-At least 1 symbol\nMore than 8 characters.')
                continue
            return password.strip()
                
    if check_password_valid(password) is None:
        raise NameError('Password syntax invalid.')
    return password.strip()  

def make_login(email = None, password = None, csv_file = login_csv):
    '''
    Function to create a whole login in one iteration and write to a CSV file.

    Parameters:
    email (str): Email to create login for.
    password (str): Password to assign to login.
    csv_file (str): CSV file location.

    Returns:
    True: Login successfully created.
    ValueError: Email or password is invalid.
    '''
    #If email parameter empty, make email.
    if email is None:
       email = make_email()
    #If email parameter has data, check Email validity.
    else:
        email = email.strip().lower()
        email_check = check_email_valid(email, csv_file)

    #If password parameter empty, create password.
    if password is None:
        password = make_password()
    #If password parameter has data, check password validity.
    else:
        password = password.strip()
        password_check = check_password_valid(password)

    try:
        #If Email is incorrect or already exists, raise ValueError.
        if email_check is None:
            raise SyntaxError('Invalid email syntax.')
        elif not email_check:
            raise ValueError('Email already exists.')

        #If password has incorrect syntax, raise ValueError.
        if password_check is None:
            raise SyntaxError('Invalid password syntax.')
        
    except NameError:
        #If all syntax and validity correct, write file to CSV and report to the user.
        write_to_csv(email, password, csv_file)
        print(f'Added {email} to database.')
        return True
    
if __name__ == '__main__':
    main()