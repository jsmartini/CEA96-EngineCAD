
import thermo
import re
import numpy as np
import scipy.optimize as opt
from CEA96.CEA.Thermodynamics.thermodynamics import *
from CEA96.CEA.Database import ThermoDB
"""
Minimization of Gibbs Free Energy via Fixing Pressure (MPA) and Entropy = 0
Isentropic Expansion at constant pressure
1.) Minimize gibbs e over temperature range @ P and S, find Temperature and Eqlbrm compositions
2.) Determine Optimal O/F ratio @ Pressure
"""

def decToInt(decimal:float, threshold = 0.05):
    """
    for determining stoich coefficients
    :param decimal:
    :param threshold:
    :return: (multiplier, coefficient for the oxidizer in O/F rations
    """
    integer = 1
    while True:
        print(decimal * integer % 1)
        if (decimal * integer) % 1 <= threshold:
            return (integer, round(decimal*integer))
        else:
            integer += 1


def Stoich1(OFratio:float, oxidizer:str, fuel:str, products:list, db = ThermoDB()):
    assert isinstance(products[0], Species)
    oxidizer = db.getSpecies(oxidizer)
    fuel = db.getSpecies(fuel)
    oxy_coe = decToInt(OFratio)[0]
    fuel_coe = decToInt(OFratio)[1]
    reactants = [oxidizer, fuel]
    reactantsElements = getElementCountReactants(reactants, oxy=(oxidizer.getInfo()[0], oxy_coe), fuel=(fuel.getInfo()[0], fuel_coe))
    productElements = getElementCount(products)
    for element in reactantsElements.keys():
        MatchingFlag = False
        for e in productElements.keys():
            if element == e:
                MatchingFlag = True
        if not MatchingFlag:
            raise Exception("Invalid Combination of Reactants and Products, Base Elements non-matching")
    return


def minimizeFreeGibbs(reactants = [], products = [], ):
    pass


