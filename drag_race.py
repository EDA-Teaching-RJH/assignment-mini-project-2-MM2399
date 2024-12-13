import login_manager

class Calculator:
    '''
    Class to handle calculations of any kind relating to a car's dynamics.
    Used by the Car class.

    Parameters:
    Please view Car class and they are linked.
    '''
    def calculate_horsepower(self, displacement, turbo, is_petrol, tuning_level, redline):
        '''
        Class method to calculate approximate engine horsepower.

        Parameters:
        displacment (float): Displacement volume of the total engine in litres.
        turbo (Bool): If car is turbocharged.
        is_petrol (Bool): If car runs on petrol (True) or diesel (False)
        tuning_level (float): Relative factor of how tuned the engine is for its size.
        redline (float): RPM at which the car must shift gear, limiting power output.

        Outputs:
        power (float): Horsepower estimate based on parameters (engine specs).
        '''
        #Performs a multiplier calculation based off engine specs.
        multiplier = 1
        multiplier *= float(displacement)
        multiplier *= float(redline)
        if turbo is True:
            multiplier *= 1.5
        if is_petrol is True:
            multiplier *= 1.1
        multiplier *= float(tuning_level)
        power = (multiplier / 100)
        return power

    def calculate_front_area(self, type):
        '''
        Class method to approximate the front surface area of a vehicle based on it's type.

        Parameters:
        type (str): Type of vehicle.

        Returns:
        area (float): Front surface area approximation of the vehicle.
        '''
        #Match vehicle type and return surface area.
        match type:
            case 'economy':
                area = 2.2
            case 'van':
                area = 4
            case 'sport':
                area = 2
            case 'super':
                area = 1.8
            case 'hyper':
                area = 1.6
            case _:
                area = 'N/A'

        return area    
    
    def calculate_drag_coefficient(self, type):
        '''
        Class method to approximate the drag coefficient of a vehicle based on it's type.

        Parameters:
        type (str): Type of vehicle.

        Returns:
        drag_coefficient (float): Drag coefficient approximation of the vehicle.
        '''
        #Match type to drag coefficient.
        match type:
            case 'economy':
                drag_coefficient = 0.35
            case 'van':
                drag_coefficient = 0.45
            case 'sport':
                drag_coefficient = 0.3
            case 'super':
                drag_coefficient = 0.28
            case 'hyper':
                drag_coefficient = 0.25
            case _:
                drag_coefficient = 'N/A'

        return drag_coefficient  
    
    def calculate_current_drag(self, area, drag_coefficient, velocity, air_density = 1.1225):
        '''
        Class method to calculate the current drag force of a vehicle based on velocity, drag coefficient and air density.

        Parameters:
        area (float): Surface area at the front of the vehicle.
        drag_coefficient (float): Drag coefficient of the vehicle.
        velocity (float): Current velocity of the vehicle.
        air_density (float): Density of the air the vehicle is passing through.

        Returns:
        drag_force (float): Drag force approximation in Newtons.
        '''
        #Calculate drag force using the appropriate equation.
        drag_force = (0.5 * air_density * area * drag_coefficient * (velocity**2))
        return drag_force
    
    def calculate_initial_acceleration(self, power, weight, area, drag_coefficient, air_density = 1.1225, velocity = 2):
        '''
        Class method to calculate the approxmiate initial acceleration of a vehicle just moving from rest.

        Parameters:
        power (float): Power in Watts of the engine.
        weight (float): Weight of the vehicle in KG.
        area (float): Surface area at the front of the vehicle.
        drag_coefficient (float): Drag coefficient of the vehicle.
        air_density (float): Air density of which the vehicle is moving through.
        velocity (float): Velocity of vehicle just after moving off.

        Returns:
        acceleration (float): Approximate acceleration of the vehicle from rest.
        '''
        #Calculate the net force using the appropriate equation.
        net_force = ((power) / velocity) - (self.calculate_current_drag(area, drag_coefficient, velocity, air_density))

        #Calculate acceleration based on the net force and the weight of the vehicle.
        acceleration = (net_force / (weight*2))
        return acceleration
    
    def calculate_current_acceleration(self, power, weight, area, drag_coefficient, velocity, air_density = 1.1225):
        '''
        Class method to calculate the current acceleration of a vehicle.

        Parameters:
        power (float): Power in Watts of the engine.
        weight (float): Weight of the vehicle in KG.
        area (float): Surface area at the front of the vehicle.
        drag_coefficient (float): Drag coefficient of the vehicle.
        air_density (float): Air density of which the vehicle is moving through.
        velocity (float):  Current velocity of the vehicle.

        Returns:
        acceleration (float): Approximate acceleration of the vehicle at current velocity.
        '''
         #Calculate the net force using the appropriate equation.
        net_force = ((power) / velocity) - (self.calculate_current_drag(area, drag_coefficient, velocity, air_density))

        #Calculate acceleration based on the net force and the weight of the vehicle.
        acceleration = (net_force / (weight*2))
        return acceleration
    
    def calculate_top_speed(self, power, type, air_density = 1.1225):
        '''
        Class method to calculate the theoretical top speed of a vehicle.

        Parameters:
        power (float): Power in Watts of the engine.
        type (str): Type of vehicle.
        air_density (float): Air density that the vehicle is moving through.

        Returns:
        top_speed (float): Approximate top speed of the vehicle.
        '''
        #Calculate top speed using appropriate equation.
        top_speed = (((power*2) / (air_density * self.calculate_front_area(type) * self.calculate_drag_coefficient(type)))**(1/3))
        return top_speed

class Car(Calculator):
    '''
    Class to handle car movement and dynamics based on specifications.

    Attributes:
    weight (float): Weight of the vehicle in KG.
    type (str): Type of the vehicle, category.
    registration (str): Registration of the vehicle.
    displacement (float): Engine displacement volume of the vehicle in litres.
    turbo (Bool): If the vehicle is turbocharged.
    is_petrol (Bool): If the vehicle uses petrol (True) or diesel (False)
    tuning_level (float): Relative factor of how tuned the engine is for its size.
    redline (float): RPM at which the car must shift.
    '''
    def __init__(self, weight, type, registration, displacement, turbo, is_petrol, tuning_level, redline):
        self.displacement = displacement
        self.turbo = turbo
        self.is_petrol = is_petrol
        self.tuning_level = tuning_level
        self.redline = redline
        self.weight = weight
        self.type = type
        self.registration = registration
    
    def return_registration(self):
        #Returns registraton.
        return self.registration
    
    def return_turbo_status(self):
        #Returns turbo status.
        return (self.turbo)
    
    def return_area(self):
        #Returns front surface area of vehicle
        return (self.calculate_front_area(self.type))
    
    def return_drag_coefficient(self):
        #Return drag coefficient of vehicle
        return (self.calculate_drag_coefficient(self.type))
    
    def return_current_drag(self, velocity = 0):
        #Return current drag of vehicle at specified velocity
        return (self.calculate_current_drag(self.return_area(), self.return_drag_coefficient(), velocity))
    
    def return_horsepower(self):
        #Return horsepower of the vehicle.
        return (self.calculate_horsepower(self.displacement, self.turbo, self.is_petrol, self.tuning_level, self.redline))
    
    def return_power_watts(self):
        #Return power of vehicle in watts.
        return (self.return_horsepower() * 746)

    def return_initial_acceleration(self):
        #Return the inital acceleration of the vehicle.
        return (self.calculate_initial_acceleration(self.return_power_watts(), self.weight, self.return_area(), self.return_drag_coefficient(), velocity = 1))
    
    def return_current_acceleration(self, velocity):
        #Return the current acceleration of the vehicle based on current velocity.
        return (self.calculate_current_acceleration(self.return_power_watts(), self.weight, self.return_area(), self.return_drag_coefficient(), velocity))
    
    def return_top_speed(self):
        #Return theoretical top speed of vehicle.
        return (self.calculate_top_speed(self.return_power_watts(), self.type))

    def calculate_drag_time(self, length, time_step = 0.01):
        '''
        Class method to calculate the time the car will take to travel the drag strip.

        Parameters:
        length (float): Length of the drag strip in metres.
        time_step (float): Steps to perform the integration calculation.  

        Returns:
        time (float): Time taken for vehicle to travel the drag strip.
        velocity (float): Velocity the vehicle reaches by the end of the drag strip.
        '''
        #Define starting velocity, position and time.
        velocity = 0
        position = 0
        time = 0

        #Integrate to calculate the time and velocity until end of the drag strip.
        while position < length:
            if velocity == 0:
                acceleration = self.return_current_acceleration(velocity+0.01)
            else:
                acceleration = self.return_current_acceleration(velocity+0.01)
            velocity += acceleration * time_step
            position += velocity * time_step
            time += time_step

        return time, velocity

def main():
    '''
    Run the drag strip simulation. Requires login.
    '''
    if login('admin@admin.com','Admin123!') is True:
        print ('\nWelcome to the drag strip!')
    
    vehicles = add_vehicles_manually()
    #vehicles = [[1200, 'economy','GL60UYA',1.4, True, False, 1, 5000],[2000, 'sport','OK04BYE',3.0, False, True, 1, 7000]]
    while True:
        drag_length = input('Enter length of the drag strip (m) >')
        try:
            float(drag_length)
        except ValueError:
            print ('Invalid drag length')
            continue
        
        print_all_stats(vehicles, float(drag_length))
        print ('=========================================================')
        print (f'Winner is: {determine_winner(vehicles, float(drag_length))}')
        print ('=========================================================')
        break
          
def login(username = None, password = None):
    '''
    Function to handle the account login using the login_manager library.

    Parameters:
    username (str): Username to login with.
    password (str): Password to login with.

    Returns:
    True: Login complete.
    '''
    #If parameters inputted, attempt login. If failed, request details.
    if username is not None and password is not None:
        if login_manager.login(username, password) is True:
            print ('Login successful.')
            return True
        print ('Quick login failed, please enter manually.')

    while True:
        #Login process, user can create account or manually enter login.
        login_status = input('Login or create account? (Enter login or create) >').strip().lower()
        if login_status == 'login':
            if login_manager.login() is True:
                print ('Login successful.')
                return True
            else:
                print ('Login Failed.')

        elif login_status == 'create':
            login_manager.make_login()
        else:
            print ('Please enter valid option.')

def assign_type(type):
    '''
    Function to assign the type of vehicle.

    Parameters:
    type (str): Type of vehicle.

    Returns:
    type (str): Valid type of vehicle.
    '''
    #Accepted types of vehicle for comparison
    accepted_types = ['economy','van','sport','super','hyper']

    #If no parameter or the parameter is not valid, request type until valid.
    if type is None or type not in accepted_types:
        while True:
            type = input('Enter type of vehicle (economy, van, sport, super, hyper) >').strip().lower()
            if type in accepted_types:
                return type 
            print ('Invalid type.')

def assign_registration(registration):
    #Assigns registration to the vehicle.
    if registration is None:
        registration = input('Enter vehicle registration >').strip().upper()
        return registration
      
def assign_displacement(displacement):
    '''
    Function to assign displacement to vehicle.

    Parameters:
    displacement (float): Displacement of vehicle in litres.

    Returns:
    displacement (float): Valid displacement of vehicle in litres.
    '''
    while True:
        #If no parameter input, request displacement until valid.
        if displacement is None:
            displacement = input('Enter engine displacement in litres >').strip()
        try:
            float(displacement)
            return float(displacement)
        except ValueError:
            print ('Enter valid displacement.')
            displacement = None

def assign_turbo(turbo):
    '''
    Function to assign turbo to vehicle.
    
    Parameters:
    turbo (Bool): If the vehicle is turbocharged.

    Returns:
    turbo (Bool): Valid turbocharger status.
    '''
    #If parameter empty or invalid input, request turbo status until valid.
    if turbo is None or (turbo is not True and turbo is not False):
        while True:
            turbo = input('Has the vehicle got a turbo? (y or n) >').strip().lower()
            if turbo == 'y':
                turbo = True
            elif turbo == 'n':
                turbo = False
            else:
                print ('Enter valid input.')
                continue
            return turbo

def assign_fuel(is_petrol):
    '''
    Function to assign fuel type to vehicle.

    Parameters:
    is_petrol (Bool): If petrol (True) or diesel (False).

    Returns:
    is_petrol (Bool): Validated fuel type.
    '''
    #If parameter empty or not bool, request fuel type until valid.
    if is_petrol is None or (is_petrol is not True and is_petrol is not False):
        while True:
            is_petrol = input('Does the car use petrol or diesel? >').strip().lower()
            if is_petrol == 'petrol':
                is_petrol = True
            elif is_petrol == 'diesel':
                is_petrol = False
            else:
                print ('Enter valid fuel type.')
                continue
            return is_petrol

def assign_redline(redline):
    '''
    Function to assign redline to vehicle.

    Parameters:
    redline (float): Redline in RPM of the vehicle, the RPM is must shift at.

    Returns:
    redline (float): Valid redline value.
    '''
    while True:
        #If no parameter inputted, request redline until valid input.
        if redline is None:
            redline = input('Enter the vehicle redline >').strip().lower()
        try:
            float(redline)
            return float(redline)
        except ValueError:
            print('Enter a valid displacement.')
            redline = None

def assign_tuning_level(tuning_level):
    '''
    Function to assign the tuning level to the vehicle.

    Parameters:
    tuning_level (float): Relative factor of how tuned the engine is for its size.

    Returns:
    tuning_level (float): Valid tuning level of engine.
    '''
    while True:
        #If no parameter or parameter invalid, request tuning level until valid.
        if tuning_level is None:
            print ('\nTuning level is a ratio of the engine output vs expected output.')
            print ('Approx. 1 for regular cars, 0.5 for underpowered engines, above 1 for tuned vehicles, depending on the tune.\n')
            tuning_level = input('Enter tuning level >')
        try:
            float(tuning_level)
            return float(tuning_level)
        except ValueError:
            print ('Enter valid tuning level.')
            tuning_level = None

def assign_weight(weight):
    '''
    Function to assign weight to the vehicle.

    Parameters:
    weight (float): Weight of the vehicle in KG.

    Returns:
    weight (float): Valid weight of the vehicle.
    '''
    while True:
        #If parameter is empty or vehicle weight invalid, request weight until valid.
        if weight is None:
            weight = input('Enter vehicle weight in KG >').strip().lower()
        try:
            float(weight)
            return float(weight)
        except ValueError:
            print('Enter valid weight.')
            weight = None

def assign_vehicle_details(type = None , registration = None, displacement = None, turbo = None, is_petrol = None, redline = None, tuning_level = None, weight = None):
    '''
    Function to assign each detail to the vehicle.

    Parameters:
    weight (float): Weight of the vehicle in KG.
    type (str): Type of the vehicle, category.
    registration (str): Registration of the vehicle.
    displacement (float): Engine displacement volume of the vehicle in litres.
    turbo (Bool): If the vehicle is turbocharged.
    is_petrol (Bool): If the vehicle uses petrol (True) or diesel (False)
    tuning_level (float): Relative factor of how tuned the engine is for its size.
    redline (float): RPM at which the car must shift.

    Returns:
    weight (float): Valid weight of the vehicle in KG.
    type (str): Valid type of the vehicle, category.
    registration (str): Valid registration of the vehicle.
    displacement (float): Valid engine displacement volume of the vehicle in litres.
    turbo (Bool): Valid status of turbocharger.
    is_petrol (Bool): Valid fuel type.
    tuning_level (float): Valid relative factor of how tuned the engine is for its size.
    redline (float): Valid RPM at which the car must shift.
    '''
    type = assign_type(type) #Assign type
    registration = assign_registration(registration) #Assign registration
    displacement = assign_displacement(displacement) #Assign displacement
    turbo = assign_turbo(turbo) #Assign turbo status
    is_petrol = assign_fuel(is_petrol) #Assign fuel type
    redline = assign_redline(redline) #Assign redline
    tuning_level = assign_tuning_level(tuning_level) #Assign tuning level
    weight = assign_weight(weight) #assign weight
    return weight, type, registration, displacement, turbo, is_petrol, tuning_level, redline

def add_vehicles_manually():
    '''
    Function to add vehicles manually by prompting input for each statistic.

    Parameters:
    None

    Returns:
    vehicles (array): List of stored vehicles added.
    '''
    #Define vehicles list 
    vehicles = []
    while True:
        #Add vehicle details to the list.
        vehicles.append(assign_vehicle_details())
        #Prompt addition of more vehicles until finished.
        while True:
            add_more = input('Enter another vehicle? (y or n)>').strip().lower()
            if add_more == 'y':
                break
            elif add_more == 'n':
                return vehicles
            else:
                print ('Enter valid option.')
            
            
def print_stats(vehicle, drag_length):
    '''
    Function to print all of statistics of the vehicles and drag race.

    Parameters:
    vehicle (str): Vehicle to print details for.
    drag_length (float): Length of the drag strip in metres.

    Returns:
    None: Only prints statistics.
    '''
    #Assign vehicle as object to the car class.
    vehicle = Car(vehicle[0], vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7])
    #Print all the statistics.
    print ('---------------------------------------------------------')
    print (f'Registration: {vehicle.return_registration()}\n')
    print (f'Power (HP): {vehicle.return_horsepower():.3f}')
    print (f'Power (W): {vehicle.return_power_watts():.3f}')
    print (f'Turbocharged: {vehicle.return_turbo_status()}')
    print (f'Front area approx. (m^2): {vehicle.return_area()}')
    print (f'Drag coefficient approx: {vehicle.return_drag_coefficient()}\n')
    print (f'Drag force at 5m/s (N): {vehicle.return_current_drag(5):.3f}')
    print (f'Drag force at 10m/s (N): {vehicle.return_current_drag(10):.3f}')
    print (f'Drag force at 25m/s (N): {vehicle.return_current_drag(25):.3f}\n')
    print (f'Initial acceleration (m/s^2): {vehicle.return_initial_acceleration():.3f}')
    print (f'Acceleration at 5ms (m/s^2): {vehicle.return_current_acceleration(5):.3f}')
    print (f'Acceleration at 10ms (m/s^2): {vehicle.return_current_acceleration(10):.3f}')
    print (f'Acceleration at 25ms (m/s^2): {vehicle.return_current_acceleration(25):.3f}\n')
    print (f'Top speed (m/s)(Overall): {vehicle.return_top_speed():.3f}')
    print (f'Top speed (mph)(Overall): {vehicle.return_top_speed()*2.23694:.3f}\n')
    print (f'Time to complete a {drag_length}m drag: {vehicle.calculate_drag_time(drag_length)[0]:.3f}s')   
    print (f'Top speed at end of drag (m/s): {vehicle.calculate_drag_time(drag_length)[1]:.3f}')
    print (f'Top speed at end of drag (mph): {vehicle.calculate_drag_time(drag_length)[1]*2.23694:.3f}\n')  
    print ('---------------------------------------------------------')

def print_all_stats(vehicles, drag_length):
    '''
    Function to print stats of every single vehicle.

    Parameters:
    vehicles (array): List of vehicles to print data of.
    drag_length (float): Length of the drag strip in metres.

    Returns:
    None: Only prints statistics.
    '''
    #Iterate through each vehicle and print stats.
    for vehicle in vehicles:
        print_stats(vehicle, drag_length)

def determine_winner(vehicles, drag_length):
    '''
    Function to detrmine the winner out of all the cars added to the drag race.
    
    Parameters:
    vehicles (array): List of vehicles to print data of.
    drag_length (float): Length of the drag strip in metres.
    
    Returns:
    winner (str): Registration of the winning vehicle.
    '''
    #Create list to hold all drag times and vehicles.
    times = []
    vehicle_list = []
    #Iterate through each vehicle and append the vehicle and its drag time to the appropriate lists.
    for vehicle in vehicles:
        vehicle = Car(vehicle[0], vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7])
        times.append(vehicle.calculate_drag_time(drag_length)[0])
        vehicle_list.append(vehicle)

    #Find the minimum time and associate it with the winning vehicle.
    win_time = min(times)
    for number, time in enumerate(times):
        if time == win_time:
            winner = vehicle_list[number]
            return winner.return_registration()           
    
if __name__ == '__main__':
    main()
