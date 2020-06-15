
from math import log


class Species:
    # Takes a Species Dict from the DB and loads it into the class to pick apart
    #
    #
    kgMole = 0 #kilogram mole of species in mixture

    def findInterval(self, temp):
        #finds interval for temperature floor or ceiling

        interval_id= 0
        while interval_id < self.record["intervals_number"]:
            if temp <= self.record["intervals"][interval_id]["tu"] and temp >= self.record["intervals"][interval_id]["tl"]:
                return interval_id
            else:
                interval_id += 1
        raise Exception("Missing Thermochemical Data")

    def __del__(self):
        pass

    def __init__(self, species: dict):
        self.record = species

    def id(self):
        return self.record["id"]

    def phase(self):
        return self.record["phase"]

    def mw(self):
        #molar weight
        return self.record["mw"] / 1000 #kg/mol

    def hof(self):
        #heat of formation at 298.15k
        return self.record["hof"]

    def b_coe(self, temp):
        interval = self.findInterval(temp)
        return self.record["intervals"][interval]["b"]

    def Cp(self, temp):
        temp = float(temp)
        interval = self.findInterval(temp)
        t_exponents = self.record["intervals"][interval]["t"]
        Cp_Coefficients = self.record["intervals"][interval]["Cp"]
        CpR = 0
        #Eq 4.3 25/58 RP_1311
        for t, a in zip(t_exponents, Cp_Coefficients[:len(Cp_Coefficients)]):
            CpR+=a*(temp**t)
        return CpR

    def Cp_coe(self, temp):
        temp = float(temp)
        interval = self.findInterval(temp)
        return self.record["intervals"][interval]["Cp"]

    def t_exponents(self, temp):
        temp = float(temp)
        interval = self.findInterval(temp)
        return self.record["intervals"][interval]["Cp"]

    def H(self, temp):
        temp = float(temp)
        interval = self.findInterval(temp)
        Cp = self.record["intervals"][interval]["Cp"]
        #4.10 25/58 RP-1311
        return -Cp[0]*(temp**-2) + Cp[1]*(temp**-1)*log(temp) + Cp[2] + Cp[3]*temp/2+ Cp[4]*(temp**2)/3 +Cp[5]*(temp**3)/4 + Cp[6]*(temp**7)/5 + Cp[7]/temp

    def s(self, temp):
        temp = float(temp)
        interval = self.findInterval(temp)
        t = self.record["intervals"][interval]["t"]
        Cp = self.record["intervals"][interval]["Cp"]
        return -Cp[0]*(temp**-2)/2-Cp[1]*(temp**-1)+Cp[2]*log(temp)+Cp[3]*temp+Cp[4]*(temp**2)/2+Cp[5]*(temp**3)/3+Cp[6]*(temp**4)/4+Cp[-1]

    def h_coe(self, temp):
        temp = float(temp)
        interval = self.findInterval(temp)
        return self.record["intervals"][interval]["h"]

    def __str__(self):
        return self.record.__str__()