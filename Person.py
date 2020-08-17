class Person:
    def __init__(self, firstName, lastName, address, age, phoneNumber):
        self.__firstName   = firstName
        self.__lastName    = lastName
        self.__address     = address
        self.__email       = firstName + "." + lastName + "@gmail.com"
        self.__age         = age
        self.__phoneNumber = phoneNumber
        self.__fullName    = firstName + " " + lastName

    # GETTER METHODS
    def getFirstName(self):
        return self.__firstName

    def getLastName(self):
        return self.__lastName

    def getAddress(self):
        return self.__address

    def getEmail(self):
        return self.__email

    def getAge(self):
        return self.__age

    def getPhoneNumber(self):
        return self.__phoneNumber

    def getFullName(self):
        return self.__fullName


    # SETTER METHODS
    def setFirstName(self, name):
        self.__firstName = name

    def setLastName(self, name):
        self.__lastName = name

    def setAddress(self, address):
        self.__address = address

    def setEmail(self, email):
        self.__email = email

    def setAge(self, age):
        self.__age = age

    def setPhoneNumber(self, number):
        self.__phoneNumber = number










