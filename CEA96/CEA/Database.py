import os
import json
import re

class Species:

    def __init__(self, data:dict):
        self.raw = data
        self.name = data["name"]
        self.info = data["info"]
        self.Intervals = data["Intervals"]
        self.source = data["Source"]
        self.Elements = data["Elements"]
        self.MoleWeight = data["MolecularWeight"]
        self.HeatOfFormation = data["HeatOfFormation"]
    def getInterval(self, temp):
        for interval in self.Intervals:
            if interval["temp_lower"] <= temp and interval["temp_upper"] >= temp:
                return interval
    def getMW(self):
        return self.MoleWeight
    def getHoF(self):
        return self.HeatOfFormation
    def getElements(self):
        return self.Elements
    def getInfo(self):
        return self.name, self.info, self.source
    def getRaw(self):
        return self.raw

class ThermoDB:

    Mixture = {
        "Products":[],
        "Reactants":[]
    }

    def __init__(self):
        os.chdir("datasets")
        self.db = json.load(open("thermo.json"))
        self.productsdata = self.db["PRODUCTS"]
        self.reactantsdata = self.db["REACTANTS"]
        self.products = self.productsdata.keys()
        self.reactants = self.reactantsdata.keys()

    def Query(self, pattern, type = None):
        """
        :param pattern: text pattern to search
        :param type: true -> products, false->reactants, None, both (default
        :return: list of matching names and database location
        """
        matching = []
        if type == None:
            for name in self.products:
                if pattern in name:
                    matching.append(("P", name))
            for name in self.reactants:
                if pattern in name:
                    matching.append(("R", name))
        elif type == True:
            for name in self.products:
                if pattern in name:
                    matching.append(("P", name))
        elif type == False:
            for name in self.reactants:
                if pattern in name:
                    matching.append(("R", name))
        return matching

    def addSpeciesToMixture(self, name):
        location = self.Query(name)
        if len(location) > 1:
            raise ValueError("Name not specific, too many species with name in Query")
        if location[0][0] == "P":
            self.Mixture["Products"][location[1]].append(Species(self.productsdata[location[0][1]]))
        elif location[0][0] == "R":
            self.Mixture["Reactants"][location[1]].append(Species(self.reactantsdata[location[0][1]]))

    def getSpecies(self, name):
        location = self.Query(name)
        if len(location) > 1:
            raise ValueError("Name not specific, too many species with name in Query")
        if location[0][0] == "P":
            return Species(self.productsdata[location[0][1]])
        elif location[0][0] == "R":
            return Species(self.reactantsdata[location[0][1]])

    def clearMixture(self):
        self.Mixture = {
            "Products":[],
            "Reactants":[]
        }


if __name__ == "__main__":
    db = ThermoDB()
    print(db.getSpecies("C2H4O(L),ethyle").getRaw())