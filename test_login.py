import pytest
import login_manager
import csv
import os

@pytest.fixture(scope='session') #I SPEND 2 HOURS TO REALISED I NEEDED TO USE THIS TO STOP IT RESETTING THE FILE IN EVERY TEST 
def temp_csv_file():
    '''
    Function to create the temporary CSV file to perform tests on the login manager.

    Yields:
    file_name (str): Name of the temporary file to test logins.
    '''
    file_name = "test_logins.csv"  #Name of the file to create in the current directory
    try:
        #Create and fill the file with some test data
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['test@test.com', 'Testing123!'])
            writer.writerow(['testtwo@new.com', 'NewTest321?'])

        print(f"Temp file created: {file_name}")
        yield file_name
    finally:
        #Clean up the file after the test
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Temp file deleted: {file_name}")


#Assign email, password and expected outcome to parameters for login test functions
@pytest.mark.parametrize(
        'email, password, expected',
        [
            ('test@test.com', 'Testing123!', True), #Valid login
            ('test@test.com', 'wrongpassword', False), #Valid email, invalid password <- Failing 
            ('', 'Testing123!', False), #Blank email
            ('test@test.com', '', False), #Blank password
        ]
)

#Calls the login from the parameterized values and asserts each to check validity.
def test_login(email, password, expected, temp_csv_file):
    try:
        result = login_manager.login(email, password, temp_csv_file)
        assert not isinstance(result, BaseException)
        assert result == expected

    except (NameError, ValueError, SyntaxError):
        pass
#Assign email, password and expected outcome to parameters for create login test functions
@pytest.mark.parametrize(
        'email, password, expected',
    [
        ('testy@test.com', 'NewPassword123!', True),  #Successful creation
        ('testy@test.com', 'SecondPassword123!', False), #Duplicate email
        ('', 'Password123!', False), #No username
        ('new@new.com', '', False),  #No password
        ('', '', False),  #No data
        ('hello@hello.com', 'NewPassword123!', True), # Final test
    ]
)

#Tests each parameterized value to create a login.
def test_create_login(email, password, expected, temp_csv_file):
    if expected:
        result = login_manager.make_login(email, password, temp_csv_file)
        assert result is True
        with open(temp_csv_file, mode='r', newline = '') as file:
            rows = list(csv.reader(file))
            assert any(row[0] == email and row[1] == password for row in rows)
            
    else:
        with pytest.raises((NameError, ValueError, SyntaxError)):
            login_manager.make_login(email, password, temp_csv_file)