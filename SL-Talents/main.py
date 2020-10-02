########################################################################################
#Edit this section then click run and paste the output into simc
########################################################################################
#spec lookup dict
specs = {'1': 'beast_mastery', '2': 'marksmanship', '3': 'survival'}
########################################################################################
########################################################################################

profile = ""

def getname(talent_numbers, select_spec):
    if (select_spec == 'marksmanship'):
        talent_names_gen = getname_marksmanship(talent_numbers)
    if (select_spec == 'beast_mastery'):
        talent_names_gen = getname_beast_mastery(talent_numbers)
    if (select_spec == 'survival'):
        talent_names_gen = getname_survival(talent_numbers)
    return talent_names_gen


def getname_beast_mastery(talent_numbers):
    talents = [('KI', 'AC', 'DB'), ('SoB', 'OwtP', 'Chim'), ('', '', ''),
               ('SC', 'TotH', 'AmoC'), ('', '', ''),
               ('Stomp', 'Barrage', 'Stampede'), ('AotB', 'KC', 'BS')]
    res = [row[x - 1] for (row, x) in zip(talents, talent_numbers)]
    return '_'.join(r for r in res if r != '')


def getname_marksmanship(talent_numbers):
    talents = [('MaMa', 'SS', 'AMoC'), ('CA', 'Barrage', 'ES'), ('', '', ''),
               ('Steady', 'Stream', 'Chim'), ('', '', ''),
               ('LS', 'DeadEye', 'DT'), ('CTS', 'LnL', 'Volley')]
    res = [row[x - 1] for (row, x) in zip(talents, talent_numbers)]
    return '_'.join(r for r in res if r != '')


def getname_survival(talent_numbers):
    talents = [('VV', 'ToE', 'AP'), ('GT', 'HB', 'Butchery'), ('', '', ''),
               ('BS', 'ST', 'AMoC'), ('', '', ''), ('Tip', 'MB', 'FS'),
               ('BoP', 'WI', 'Chakrams')]
    res = [row[x - 1] for (row, x) in zip(talents, talent_numbers)]
    return '_'.join(r for r in res if r != '')


covenants = ['necrolord', 'venthyr', 'night_fae', 'kyrian']
import itertools
options = [
    range(1, 4),
    range(1, 4), [1],
    range(1, 4), [1],
    range(1, 4),
    range(1, 4)
]

print('Please enter number for spec:')
for spec in specs:
    print(spec, specs[spec])
selection = input()
spec = specs.get(selection, None)
if spec == None:
    print('Invalid spec selected.')
    quit()
print('Do you want to include covenant baseline abilities? y/n')
covenantSelection = input()
includeCovenants = True if covenantSelection == 'y' else False
#print('Do you want the output to be done in profilesets? y/n')
#profileSetSelection = input()
#doProfileSets = True if profileSetSelection == 'y' else False
doProfileSets = False

with open(spec + '/' + spec + '_talents' + ('_covenants' if includeCovenants else '') + ('_profilesets' if doProfileSets else '_copy') + '.simc', 'w') as outputfile:
  for talents in itertools.product(*options):
    temp_names = getname(talents, spec)
    if doProfileSets:
      if includeCovenants:
        for c in covenants:
          profile += "\n" + "profileset.\"" + c + "_" + temp_names + "\""
          profile += "+=covenant=" + c
          profile += "\n" + "profileset.\"" + c + "_" + temp_names + "\""
          profile += "+=talents=" + ''.join(map(str, talents)) + "\n"
      else:
          profile += "\n" + "profileset.\"" + temp_names + "\""
          profile += "+=talents=" + ''.join(map(str, talents)) + "\n"
    else:
      if includeCovenants:
        for c in covenants:
          profile += "\n" + "copy=" + c + "_" + temp_names
          profile += ",talents_" + spec + "\n"
          profile += "talents=" + ''.join(map(str, talents)) + "\n"
          profile += "covenant=" + c + "\n"
      else:
        profile += "\n" + "copy=" + temp_names
        profile += ",talents_" + spec + "\n"
        profile += "talents=" + ''.join(map(str, talents)) + "\n"
        
        #profile += "talents=" + ''.join(map(str, talents)) + '",talents_' + specs + "\n"
        #outputfile.write('copy="' + nameToPrint + '"' + ',bm_covenant_' + covenant + '\n' + 'soulbind=')

  outputfile.write("##############################################################")
  outputfile.write("\n#Replace this with your desired base profile /simc etc \n")
  outputfile.write("##############################################################")
  outputfile.write("\ndefault_actions=1\n")
  outputfile.write(profile)
print('Finished. Please find output in output file.')
