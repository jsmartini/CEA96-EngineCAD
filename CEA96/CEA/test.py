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


temps = []
gibbs = []
mix = ["CH4", "O2","O2"]
P = 6*10**6
for i in range(1, 9500, 10):
    try:
        gibbsE = GibbsFreeEnergyMixture(i, P, getObjects(mix)) / 1000
    except TypeError as e:
        continue
    print("TEMP {0}:\t\t:Gibbs:{1}\t".format(i,gibbsE))
    temps.append(i)
    gibbs.append(gibbsE)
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
fig = plt.figure()
ax = plt.axes()
ax.plot(temps, gibbs)
plt.title("Free Gibbs Energy and Temperature for {0} and {1} mixture. Fixed Pressure at {2}, MPa".format(mix[0], mix[1], P/10**6))
plt.xlabel("Temperature (K)")
plt.ylabel("Free Gibbs Energy (kJ/mol)")
plt.show()
