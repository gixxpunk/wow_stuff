import networkx as nx
from itertools import combinations
from copy import deepcopy
import csv

#----------------------------------------------------------------------------
#Hit run at the top of the page. Follow on-screen instructions bottom right
#Output will be found in output.simc on the left after program has finished
#----------------------------------------------------------------------------

# TODO:
# Add option to potentially filter out non-DPS soulbind traits?
# Pelagos 328263 328265
# Kleia 329784 328258
# Mikanikos 331725 331726

#spec lookup dict
specs = {'1': 'beast_mastery', '2': 'marksmanship', '3': 'survival'}
#covenant lookup dict
covenants = {'1': 'kyrian', '2': 'night_fae', '3': 'necrolord', '4': 'venthyr'}
#kyrian soulbind lookup dict
kyrianSoulbinds = {
    '1': 'Pelagos',
    '2': 'Kleia',
    '3': 'Forgelite Prime Mikanikos'
}
#kyrian soulbind lookup dict
faeSoulbinds = {'1': 'Niya', '2': 'Dreamweaver', '3': 'Korayn'}
#kyrian soulbind lookup dict
necroSoulbinds = {
    '1': 'Plague Deviser Marileth',
    '2': 'Emeni',
    '3': 'Bonesmith Heirmir'
}
#kyrian soulbind lookup dict
venthyrSoulbinds = {
    '1': 'Nadjia the Mistblade',
    '2': 'Theotar the Mad Duke',
    '3': 'General Draven'
}
#dps relevant conduits - id|category (0 generic, 1 beast_mastery, 2 marksmanship, 3 survival, 4 kyrian, 5 necro, 6 nf, 7 ven) tuples
baseFinesse = [['175', '0']]  #Reversal of Fortune
alteredFinesse = []
basePotency = [
    ['137', '4'],  #Enfeebled Mark
    ['139', '7'],  #Empowered Release
    ['143', '5'],  #Necrotic Barrage
    ['140', '6'],  #Spirit Attunement
    ['183', '1'],  #Ferocious Appetite
    ['185', '1'],  #One With The Beast
    ['253', '1'],  #Bloodletting
    ['223', '1'],  #Echoing Call
    ['189', '2'],  #Brutal Projectiles
    ['192', '2'],  #Deadly Chain
    ['199', '2'],  #Powerful Precision
    ['188', '2'],  #Sharpshooter's Focus
    ['251', '3'],  #Deadly Tandem
    ['252', '3'],  #Flame Infusion
    ['226', '3'],  #Stinging Strike
    ['224', '3'],  #Strength of the Pack
]
alteredPotency = []
baseEndurance = [['', '0']]  #dummy to just make dealing with it later easier
alteredEndurance = []

def countConduits(path):
    potencyCount = 0
    finesseCount = 0
    enduranceCount = 0
    for value in path:
        if 'potency' in value:
            potencyCount += 1
        elif 'finesse' in value:
            finesseCount += 1
        elif 'endurance' in value:
            enduranceCount += 1
    return [potencyCount, finesseCount, enduranceCount]


def conduitCombinatorics(condCount, conduitArray):
    if condCount[0] > len(conduitArray[0]):
        condCount[0] = len(conduitArray[0])
    if condCount[1] > len(conduitArray[1]):
        condCount[1] = len(conduitArray[1])
    if condCount[2] > len(conduitArray[2]):
        condCount[2] = len(conduitArray[2])
    return combinations(conduitArray[0], condCount[0]), combinations(
        conduitArray[1], condCount[1]), combinations(conduitArray[2],
                                                     condCount[2])


def filterConduitArray(potency, finesse, endurance, covenant, spec):
    numbersToRemove = []
    if covenant == 'kyrian':  #remove 5/6/7
        numbersToRemove.extend(['5', '6', '7'])
    elif covenant == 'night_fae':  #remove 4/5/7
        numbersToRemove.extend(['4', '5', '7'])
    elif covenant == 'necrolord':  #remove 4/6/7
        numbersToRemove.extend(['4', '6', '7'])
    elif covenant == 'venthyr':  #remove 4/5/6
        numbersToRemove.extend(['4', '5', '6'])
    if spec == 'beast_mastery':  #remove 2/3
        numbersToRemove.extend(['2', '3'])
    elif spec == 'marksmanship':  #remove 1/3
        numbersToRemove.extend(['1', '3'])
    elif spec == 'survival':  #remove 1/2
        numbersToRemove.extend(['1', '2'])

    for value in potency[:]:
        if value[1] in numbersToRemove:
            potency.remove(value)

    for value in finesse[:]:
        if value[1] in numbersToRemove:
            finesse.remove(value)

    for value in endurance[:]:
        if value[1] in numbersToRemove:
            endurance.remove(value)

    [r.pop(1) for r in potency]
    [r.pop(1) for r in finesse]
    [r.pop(1) for r in endurance]


def replaceConduitText(path):
    tempPath = []
    for node in path:
        if 'endurance' not in node and 'finesse' not in node and 'potency' not in node:
            tempPath.append(node)
    return tempPath


def flattenList(l):
    return [item for sublist in l for item in sublist]

def insertAbbreviatedSoulbindName(nameString):
    with open("soulbind_lookup.txt", mode='r') as csvLookup:
        csvReader = csv.reader(csvLookup)
        for row in csvReader:
            if int(row[0]) >= 1000:
                nameString = nameString.replace(row[0], row[1])
            else:
                nameString = nameString.replace(row[0]+":", row[1]+":")
    return nameString

def getUserInputs():
    print('Please enter number for spec:')
    for spec in specs:
        print(spec, specs[spec])
    selection = input()
    spec = specs.get(selection, None)
    if spec == None:
        print('Invalid spec selected.')
        quit()
    print('Please enter number for covenant:')
    for covenant in covenants:
        print(covenant, covenants[covenant])
    selection = input()
    covenant = covenants.get(selection, None)
    if covenant == 'kyrian':
        print('Please enter number for soulbind:')
        for soulbind in kyrianSoulbinds:
            print(soulbind, kyrianSoulbinds[soulbind])
        selection = input()
        soulbind = kyrianSoulbinds.get(selection, None)
        if soulbind == None:
            print('Invalid soulbind selected.')
            quit()
    elif covenant == 'night_fae':
        print('Please enter number for soulbind:')
        for soulbind in faeSoulbinds:
            print(soulbind, faeSoulbinds[soulbind])
        selection = input()
        soulbind = faeSoulbinds.get(selection, None)
        if soulbind == None:
            print('Invalid soulbind selected.')
            quit()
    elif covenant == 'necrolord':
        print('Please enter number for soulbind:')
        for soulbind in necroSoulbinds:
            print(soulbind, necroSoulbinds[soulbind])
        selection = input()
        soulbind = necroSoulbinds.get(selection, None)
        if soulbind == None:
            print('Invalid soulbind selected.')
            quit()
    elif covenant == 'venthyr':
        print('Please enter number for soulbind:')
        for soulbind in venthyrSoulbinds:
            print(soulbind, venthyrSoulbinds[soulbind])
        selection = input()
        soulbind = venthyrSoulbinds.get(selection, None)
        if soulbind == None:
            print('Invalid soulbind selected.')
            quit()
    else:
        print('Invalid covenant selected.')
        quit()
    rank = input('Please enter desired conduit rank [1-15]\n')
    if int(rank) < 1 or int(rank) > 15:
        print('Invalid rank selected.')
        quit()
    return spec, covenant, soulbind, rank


def buildGraph(soulbind):
    soulbindGraph = nx.DiGraph()
    if soulbind == kyrianSoulbinds['1']:
        soulbindGraph.add_edges_from([('328257', 'finesse1'),
                                      ('328257', 'endurance1'),
                                      ('328257', 'potency1'),
                                      ('finesse1', '329777'),
                                      ('endurance1', '329786'),
                                      ('potency1', '328261'),
                                      ('329777', 'endurance2'),
                                      ('329786', 'endurance2'),
                                      ('328261', 'endurance2'),
                                      ('endurance2', '328265'),
                                      ('endurance2', '328263'),
                                      ('328265', 'potency2'),
                                      ('328263', 'potency2'),
                                      ('potency2', 'potency3'),
                                      ('potency2', 'finesse2'),
                                      ('potency3', '328266'),
                                      ('finesse2', '328266')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '328257', '328266', cutoff=None))
    elif soulbind == kyrianSoulbinds['2']:
        soulbindGraph.add_edges_from([('329776', 'finesse1'),
                                      ('334066', 'potency1'),
                                      ('finesse1', 'potency2'),
                                      ('potency1', 'potency2'),
                                      ('potency2', '329781'),
                                      ('potency2', '329779'),
                                      ('potency2', '329778'),
                                      ('329781', 'potency3'),
                                      ('329779', 'endurance1'),
                                      ('329778', 'finesse2'),
                                      ('potency3', 'endurance2'),
                                      ('finesse2', 'endurance2'),
                                      ('endurance1', 'endurance2'),
                                      ('endurance2', '329784'),
                                      ('endurance2', '328258'),
                                      ('329784', '329791'), ('328258',
                                                             '329791')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '329776', '329791', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '334066', '329791', cutoff=None))
    elif soulbind == kyrianSoulbinds['3']:
        soulbindGraph.add_edges_from([('331610', 'finesse1'), 
                                      ('331609', 'potency1'),
                                      ('finesse1', 'endurance1'),
                                      ('potency1', 'endurance1'),
                                      ('endurance1', '333935'),
                                      ('endurance1', '331612'),
                                      ('endurance1', '331611'),
                                      ('333935', 'endurance2'),
                                      ('331612', 'finesse2'),
                                      ('331611', 'potency2'),
                                      ('endurance2', 'potency3'),
                                      ('finesse2', 'potency3'),
                                      ('potency2', 'potency3'),
                                      ('potency3', '331726'),
                                      ('potency3', '331725'),
                                      ('331726', '333950'), ('331725',
                                                             '333950')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '331610', '333950', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '331609', '333950', cutoff=None))
    elif soulbind == faeSoulbinds['1']:
        soulbindGraph.add_edges_from([('342270', 'potency1'),
                                      ('320658', 'endurance1'),
                                      ('potency1', 'finesse1'),
                                      ('endurance1', 'finesse1'),
                                      ('finesse1', '320659'),
                                      ('finesse1', '320660'),
                                      ('finesse1', '320662'),
                                      ('320659', 'endurance2'),
                                      ('320660', 'potency2'),
                                      ('320662', 'finesse2'),
                                      ('endurance2', 'potency3'),
                                      ('potency2', 'potency3'),
                                      ('finesse2', 'potency3'),
                                      ('potency3', '320668'),
                                      ('potency3', '320687'),
                                      ('320668', '322721'), ('320687',
                                                             '322721')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '342270', '322721', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '320658', '322721', cutoff=None))
    elif soulbind == faeSoulbinds['2']:
        soulbindGraph.add_edges_from([('319191', 'finesse1'),
                                      ('319191', 'potency1'),
                                      ('finesse1', 'endurance1'),
                                      ('potency1', 'endurance1'),
                                      ('endurance1', '319210'),
                                      ('endurance1', '319211'),
                                      ('endurance1', '319213'),
                                      ('319210', 'endurance2'),
                                      ('319211', 'potency2'),
                                      ('319213', 'finesse2'),
                                      ('endurance2', 'potency3'),
                                      ('potency2', 'potency3'),
                                      ('finesse2', 'potency3'),
                                      ('potency3', '319214'),
                                      ('potency3', '319216'),
                                      ('319214', '319217'), ('319216',
                                                             '319217')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '319191', '319217', cutoff=None))
    elif soulbind == faeSoulbinds['3']:
        soulbindGraph.add_edges_from([('325067', 'potency1'),
                                      ('325065', 'finesse1'),
                                      ('potency1', 'endurance1'),
                                      ('finesse1', 'endurance1'),
                                      ('endurance1', '325068'),
                                      ('endurance1', '325069'),
                                      ('endurance1', '325601'),
                                      ('325068', 'potency2'),
                                      ('325069', 'endurance2'),
                                      ('325601', 'finesse2'),
                                      ('potency2', 'potency3'),
                                      ('endurance2', 'potency3'),
                                      ('finesse2', 'potency3'),
                                      ('potency3', '325072'),
                                      ('potency3', '325073'),
                                      ('325072', '325066'), ('325073',
                                                             '325066')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '325067', '325066', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '325065', '325066', cutoff=None))
    elif soulbind == necroSoulbinds['1']:
        soulbindGraph.add_edges_from([('323074', 'endurance1'),
                                      ('323074', 'potency1'),
                                      ('323074', 'finesse1'),
                                      ('endurance1', '323089'),
                                      ('potency1', '323091'),
                                      ('finesse1', '323090'),
                                      ('323089', 'finesse2'),
                                      ('323091', 'finesse2'),
                                      ('323090', 'finesse2'),
                                      ('finesse2', '323079'),
                                      ('finesse2', '323081'),
                                      ('323079', 'potency2'),
                                      ('323081', 'potency2'),
                                      ('potency2', 'endurance2'),
                                      ('potency2', 'potency3'),
                                      ('endurance2', '323095'),
                                      ('potency3', '323095')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '323074', '323095', cutoff=None))
    elif soulbind == necroSoulbinds['2']:
        soulbindGraph.add_edges_from([('323921', 'finesse1'),
                                      ('341650', 'endurance1'),
                                      ('finesse1', 'potency1'),
                                      ('endurance1', 'potency1'),
                                      ('potency1', '324440'),
                                      ('potency1', '324441'),
                                      ('324440', 'potency2'),
                                      ('324441', 'potency2'),
                                      ('potency2', '323918'),
                                      ('potency2', '323919'),
                                      ('potency2', '323916'),
                                      ('323918', 'potency3'),
                                      ('323919', 'endurance2'),
                                      ('323916', 'finesse2'),
                                      ('potency3', '342156'),
                                      ('endurance2', '342156'),
                                      ('finesse2', '342156')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '323921', '342156', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '341650', '342156', cutoff=None))
    elif soulbind == necroSoulbinds['3']:
        soulbindGraph.add_edges_from([('326504', 'endurance1'),
                                      ('326507', 'potency1'),
                                      ('endurance1', 'potency2'),
                                      ('potency1', 'potency2'),
                                      ('potency2', '326509'),
                                      ('potency2', '326511'),
                                      ('potency2', '326572'),
                                      ('326509', 'finesse1'),
                                      ('326511', 'potency3'),
                                      ('326572', 'endurance2'),
                                      ('finesse1', 'endurance3'),
                                      ('potency3', 'endurance3'),
                                      ('endurance2', 'endurance3'),
                                      ('endurance3', '326512'),
                                      ('endurance3', '326513'),
                                      ('326512', '326514'), ('326513',
                                                             '326514')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '326504', '326514', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '326507', '326514', cutoff=None))
    elif soulbind == venthyrSoulbinds['1']:
        soulbindGraph.add_edges_from([('331576', 'potency1'),
                                      ('331577', 'endurance1'),
                                      ('potency1', 'finesse1'),
                                      ('endurance1', 'finesse1'),
                                      ('finesse1', '331579'),
                                      ('331579', 'finesse2'),
                                      ('331579', 'potency2'),
                                      ('331579', 'endurance2'),
                                      ('finesse2', '331580'),
                                      ('potency2', '331582'),
                                      ('endurance2', '331584'),
                                      ('331580', 'potency3'),
                                      ('331582', 'potency3'),
                                      ('331584', 'potency3'),
                                      ('potency3', '331586')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '331576', '331586', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '331577', '331586', cutoff=None))
    elif soulbind == venthyrSoulbinds['2']:
        soulbindGraph.add_edges_from([('336140', 'potency1'),
                                      ('336147', 'finesse1'),
                                      ('potency1', 'potency2'),
                                      ('finesse1', 'potency2'),
                                      ('potency2', '336243'),
                                      ('potency2', '336239'),
                                      ('potency2', '336245'),
                                      ('336243', 'endurance1'),
                                      ('336239', 'finesse2'),
                                      ('336245', 'potency3'),
                                      ('endurance1', 'endurance2'),
                                      ('finesse2', 'endurance2'),
                                      ('potency3', 'endurance2'),
                                      ('endurance2', '336247'),
                                      ('endurance2', '336184'),
                                      ('336247', '319983'), ('336184',
                                                             '319983')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '336140', '319983', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '336147', '319983', cutoff=None))
    elif soulbind == venthyrSoulbinds['3']:
        soulbindGraph.add_edges_from([('332755', 'endurance1'),
                                      ('332756', 'endurance1'),
                                      ('endurance1', '319973'),
                                      ('endurance1', '332753'),
                                      ('endurance1', '332754'),
                                      ('319973', 'finesse1'),
                                      ('332753', 'endurance2'),
                                      ('332754', 'potency1'),
                                      ('finesse1', 'potency2'),
                                      ('endurance2', 'potency2'),
                                      ('potency1', 'potency2'),
                                      ('potency2', '319978'),
                                      ('potency2', '319982'),
                                      ('319978', 'potency3'),
                                      ('319982', 'endurance3'),
                                      ('potency3', '340159'),
                                      ('endurance3', '340159')])
        paths = list(
            nx.all_simple_paths(
                soulbindGraph, '332755', '340159', cutoff=None))
        paths += list(
            nx.all_simple_paths(
                soulbindGraph, '332756', '340159', cutoff=None))
    return soulbindGraph, paths


def main():
    printSpecific = input('Do you wish to print a specific combination? y/n \n')
    if(printSpecific == 'y'):
        spec, covenant, soulbind, rank = getUserInputs()
        generateCombos(spec, covenant, soulbind, rank)
        print('Finished. Please find output in relevant folder(s).')
    elif(printSpecific == 'n'):
        rank = input('Which rank do you want the soulbinds to be?\n')
        if int(rank) < 1 or int(rank) > 15:
            print('Invalid rank selected.')
            quit()
        for specKey in specs:
            spec = specs.get(specKey, None)
            for covenantKey in covenants:
                covenant = covenants.get(covenantKey, None)
                if(covenant == 'kyrian'):
                    for soulbindKey in kyrianSoulbinds:
                        soulbind = kyrianSoulbinds.get(soulbindKey, None)
                        generateCombos(spec, covenant, soulbind, rank)
                if(covenant == 'night_fae'):
                    for soulbindKey in faeSoulbinds:
                        soulbind = faeSoulbinds.get(soulbindKey, None)
                        generateCombos(spec, covenant, soulbind, rank)
                if(covenant == 'necrolord'):
                    for soulbindKey in necroSoulbinds:
                        soulbind = necroSoulbinds.get(soulbindKey, None)
                        generateCombos(spec, covenant, soulbind, rank)
                if(covenant == 'venthyr'): 
                    for soulbindKey in venthyrSoulbinds:
                        soulbind = venthyrSoulbinds.get(soulbindKey, None)
                        generateCombos(spec, covenant, soulbind, rank)
        print('Finished. Please find output in relevant folder(s).')
    else:
        print("Invalid input, please choose y or n.")
        quit()

def generateCombos(spec, covenant, soulbind, rank):
    print('Generating Profiles for ' + spec + '_' + covenant + '_' + soulbind + '_' + 'rank' + rank)
    profile = ""
    with open(spec + '/' + spec + '_' + covenant + '_' + soulbind + '_' + 'rank' + rank + '.simc', 'w') as outputfile:
        outputfile.write(
            "#Replace this with your desired base profile /simc etc \n\ncovenant="
            + covenant + "\n")

        alteredPotency = deepcopy(basePotency)
        alteredEndurance = deepcopy(baseEndurance)
        alteredFinesse = deepcopy(baseFinesse)

        filterConduitArray(alteredPotency, alteredFinesse, alteredEndurance, covenant, spec)

        soulbindGraph, paths = buildGraph(soulbind)

        for path in paths:
            conduitCount = countConduits(path)
            newPath = replaceConduitText(path)
            potencyCombos, finesseCombos, enduranceCombos = conduitCombinatorics(
                conduitCount, [
                    flattenList(alteredPotency),
                    flattenList(alteredFinesse),
                    flattenList(alteredEndurance)
                ])
            potencyComboList = []
            finesseComboList = []
            enduranceComboList = []
            profile = ''
            for node in newPath:
                profile += node + "/"
            for potencyCombo in potencyCombos:
                potencyComboList.append(potencyCombo)
            for finesseCombo in finesseCombos:
                finesseComboList.append(finesseCombo)
            for enduranceCombo in enduranceCombos:
                enduranceComboList.append(enduranceCombo)
            for potCondTuple in potencyComboList:
                for finCondTuple in finesseComboList:
                    for endCondTuple in enduranceComboList:
                        profileToPrint = profile
                        for potCond in potCondTuple:
                            if (potCond != ''):
                                profileToPrint += potCond + ":R" + rank + "/"
                        for finCond in finCondTuple:
                            if (finCond != ''):
                                profileToPrint += finCond + ":R" + rank + "/"
                        for endCond in endCondTuple:
                            if (endCond != ''):
                                profileToPrint += endCond + ":R" + rank + "/"
                        if (profileToPrint[-1] == '/'):
                            profileToPrint = profileToPrint[:-1]
                        nameToPrint = insertAbbreviatedSoulbindName(profileToPrint)
                        outputfile.write('copy="' + nameToPrint + '"' + ',covenant_' + covenant + '\n' + 'soulbind=')
                        outputfile.write(profileToPrint + '\n')

if __name__ == "__main__":
    main()
