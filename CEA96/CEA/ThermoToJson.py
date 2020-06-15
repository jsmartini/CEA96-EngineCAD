import re
import json
import os

def reader(file):
    thermodata = {"PRODUCTS": {}, "REACTANTS": {}}
    with open(file, 'r') as f:
        lines = len(open(file, 'r').readlines())
        buffer = ''
        # start: clear table of contents and datasheet info
        i = 42
        while i > 0:
            i = i - 1
            buffer = f.readline()
        # end: contents
        max_line = lines  # testing variable
        # data flags
        InfoFlag = True
        IntervalFlag = False
        Intervals = 0
        line = 1
        entry = {}
        interval = {"temp_lower": 0, "temp_upper": 0, "T_exp": [], "Cp_coes": [], "b_constants": [],
                    "(H(298.15)-H(0))": 0}
        PDFLAG = True  # products -> reactants

        while max_line > 0:
            max_line = max_line - 1

            buffer = f.readline()

            if re.search("END PRODUCTS", buffer) != None:
                print("FINISHED PRODUCTS")
                PDFLAG = False
                continue
            elif re.search("END REACTANTS", buffer) != None:
                print("FINISHED REACTANTS")
                return thermodata

            if InfoFlag:
                if line == 1:
                    line1regex = r'\s'
                    tokens = re.split(line1regex, buffer)
                    entry["name"] = tokens[0]
                    tokens.pop(0)
                    entry["info"] = []
                    for t in tokens:
                        if t != "":
                            entry["info"].append(t)
                    line = 2
                    continue

                elif line == 2:
                    Intervals = int(buffer[1:3].strip())
                    entry["Intervals"] = Intervals
                    entry["Source"] = buffer[3:10]
                    entry["Elements"] = {}
                    # 10-18; spacing is by 8
                    entry["Elements"][buffer[10:12]] = int(buffer[14:15])
                    entry["Elements"][buffer[18:20]] = int(buffer[22:23])
                    entry["Elements"][buffer[26:28]] = int(buffer[30:31])
                    entry["Elements"][buffer[34:36]] = int(buffer[38:39])
                    entry["Elements"][buffer[42:44]] = int(buffer[46:47])
                    buffer = buffer[51:-1]
                    buffer = re.split(r'\s+', buffer)
                    if float(buffer[0]) != 0:
                        entry["MolecularWeight"] = float(buffer[0])
                        entry["HeatOfFormation"] = float(buffer[1])
                    else:
                        entry["Phase"] = int(buffer[0])
                        entry["MolecularWeight"] = float(buffer[1])
                        entry["HeatOfFormation"] = float(buffer[2])
                    entry["Intervals"] = []
                    line = 3
                    InfoFlag = False
                    IntervalFlag = True

                    # if reactant has no intervals but has t exponents
                    if Intervals == 0:
                        buffer = f.readline()
                        InfoFlag = True
                        IntervalFlag = False
                        line = 1
                        buffer = re.split(r'\s+', buffer)
                        del buffer[0]  # removing whitespace
                        del buffer[-1]  # removing whitespace
                        interval["temp_upper"] = float(buffer[0][0:-1])
                        interval["T_exp"].append(float(buffer[1]))
                        interval["T_exp"].append(float(buffer[2]))
                        interval["T_exp"].append(float(buffer[3]))
                        interval["T_exp"].append(float(buffer[4]))
                        interval["T_exp"].append(float(buffer[5]))
                        interval["T_exp"].append(float(buffer[6]))
                        interval["T_exp"].append(float(buffer[7]))
                        interval["T_exp"].append(float(buffer[8]))
                        interval["EnthalpyDifference"] = float(buffer[9])
                        entry["Intervals"].append(interval)
                        interval = {"temp_lower": 0, "temp_upper": 0, "T_exp": [], "Cp_coes": [], "b_constants": [],
                                    "EnthalpyDifference": 0}
                    continue

            elif IntervalFlag:

                if line == 3:
                    buffer = re.split(r'\s+', buffer)
                    del buffer[0]  # removing whitespace
                    del buffer[-1]  # removing whitespace
                    interval["temp_lower"] = float(buffer[0])
                    interval["temp_upper"] = float(buffer[1][0:-1])
                    interval["T_exp"].append(float(buffer[2]))
                    interval["T_exp"].append(float(buffer[3]))
                    interval["T_exp"].append(float(buffer[4]))
                    interval["T_exp"].append(float(buffer[5]))
                    interval["T_exp"].append(float(buffer[6]))
                    interval["T_exp"].append(float(buffer[7]))
                    interval["T_exp"].append(float(buffer[8]))
                    interval["T_exp"].append(float(buffer[9]))
                    interval["EnthalpyDifference"] = float(buffer[10])
                    line = 4
                    continue

                elif line == 4:
                    interval["Cp_coes"].append(float(buffer[0:16].replace("D", "E")))
                    interval["Cp_coes"].append(float(buffer[16:32].replace("D", "E")))
                    interval["Cp_coes"].append(float(buffer[32:48].replace("D", "E")))
                    interval["Cp_coes"].append(float(buffer[48:64].replace("D", "E")))
                    interval["Cp_coes"].append(float(buffer[64:-1].replace("D", "E")))
                    line = 5
                    continue

                elif line == 5:
                    interval["Cp_coes"].append(float(buffer[0:16].replace("D", "E")))
                    interval["Cp_coes"].append(float(buffer[16:32].replace("D", "E")))
                    interval["b_constants"].append(float(buffer[48:64].replace("D", "E")))
                    interval["b_constants"].append(float(buffer[64:-1].replace("D", "E")))
                    line = 3
                    Intervals = Intervals - 1
                    entry["Intervals"].append(interval)
                    interval = {"temp_lower": 0, "temp_upper": 0, "T_exp": [], "Cp_coes": [], "b_constants": [],
                                "EnthalpyDifference": 0}
                    if Intervals == 0 and InfoFlag == False:
                        line = 1
                        InfoFlag = True
                        IntervalFlag = False
                        if PDFLAG:
                            thermodata["PRODUCTS"][entry["name"]] = entry
                        elif not PDFLAG:
                            thermodata["REACTANTS"][entry["name"]] = entry
                        entry = {}
                        # next species

                    continue


if __name__ == "__main__":
    os.chdir("datasets")
    json.dump(reader("thermo.inp"), indent=4, fp=open("thermo.json", "w"))