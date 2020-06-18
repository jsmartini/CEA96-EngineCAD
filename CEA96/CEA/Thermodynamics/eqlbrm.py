from CEA96.CEA.Thermodynamics.thermodynamics import *
from CEA96.CEA.Database import *
import scipy.optimize as opt
import numpy as np

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

def Stoich2Products(OFratio:float, oxidizer:str, fuel:str, products:list, db = ThermoDB()):
    assert isinstance(products[0], Species)
    assert len(products) == 2
    oxidizer = db.getSpecies(oxidizer)
    fuel = db.getSpecies(fuel)
    global oxy_coe
    global fuel_coe
    oxy_coe = decToInt(OFratio)[0]
    fuel_coe = decToInt(OFratio)[1]
    reactants = [oxidizer, fuel]
    products = [Species(db.getSpecies(i)) for i in products]
    reactantsElements = getElementCountReactants(reactants, oxy=(oxidizer.getInfo()[0], oxy_coe), fuel=(fuel.getInfo()[0], fuel_coe))
    productElements = getElementCount(products)
    for element in reactantsElements.keys():
        MatchingFlag = False
        for e in productElements.keys():
            if element == e:
                MatchingFlag = True
        if not MatchingFlag:
            raise Exception("Invalid Combination of Reactants and Products, Base Elements non-matching")
    def checkbalance(elements1:dict, elements2:dict)->bool:
        for k1 in elements1.keys():
            for k2 in elements2.keys():
                if k1 == k2:
                    if elements1[k1] != elements2[k1]:
                        return False
                else:
                    continue
        return True
    def solve(roof):
        p1coe = 1
        p2coe = 1
        while p1coe <= roof:
            while p2coe <roof:
                #reusing this eq
                e = getElementCountReactants(products, oxy=(products[0].getInfo()[0], p1coe), fuel=(products[1].getInfo()[0], p2coe))
                if checkbalance(reactantsElements, e):
                    out =  {
                        "oxyCoe": oxy_coe,
                        "fuelCoe": fuel_coe,
                        "p1Coe": p1coe,
                        "p2Coe": p2coe
                    }
                    del oxy_coe
                    del fuel_coe
                    return out
                else:
                    p2coe += 1
            p1coe += 1
        return {}
    roof_multiplier = 1
    convergence_limit = 100
    while True:
        roof = np.max(roof_multiplier*oxy_coe, roof_multiplier*fuel_coe)
        out = solve(roof)
        if out == {}:
            roof_multiplier += 1
        else:
            return out
        if convergence_limit == roof_multiplier:
            raise Exception("Coefficients did not Converge: eqlbrm.py line 82")

class CombustionReaction:

    def __init__(self, oxyCoe, FuelCoe, products:list):
        assert len(products) == 2
        pass
