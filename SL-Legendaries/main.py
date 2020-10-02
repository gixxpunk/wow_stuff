
# Fill this out if you want to use a special profile name that isn't spec + _legendaries
specialProfileName = ""

#Stat bonus IDs for legendaries
# 6648 mastery
# 6649 haste
# 6647 crit
# 6650 vers

#Legendary bonus IDs
#7003 Call of the Wild
#7004 Nessingwary's Trapping Apparatus
#7005 Soulforge Embers
#7006 Craven Strategem
#7007 Dire Command
#7008 Flamewaker's Cobra Sting
#7009 Qa'pla, Eredun War Order
#7010 Rylakstalker's Piercing Fangs
#7011 Eagletalon's True Focus
#7012 Surging Shots
#7013 Serpentstalker's Trickery
#7014 Secrets of the Unblinking Vigil
#7015 Wildfire Cluster
#7016 Rylakstalker's Confounding Strikes
#7017 Latent Poison
#7018 Butcher's Bone Fragments

#spec lookup dict
specs = {'1': 'beast_mastery', '2': 'marksmanship', '3': 'survival'}

# index: ['bonusID', 'Name', ['Slot1', 'slot1ItemID'], ['Slot2', 'slot2ItemID']]
genericLegendaries = {
'1': ['7003', 'Call of the Wild', 'wrist', 'finger1'],
'2': ['7004', "Nessingwary's Trapping Apparatus", 'waist', 'feet'],
'3': ['7005', 'Soulforge Embers', 'head', 'shoulder'],
'4': ['7006', 'Craven Strategem', 'neck', 'chest']
}
beastMasteryLegendaries = {
'1': ['7007', "Dire Command", 'chest', 'finger1'],
'2': ['7008', "Flamewaker's Cobra Sting", 'legs', 'feet'],
'3': ['7009', "Qa'pla Eredun War Order", 'shoulder', 'hands'],
'4': ['7010', "Rylakstalker's Piercing Fangs", 'feet', 'back'],
}
marksmanshipLegendaries = {
'1': ['7011', "Eagletalon's True Focus", 'head', 'waist'],
'2': ['7012', 'Surging Shots', 'neck', 'wrist'],
'3': ['7013', "Serpentstalker's Trickery", 'shoulder', 'finger1'],
'4': ['7014', 'Secrets of the Unblinking Vigil', 'wrist', 'hands'],
}
survivalLegendaries = {
'1': ['7015', 'Wildfire Cluster', 'waist', 'legs'],
'2': ['7016', "Rylakstalker's Confounding Strikes", 'legs', 'back'],
'3': ['7017', 'Latent Poison Injectors', 'head', 'hands'],
'4': ['7018', "Butcher's Bone Fragments", 'chest', 'back'],
}

slotIds = {
'head': '172325',
'neck': '178927',
'shoulder': '172327',
'chest': '172322',
'wrist': '172329',
'hands': '172324',
'waist': '172328',
'legs': '172326',
'feet': '172323',
'finger1': '178926',
'back': '173242',
}


# index: ['bonusID', 'Name']
statIDs = {
'1': ['6647', 'Crit'],
'2': ['6648', 'Mastery'],
'3': ['6649', 'Haste'],
'4': ['6650', 'Versatility'],
}

def getKeyList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list

def generateLegendaries(spec, genericSelection, ilvlSelection, profileName, sameSlotWanted, sameSlotSelection, firstStatSelection, secondStatSelection):
    generatedProfile = ''
    statBonusIDS = '/' + str(firstStatSelection) + '/' + str(secondStatSelection)
    if(spec == 'beast_mastery'):
        for legendary in beastMasteryLegendaries:
            ## First variation of the legendary
            firstLegSlot = sameSlotSelection if sameSlotWanted == 'y' else beastMasteryLegendaries[legendary][2]

            generatedProfile += f"copy=\"{beastMasteryLegendaries[legendary][1]}_{firstLegSlot}\",{profileName}\n"
            generatedProfile += f"{firstLegSlot}=,id={slotIds[firstLegSlot]},bonus_id={beastMasteryLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"

            ## Second variation of the legendary
            secondLegSlot = sameSlotSelection if sameSlotWanted == 'y' else beastMasteryLegendaries[legendary][3]
            generatedProfile += f"copy=\"{beastMasteryLegendaries[legendary][1]}_{secondLegSlot}\",{profileName}\n"
            generatedProfile += f"{secondLegSlot}=,id={slotIds[secondLegSlot]},bonus_id={beastMasteryLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"

    elif(spec == 'marksmanship'):
        for legendary in marksmanshipLegendaries:
            ## First variation of the legendary
            firstLegSlot = sameSlotSelection if sameSlotWanted == 'y' else marksmanshipLegendaries[legendary][2]

            generatedProfile += f"copy=\"{marksmanshipLegendaries[legendary][1]}_{firstLegSlot}\",{profileName}\n"
            generatedProfile += f"{firstLegSlot}=,id={slotIds[firstLegSlot]},bonus_id={marksmanshipLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"

            ## Second variation of the legendary
            secondLegSlot = sameSlotSelection if sameSlotWanted == 'y' else marksmanshipLegendaries[legendary][3]
            generatedProfile += f"copy=\"{marksmanshipLegendaries[legendary][1]}_{secondLegSlot}\",{profileName}\n"
            generatedProfile += f"{secondLegSlot}=,id={slotIds[secondLegSlot]},bonus_id={marksmanshipLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"
    elif(spec == 'survival'):
        for legendary in survivalLegendaries:
            ## First variation of the legendary
            firstLegSlot = sameSlotSelection if sameSlotWanted == 'y' else survivalLegendaries[legendary][2]

            generatedProfile += f"copy=\"{survivalLegendaries[legendary][1]}_{firstLegSlot}\",{profileName}\n"
            generatedProfile += f"{firstLegSlot}=,id={slotIds[firstLegSlot]},bonus_id={survivalLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"

            ## Second variation of the legendary
            secondLegSlot = sameSlotSelection if sameSlotWanted == 'y' else survivalLegendaries[legendary][3]
            generatedProfile += f"copy=\"{survivalLegendaries[legendary][1]}_{secondLegSlot}\",{profileName}\n"
            generatedProfile += f"{secondLegSlot}=,id={slotIds[secondLegSlot]},bonus_id={survivalLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"
    else:
        print("Unknown spec")
        quit()
    if(genericSelection == 'y'):
        for legendary in genericLegendaries:
            ## First variation of the legendary
            firstLegSlot = sameSlotSelection if sameSlotWanted == 'y' else genericLegendaries[legendary][2]

            generatedProfile += f"copy=\"{genericLegendaries[legendary][1]}_{firstLegSlot}\",{profileName}\n"
            generatedProfile += f"{firstLegSlot}=,id={slotIds[firstLegSlot]},bonus_id={genericLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"

            ## Second variation of the legendary
            secondLegSlot = sameSlotSelection if sameSlotWanted == 'y' else genericLegendaries[legendary][3]
            generatedProfile += f"copy=\"{genericLegendaries[legendary][1]}_{secondLegSlot}\",{profileName}\n"
            generatedProfile += f"{secondLegSlot}=,id={slotIds[secondLegSlot]},bonus_id={genericLegendaries[legendary][0]}{statBonusIDS},ilevel={ilvlSelection}\n\n"
    return generatedProfile

def main():
    print('Please enter number for spec:')
    for spec in specs:
        print(spec, specs[spec])
    selection = input()
    spec = specs.get(selection, None)
    if spec == None:
        print('Invalid spec selected.')
        quit()

    print("Do you want to include generic legendaries? y/n")
    genericSelection = input()

    print("What ilevel should the legendaries be?")
    ilvlSelection = input()
    ilvlSelection = int(ilvlSelection)

    print("Do you want to set stats on the legendaries? y/n")
    wantStats = input()

    firstStatSelection = ''
    secondStatSelection = ''

    if wantStats == 'y':
        print("Which first stat should the legendary have?")
        for stat in statIDs:
            print(stat, statIDs[stat][1])
        firstStatSelection = input()

        print("Which second stat should the legendary have?")
        for stat in statIDs:
            if(firstStatSelection == stat):
                continue
            print(stat, statIDs[stat][1])
        secondStatSelection = input()
        firstStatSelection = statIDs[firstStatSelection][0]
        secondStatSelection = statIDs[secondStatSelection][0]
    print("Do you want to generate in same slot? y/n")
    sameSlotWanted = input()

    sameSlotSelection = ''

    if sameSlotWanted == 'y':
        print("Which slot do you want to generate for?")
        for idx, slot in enumerate(slotIds):
            print(idx, slot)
        sameSlotSelection = input()
        slotIDKeyList = getKeyList(slotIds)
        sameSlotSelection = int(sameSlotSelection)
        sameSlotSelection = slotIDKeyList[sameSlotSelection]
    profileName = specialProfileName if len(specialProfileName)>1 else spec + "_legendaries"

    with open(spec + '/' + spec + '_legendaries' + '_ilvl' + str(ilvlSelection) + ('_' + sameSlotSelection if sameSlotWanted == 'y' else '') + '.simc', 'w') as outputfile:
        outputfile.write("##############################################################")
        outputfile.write("\n#Replace this with your desired base profile /simc etc ")
        outputfile.write("\n#Rename the name of your simc import to \"" + profileName + "\" \n")
        outputfile.write("##############################################################")
        outputfile.write("\ndefault_actions=1\n")
        outputfile.write("chart_show_relative_difference=1\n")
        outputfile.write("\n\n")

        writeProfile = ''

        writeProfile += generateLegendaries(spec, genericSelection, ilvlSelection, profileName, sameSlotWanted, sameSlotSelection, firstStatSelection, secondStatSelection)

        outputfile.write(writeProfile)
    print('Finished. Please find output in output file.')

if __name__ == "__main__":
    main()