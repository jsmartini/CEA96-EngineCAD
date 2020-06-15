from CEA.Species import Species
import os, json

class ThermoDB:
    """
        Thermodynamic database used to Retrieve Thermochemical data for
        CEA modules.
    """
    thermo = './datasets/thermo.inp'
    thermoJson = 'thermo.json'

    def __init__(self):
        os.chdir("datasets")
        self.ThermoDB = json.load(open(self.thermoJson, 'r'))
        self.ThermoKeys = self.ThermoDB['records'].keys()

    def query(self, pattern: str):
        matching = []
        for species in self.ThermoKeys:
            if pattern.upper() in species.upper():
                matching.append(species)
        return matching

    def getSpeciesObject(self, species: str):
        return Species(self.ThermoDB["records"][species].copy())

    def __del__(self):
        pass

class TransDB:

    def __init__(self):
        pass
        #TO-DO with trans.inp


if __name__ == "__main__":
    print(ThermoDB().query("C4H4"))
    os.chdir("../")
    print(ThermoDB().getSpeciesObject("C4H4,1,3-cyclo-"))