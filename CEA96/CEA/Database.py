import os
import json
import re

class Species:
    """
    phase = 0 (gas)
    nonzero for condensed phases
    """
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
        return self.Intervals[0]
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
    def getTexp(self, temp):
        return self.getInterval(temp)["T_exp"]
    def getCp_Coe(self, temp):
        return self.getInterval(temp)["Cp_coes"]
    def getBconst(self, temp):
        return self.getInterval(temp)["b_constants"]

class ThermoDB:

    Mixture = {
        "Products":[],
        "Reactants":[]
    }

    simpleFuels = ["CH4", "CH4(L)", "H2", "H2(L)", "RP-1"]
    simpleOxidizers = ["Air", "CL2", "CL2(L)", "F2", "F2(L)", "H2O2(L)", "N2H4(L)", "N2O", "NH4NO3(I)", "O2", "O2(L)"]

    def __init__(self):
        os.chdir("../datasets")
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
        if len(matching) == 0:
            raise BaseException("Could Not Find Species")
        return matching

    def getExact(self, pattern, type = None):
        """
        :param pattern: text pattern to search
        :param type: true -> products, false->reactants, None, both (default
        :return: list of matching names and database location
        """
        matching = []
        if type == None:
            for name in self.products:
                if pattern == name:
                    matching.append(("P", name))
            for name in self.reactants:
                if pattern == name:
                    matching.append(("R", name))
        elif type == True:
            for name in self.products:
                if pattern == name:
                    matching.append(("P", name))
        elif type == False:
            for name in self.reactants:
                if pattern == name:
                    matching.append(("R", name))
        if len(matching) == 0:
            raise BaseException("Could Not Find Species")
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
        location = self.getExact(name)

        if len(location) > 1:
            raise ValueError("Name not specific, too many species with name in Query")
            location = location[0]
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
    print(db.getSpecies("C4H4").getInterval(5000))