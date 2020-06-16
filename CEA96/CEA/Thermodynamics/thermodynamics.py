#all thermodynamics functions
from CEA96.CEA.Database import Species
import numpy as np

R = 8.314 #j/molk

def HeatCapacityT(species: Species, temp:float):
    Cp = 0
    for a, t in zip(Species.getCp_Coe(temp), Species.getTexp(temp)):
        Cp = Cp + a*temp**t
    return Cp

def EnthalpyT(species: Species, temp:float):
    a = Species.getCp_Coe(temp)
    b = Species.getBconst(temp)[0]
    return -a[0]*temp**(-2) + (a[1]*temp**(-1)) * np.log(temp) + a[2] + a[3]*temp/2 + (a[5]*temp**(2))/3 + (a[5]*temp**3)/4 + (a[6]*temp**4)/5 + b/temp

def EntropyT(species: Species, temp:float):
    a = Species.getCp_Coe(temp)
    b = Species.getBconst(temp)[1]
    return (-a[0]*temp**-2)/2 - (a[1]*temp**-1) + a[2]*np.log(temp) + a[3]*temp + (a[4]*temp**2)/2 + (a[5]*temp**3)/3 + (a[6]*temp**4)/4 + b

def EntropyTP(species: Species, temp: float, pressure:float, partialPressure: float):
    return EntropyT(species, temp) - R * np.log(partialPressure/pressure)

def GibbsFreeEnergyTP(species:Species, temp:float, pressure:float, partialpressure:float):
    return EnthalpyT(species, temp) - EntropyTP(species, temp, pressure, partialpressure) * temp

def GibbsFreeEnergyT(species:Species, temp:float):
    return EnthalpyT(species, temp) - EnthalpyT(species, temp) * temp


