import requests
from bs4 import BeautifulSoup
import hashlib


import pandas as pd 



datalist = [{'TournamentID': '17391', 'VPF': ['585487', '585486', '585485', '585484', '585483', '585482', '585481', '585480'], 'NPF': ['585471', '585470', '585469', '585468', '585467', '585466', '585465', '585464'], 'NLD': ['585463', '585462', '585461', '585460', '585459', '585458', '585457', '585456'], 'VLD': ['585479', '585478', '585477', '585476', '585475', '585474', '585473', '585472'], 'VCX': ['585501', '585500', '585499', '585498', '585496', '585495'], 'NCX': []}, {'TournamentID': '17246', 'VPF': ['618702', '586464', '586463', '586462', '586460', '586459', '586458', '586457'], 'NPF': ['618700', '586472', '586471', '586470', '586468', '586467', '586466', '586465'], 'NLD': ['618699', '586448', '586447', '586446', '586444', '586443', '586442', '586441'], 'VLD': ['618701', '586456', '586455', '586454', '586452', '586451', '586450', '586449'], 'VCX': ['586484', '586483', '586482', '586481', '586480', '586479'], 'NCX': ['586475', '586474', '586473']}, {'TournamentID': '17853', 'VPF': ['606010', '600578', '600576', '600575', '600574', '600573', '600572'], 'NPF': ['606008', '600528', '600526', '600525', '600524', '600523', '600522'], 'NLD': ['606007', '600521', '600519', '600518', '600517', '600516', '600515'], 'VLD': ['606009', '600571', '600570', '600569', '600568', '600567', '600566', '600565'], 'VCX': ['600584', '600582', '600581', '600580', '600579'], 'NCX': ['600534', '600531', '600530', '600529']}, {'TournamentID': '17854', 'VPF': ['600686', '600685', '600684', '600683', '600682', '600681'], 'NPF': ['600637', '600636', '600635', '600634', '600633', '600632', '600631'], 'NLD': ['600630', '600629', '600628', '600627', '600626', '600625', '600624'], 'VLD': ['600680', '600679', '600677', '600676', '600675', '600674'], 'VCX': [], 'NCX': []}, {'TournamentID': '18019', 'VPF': ['608253', '608252', '608251', '608250', '608249', '608248', '608247', '608246'], 'NPF': ['608213', '608212', '608211', '608210', '608209', '608208', '608207'], 'NLD': ['608205', '608204', '608203', '608202', '608201', '608200', '608199'], 'VLD': ['608244', '608243', '608242', '608241', '608240', '608239', '608238'], 'VCX': [], 'NCX': ['608227', '608226', '608225', '608224']}, {'TournamentID': '18358', 'VPF': [], 'NPF': ['668024', '667736', '667735', '667734', '667722', '667721', '667720', '667719'], 'NLD': ['668044', '668043', '668042', '667724', '667723', '667718', '667717'], 'VLD': [], 'VCX': [], 'NCX': []}, {'TournamentID': '17739', 'VPF': ['678360', '595342', '595341', '595340', '595339', '595338', '595337', '595336'], 'NPF': ['595292', '595291', '595290', '595289', '595288', '595287', '595286'], 'NLD': ['678358', '595285', '595284', '595283', '595282', '595281', '595280', '595279'], 'VLD': ['678359', '595335', '595334', '595333', '595332', '595331', '595330', '595329'], 'VCX': ['595348', '595347', '595346', '595345', '595344', '595343'], 'NCX': []}]


# initialize list of lists 
#data = [['bruh', 'bruh2', 'bruh3']]
data = {'roundID': [],
	'winner': [],
	'loser': []}
# Create the pandas DataFrame 
npf = pd.DataFrame(data)
nld = pd.DataFrame(data) 
vpf = pd.DataFrame(data) 
vld = pd.DataFrame(data) 
vcx = pd.DataFrame(data)
ncx = pd.DataFrame(data)

def appendround(rounddict, roundtype):
  try:
    global npf
    global vpf
    global nld
    global vld
    global vcx
    global ncx
    if roundtype == 'VPF':
      roundids = vpf['roundID'].tolist()
      print(rounddict['roundID'])
      if rounddict['roundID'] not in roundids:
        vpf = vpf.append(rounddict, ignore_index=True)
    if roundtype == 'NPF':
      roundids = npf['roundID'].tolist()
      print(rounddict['roundID'])
      if rounddict['roundID'] not in roundids:
        npf = npf.append(rounddict, ignore_index=True)

      
    if roundtype == 'VLD':
      roundids = vld['roundID'].tolist()
      if rounddict['roundID'] not in roundids:
        vld = vld.append(rounddict, ignore_index=True)
      
    if roundtype == 'NLD':
      roundids = nld['roundID'].tolist()
      if rounddict['roundID'] not in roundids:
        nld = nld.append(rounddict, ignore_index=True)
      
    if roundtype == 'VCX':
      roundids = vcx['roundID'].tolist()
      if rounddict['roundID'] not in roundids:
        vcx = vcx.append(rounddict, ignore_index=True)
      
    if roundtype == 'NCX':
      roundids = ncx['roundID'].tolist()
      if rounddict['roundID'] not in roundids:
        ncx = ncx.append(rounddict, ignore_index=True)
  except:
    pass
    

def getrounds(tournamentID, roundID, roundtype):
    global npf
    listofrounds = []
    url = "https://www.tabroom.com/index/tourn/results/round_results.mhtml?tourn_id=" + tournamentID + "&round_id=" + roundID
    fulltextpage = requests.get(url).text
    soup = BeautifulSoup(fulltextpage, 'html.parser')
    
    x  = soup.find_all('tbody')
    #print(x)
    y = x[0].find_all('tr')
    for i in range(len(y)):
        bruh = y[i].get_text()
        bruh2 = ' '.join(bruh.split())
        #try:
        rounddict = parseresults(bruh2, roundID)
          #print(rounddict)
        appendround(rounddict, roundtype)
          #print(rounddict)
          #listofrounds.append(rounddict)
          
        #except:
          
          #pass
    #print(listofrounds)


def findwinner(roundlist):
  aff = roundlist.count('AFF')
  neg = roundlist.count('NEG')
  if aff > neg:
    return True
  else:
    return False
def parseresults(resultstring, rID):

    newdict = {}
    try:
      temp1 = resultstring.replace('CON', 'NEG')
      temp2 = temp1.replace('PRO', 'AFF')
    except:
      pass
    #print(temp2)
    temp3 = temp2.split()
    #print(temp3)
    
    roundentry = []
    #pf and policy rounds
    if '&' in temp3:
      
      for j in temp3:
        #print(temp3)
        quicksortlist = []
        i = 0
        if j.isnumeric():
          x = True
        elif j.isupper():
          x = True
        else:
          x = False
        if len(j) == 2 and i < 3 and x:
          #print(j)
          i += 1
          listindex = temp3.index(j)
          quicksortlist.append(temp3[listindex + 1])
          quicksortlist.append(temp3[listindex + 3])
          
          quicksortlist.sort()
          if len(roundentry) == 2:
            break
          #print(quicksortlist)
          roundentry.append(quicksortlist[0] + ' & ' + quicksortlist[1])

    #ld rounds
    else:
      for j in temp3:
        if len(j) == 2 and j.isupper() and not j.isnumeric():
          listindex = temp3.index(j)
          #print(temp3[listindex + 1] + temp3[listindex + 2])
          roundentry.append(temp3[listindex + 1] + ' ' + temp3[listindex + 2])
          if len(roundentry) == 2:
            break
        #create a round hash id
    if len(roundentry) == 2:
      roundname = rID + ''.join(roundentry)
      
      hash_object = hashlib.md5(bytes(roundname, encoding='utf-8'))
      roundhash = hash_object.hexdigest()
      #print(roundhash)
      newdict['roundID'] = roundhash
      #findwinner
      winner = findwinner(temp3)
      if winner:
        newdict['winner'] = roundentry[0]
        newdict['loser'] = roundentry[1]
      else:
        newdict['winner'] = roundentry[1]
        newdict['loser'] = roundentry[0]
      return newdict
    else:
      pass
      


    
    #print(roundentry)
    #print(rID)
    
  


#for i in ids:

getrounds(str(17739), '595338', 'VPF')
for i in datalist:
  #print(i)
  print("\n")
  bruh = i.keys()
  bruh2 = []
  for j in bruh:
    #print(x[i])
    bruh2.append(j)
  print(bruh2)

print('-----------17739---------------------------------')
print(npf)
npf.to_excel(r'npf.xlsx', index = False)
vpf.to_excel(r'vpf.xlsx', index = False)
vld.to_excel(r'vld.xlsx', index = False)
nld.to_excel(r'nld.xlsx', index = False)
vcx.to_excel(r'vcx.xlsx', index = False)
ncx.to_excel(r'ncx.xlsx', index = False)


'''
Get tournaments from tab api
Get events from tab api
Find novice pf
Find get round ids
For each round get results page html
Parse the results 
Compile them into the pandas database

-------------------------------------------------------------------------------------------------
For i in round
	Check to see if partnership is in json keys
		If not create it
	Then get rating and RD of member 1
	Get rating and RD of member 2
	X = Function glickco (1elo, 1rd, 2elo, 2rd)
	1 elo - x[0]
	2 elo - x[1]
	pandas1 elo update	
	pandas2 elo update

sorting 
'''

