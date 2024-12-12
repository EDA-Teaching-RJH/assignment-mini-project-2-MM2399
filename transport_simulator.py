class Car:
    def __init__(self, weight, type, registration, wins):
        self.weight = weight
        self.type = type
        self.registration = registration
        self.wins = wins
    
    def calculate_acceleration(self):
        drag = self.
         
        

class Engine(Car):
    def __init__(self, weight, type, registration, displacement, turbo, is_petrol, tuned, redline):
        self.displacement = displacement
        self.turbo = turbo
        self.is_petrol = is_petrol
        self.tuned = tuned
        self.redline = redline
        super().__init__(weight, type, registration)

    def calculate_power(self):
        multiplier = 1
        multiplier *= (1/(self.weight)**(1/3))
        multiplier *= self.displacement
        multiplier *= self.redline
        if self.turbo is True:
            multiplier *= 1.5
        if self.is_petrol is True:
            multiplier *= 1.1
        if self.tuned is True:
            multiplier *= 2
        self.power = (multiplier / 100)
        return self.power

    def calculate_drag(self):
        match self.type:
            case 'economy':
                self.drag = 1
            case 'van':
                self.drag = 2
            case 'sport':
                self.drag = 0.8
            case 'super':
                self.drag = 0.6
            case 'hyper':
                self.drag = 0.4
            case _:
                ()
        return self.drag


