#all thermodynamics functions
from CEA96.CEA.Database import Species
import numpy as np
import thermo
R = 8.314 #j/molk

def HeatCapacityT(species: Species, temp:float):
    """
    Calculates the heat capacity of the species at temp
    :param species: Spieces object
    :param temp: temperature
    :return: Heat capacity
    """
    Cp = 0
    for a, t in zip(Species.getCp_Coe(temp), species.getTexp(temp)):
        Cp = Cp + a*temp**t
    return Cp

def EnthalpyT(species: Species, temp:float):
    """
    Calculates H @ STD pressure and varying temperature
    :param species:
    :param temp:
    :return: H
    """
    a = species.getCp_Coe(temp)
    b = species.getBconst(temp)[0]
    return -a[0]*temp**(-2) + (a[1]*temp**(-1)) * np.log(temp) + a[2] + a[3]*temp/2 + (a[5]*temp**(2))/3 + (a[5]*temp**3)/4 + (a[6]*temp**4)/5 + b/temp

def EntropyT(species: Species, temp:float):
    """
    Calculates Entropy at specified temperature and STD pressure
    :param species:
    :param temp:
    :return:
    """
    a = species.getCp_Coe(temp)
    b = species.getBconst(temp)[1]
    return (-a[0]*temp**-2)/2 - (a[1]*temp**-1) + a[2]*np.log(temp) + a[3]*temp + (a[4]*temp**2)/2 + (a[5]*temp**3)/3 + (a[6]*temp**4)/4 + b

def EntropyTP(species: Species, temp: float, pressure:float, partialPressure: float):
    """
    Calculates Entropy at specified Temperature and Pressure
    :param species:
    :param temp:
    :param pressure:
    :param partialPressure:
    :return: S
    """
    return EntropyT(species, temp) - R * np.log(partialPressure/pressure)

def GibbsFreeEnergyTP(species:Species, temp:float, pressure:float, partialpressure:float):
    return EnthalpyT(species, temp) - EntropyTP(species, temp, pressure, partialpressure) * temp

def GibbsFreeEnergyT(species:Species, temp:float):
    return EnthalpyT(species, temp) - EntropyT(species, temp) * temp

def MxMolarMass(mixture:list):
    sum = 0
    assert isinstance(mixture[0], Species)
    for specie in mixture:
        sum = sum + specie.getMW() #kg/mol
    return sum

def MxMMoptimizer(mixture:list, MxMM = 0):
    """
    Dynamic Programming to minimize usage of computational resources
    :param mixture:
    :param MxMM:
    :return: Total mixture molar mass
    """
    if MxMM != 0:
        return MxMM
    elif MxMM == 0:
        return MxMolarMass(mixture)

def MxMMfraction(species:Species, mixture, MxMM=0):
    """
    calculates mass fraction of species in mixture
    :param species:
    :param mixture:
    :param MxMM:
    :return:
    """
    return species.getMW()/MxMMoptimizer(mixture, MxMM)

def PartialPressureSpecies(pressure:float, species:Species, MxMM = 0, mixture=[]):
    """
    Calculates partial pressure for species in mixture at given total pressure
    :param pressure: total pressure
    :param mixture: mixture species
    :param species: individual species
    :param MxMM: dynamic programming: already computed mixture molar mass
    :return:
    """
    MxMM = MxMMoptimizer(mixture, MxMM=MxMM)
    return pressure*MxMMfraction(species=species, mixture=mixture, MxMM=MxMM)

def getElementalProperties(mixture:list):
    """
    creates thermo.Chemical objects for all elements in mixture
    :param mixture:
    :return: {
    "element":(number, thermo.Chemical),
    ...
    }
    """
    elements = {}
    for species in mixture:
        e = species.getElements()
        for se in e.keys():
            if se in elements.keys():
                elements[se][0] = elements[se][0] + e[se]
            else:
                elements[se] = (e[se], thermo.Chemical(se))
    return elements



def getElementCount(mixture:list):
    elements = {}
    for species in mixture:
        e = species.getElements()
        for se in e.keys():
            if se in elements.keys():
                elements[se] = elements[se] + e[se]
            else:
                elements[se] = e[se]
    return elements


def getElementCountReactants(mixture:list, oxy:tuple, fuel:tuple):
    elements = {}
    for species in mixture:
        e = species.getElements()
        for se in e.keys():
            if se in elements.keys():
                if species.getInfo()[0] == oxy[0]:
                    elements[se] = elements[se] + oxy[1]*e[se]
                elif species.getInfo()[0] == fuel[0]:
                    elements[se] = elements[se] + fuel[1]*e[se]
            else:
                if species.getInfo()[0] == oxy[0]:
                    elements[se] = oxy[1]*e[se]
                elif species.getInfo()[0] == fuel[0]:
                    elements[se] = fuel[1]*e[se]
    return elements


def ChemicalPotential(species: Species, temp):
    """
    calculates mu, chemical potential
    :param species:
    :param temp:
    :return:
    """
    pass

