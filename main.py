import requests
from bs4 import BeautifulSoup
import hashlib


import pandas as pd 
  
# initialize list of lists 
#data = [['bruh', 'bruh2', 'bruh3']]
data = {'roundID': ['Somu', 'Kiku', 'Amol', 'Lini'],
	'winner': [68, 74, 77, 78],
	'loser': [84, 56, 73, 69]}
# Create the pandas DataFrame 
df = pd.DataFrame(data) 
  
# print dataframe. 
def getrounds(tournamentID, roundID):
    global df
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
        try:
          rounddict = parseresults(bruh2, roundID)
          print(rounddict)
#append row to the dataframe
          df = df.append(rounddict, ignore_index=True)
          #print(rounddict)
          listofrounds.append(rounddict)
          
        except:
          
          pass
    print(listofrounds)


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
    
  


ids = ['600575', '606010', '606007', '600516']
#for i in ids:

getrounds(str(17739), '595338')
print('-----------17739---------------------------------')
print(df)
df.to_excel(r'bruh.xlsx', index = False)


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

