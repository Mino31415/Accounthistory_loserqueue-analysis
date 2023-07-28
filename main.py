from retrievedata import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

API_KEY = "" #put your apikey here
summonerName =  "" #put your summonername here

#get apikey if empty
if API_KEY == "":
    API_KEY = input("Enter your APIKEY: ")
if summonerName == "":
    summonerName = input("Enter Summonername: ")
games = input("Amoun of games to go through")
#
#get account
puuid = uuid(API_KEY, summonerName)[0]

#get your matchhistory, default amount of games is 30
matches = matchids(API_KEY, puuid)

#initializing ally variables
ally1 = []
ally2 = []
ally3 = []
ally4 = []
for match in matches:  #go through the matches
    matchdata = analysis(API_KEY, match, puuid, sleeper=1) #retrieve matchdata
    if matchdata != None: #ignore non Ranked Solo / Duo Matches
        #put data in according list
        ally1.append(matchdata[0])
        ally2.append(matchdata[1])
        ally3.append(matchdata[2])
        ally4.append(matchdata[3])

#handle the data
totaldata = [ally1, ally2, ally3, ally4] #create one big list so that i can loop through it with a for loop
graphdata = [] #list for average performance (5 values per ally)

for ally in totaldata: #get ally from totaldata
    #initiate variables that will be (re-)used for the graph data and count to calculate average
    winratediff = 0
    wrcounter = 0
    dmgtochamps = 0
    dmgccounter = 0
    dmgtoturrets = 0
    dmgtcounter = 0
    gold = 0
    goldcounter = 0
    kda = 0
    kdacounter = 0

    for dataset in ally: #get one single set of data from an ally
        if dataset[0] !=  None:
            winratediff += dataset[0]
            wrcounter += 1
        if dataset[1] !=  None:
            dmgtochamps += dataset[1]
            dmgccounter += 1
        if dataset[2] !=  None:
            dmgtoturrets += dataset[2]
            dmgtcounter += 1
        if dataset[3] !=  None:
            gold += dataset[3]
            goldcounter += 1
        if dataset[4] !=  None:
            kda += dataset[4]
            kdacounter += 1

    graphdata.append([round(winratediff/wrcounter, 1), round(dmgtochamps/dmgccounter, 1), round(dmgtoturrets/dmgtcounter, 1), round(gold/goldcounter, 1), round(kda/kdacounter, 1)])

#list for total average performance (1 value per ally)
average = []
for data in graphdata:
    average.append(round((data[0] + data[1] + data[2] + data[3] + data[4])/5, 1))

print("Analyzed", goldcounter, "Ranked 5v5 Solo / Duo Matches")

#Create graph
#Average graph
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#4C2A85"]) #set colors
fig1, ax1 = plt.subplots()
labels = ["Ally 1", "Ally 2", "Ally 3", "Ally 4"]
ax1.bar(labels, average)
ax1.set_title("Percentual diff in performance per ally")

#Ally 1 Graph
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#0c6e9c"]) #set colors
fig2, ax2 = plt.subplots()
labels = ["%ΔWinrate", "%ΔDamage", "%ΔTowerdmg", "%ΔGold", "ΔKDA"] #set labels for all following graphs
ax2.bar(labels, graphdata[0])
ax2.set_title("Ally 1 percentual diff")

#Ally 2 Graph
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#07823e"]) #set colors
fig3, ax3 = plt.subplots()
ax3.bar(labels, graphdata[1])
ax3.set_title("Ally 2 percentual diff")

#Ally 3 Graph
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#6fa803"]) #set colors
fig4, ax4 = plt.subplots()
ax4.bar(labels, graphdata[2])
ax4.set_title("Ally 3 percentual diff")

#Ally 4 Graph
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#ba5700"]) #set colors
fig5, ax5 = plt.subplots()
ax5.bar(labels, graphdata[3])
ax5.set_title("Ally 4 percentual diff")



#Create GUI
root = tk.Tk()
root.title("Loserqueue / Teammate analysis")
root.state('zoomed')

#create frame for first few graphs
frame_top = tk.Frame(root)
frame_top.pack(fill="both", expand=True)

#first figure
canvas1 = FigureCanvasTkAgg(fig1, frame_top)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

#second figure
canvas2 = FigureCanvasTkAgg(fig2, frame_top)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

#create lower frame
frame_bottom = tk.Frame(root)
frame_bottom.pack(fill="both", expand=True)

#third figure
canvas3 = FigureCanvasTkAgg(fig3, frame_bottom)
canvas3.draw()
canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)

#fourth figure
canvas4 = FigureCanvasTkAgg(fig4, frame_bottom)
canvas4.draw()
canvas4.get_tk_widget().pack(side="left", fill="both", expand=True)

#fifth figure
canvas5 = FigureCanvasTkAgg(fig5, frame_bottom)
canvas5.draw()
canvas5.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()