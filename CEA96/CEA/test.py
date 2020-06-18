from CEA96.CEA.Thermodynamics.thermodynamics import *
from CEA96.CEA.Database import *
import os

def GibbsFreeEnergyMixture(temp, pressure, mixture:list):
    assert isinstance(mixture[0], Species)
    MxMM = MxMolarMass(mixture)
    gibbsfree = 0
    for species in mixture:
        partialP = PartialPressureSpecies(pressure=pressure, species=species, MxMM=MxMM)
        gibbsfree += GibbsFreeEnergyTP(species=species,temp=temp, pressure=pressure, partialpressure=partialP)
    return gibbsfree

def getObjects(mix:list, db=ThermoDB()):
    return [db.getSpecies(i) for i in mix]

print(os.getcwd())

print(GibbsFreeEnergyMixture(5000, 6*10**6, getObjects(["C4H4", "Air"])))