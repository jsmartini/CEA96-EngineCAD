from CEA96.CEA.Species import Species
from CEA96.CEA.Databases import ThermoDB
import thermo
import re
import numpy as np
import scipy.optimize as opt

def strip_keys_nameonly(key: str) -> str:
    #usage: strip gross symbols from keys
    return re.split(r'[-/(]', key)[0]

class EQLBRM:
    """
    Purpose:
        Calculate the equilibrium compositions of the fuel/air mixture

    __init__
    species: list of all valid keys in thermo.json for a species

    """

    def __init__(self, species: list):
        self.DB = ThermoDB()
        self.SpeciesObjects = [self.DB.getSpeciesObject(i) for i in species]
        self.SpeciesNames = [strip_keys_nameonly(i) for i in species]

    def compositions(self):



        return


