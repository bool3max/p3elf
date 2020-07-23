class Person:

    valid_genders = ['m', 'f']
    
    def __init__(self, name, age, gender, country=None):
        self.name = name
        self.age = age
        self.country = country
        if gender.lower() not in Person.valid_genders:
            raise Exception('Invalid gender in constructor')
            return
        else:
            self.gender = gender

    def say_info(self):
        print(f"Hi, I am {self.name} and I am {self.age} years old.")
        if(self.country):
            print(f"I am also from {self.country}")

class ExonEmployee(Person):
    # add: employment length, clearnace level, department
    valid_clearances = list(range(1,10))
    valid_depts = ['comp lab', 'chem lab', 'kitchen']

    def __init__(self, name, age, gender, empl, clearance, dept, country=None):
        # handle our own stuff
        self.empl = empl
        if clearance not in ExonEmployee.valid_clearances:
            raise Exception('Invalid clearance level')
            return
        else:
            self.clearance = clearance
        self.dept = dept
        super().__init__(name, age, gender, country)

bob = ExonEmployee('Bob', 33, 'm', 92, 4, 'comp lab', 'China')
bob.say_info()
