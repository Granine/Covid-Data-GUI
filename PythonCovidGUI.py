"""covid GUI
a GUI that extract data from covid that displays information in various ways
source of data: CPEN 221 class desinated data
feature 1: plot 4 types of covid data in top to bottom order
feature 2: plot 4 types of covid data in reverse order
feature 3: lookup country based on search result (confirmed and death) and relevent global ranking
feature 4: live action feedback and text indicator
upgeade: colour, location of buttons, window size, font, adaptability to changing of window size (by drag), space usage
"""

#imports
from cgitb import lookup
from covid import Covid

from tkinter import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#debug value
debug=False

class CovidData:

    def __init__(self):
        if debug: print("covid data")
        #create nessasory variable, made global so they can be externally changed if value if problematic or from extenral source
        masterData = self.getMasterCovidData()
        self.dataLen=len(masterData)
        self.confirmed = self.getCase(masterData, "confirmed")
        self.deaths = self.getCase(masterData, "deaths")
        self.active = self.getCase(masterData, "active")
        self.recovered = self.getCase(masterData, "recovered")

    """
    initialize data and retreive data from source
    return: the list of data from the source
    """
    def getMasterCovidData(self) -> list:
        """ this function is called once to get the master data for 
            this application; 
            all data used in this application is derived from data 
            returned by this function
        """
        covid = Covid() #instantiate
        data = covid.get_data()
        if(debug): print(len(data)) 
        if(debug): print(data[159]) 
        return data

    """
    uses the masterdata data1 and returns a list of  data based on desired type/mode
    return confirmed by default (if data is none)
    param: list: covid data in format provided by getMasterCovidData
    param mode: data confirmed/death/active/recovered desired
    return: a list of country data of desired type/mode

    """
    def getCase(self, data1: list, mode) -> list:
        """ this function uses the masterdata data1 and returns a 
            list of (country, confirmed) data
        """
        #append list based on desired type od data
        caseList = []
        if (mode=="confirmed"):
            for i in data1:
                caseList.append((i["country"], i["confirmed"]))
                #print("DEBUG: confirmed is ", confirmed)
        elif (mode=="deaths"):
            for i in data1:
                caseList.append((i["country"], i["deaths"]))
            if debug:print(caseList)
        elif (mode=="active"):
            for i in data1:
                caseList.append((i["country"], i["active"]))
            
        elif (mode=="recovered"):
            for i in data1:
                caseList.append((i["country"], i["recovered"]))
        else:
            return []
        #account for None data type (see discussion board lab2)
        for n, i in enumerate(caseList):
            #if debug:print(type(caseList[n][1]))
            if caseList[n][1]is None:
                caseList = []
                if debug: print("expect empty:", caseList)
                for i in data1:
                    caseList.append((i["country"], i["confirmed"]))
        #sort after data collect, not nessasory for confirmed but after reading spec the order is not guarrentied so 
        #to be safe sort just in case
        caseList.sort(key=lambda second: second[1], reverse=True)
        #if debug:print(caseList)
        return caseList

    """
    a getter that returns the requested data
    param mode: the desired data type
    return: the type of data desired

    """
    def getList(self, mode) -> list:
        #if debug:print("getList", mode)
        #return list of data based on desired type
        if (mode=="confirmed"):
            if debug:print("return type: ", type(self.confirmed))
            return self.confirmed
        elif (mode=="deaths"):
            if debug:print("return type: ", type(self.confirmed))
            return self.deaths
        elif (mode=="active"):
            if debug:print("return type: ", type(self.confirmed))
            return self.active
        elif (mode=="recovered"):
            if debug:print("return type: ", type(self.confirmed))
            return self.recovered
        else:
            return []



   
"""
GUI management and design
"""
class CovidGUI:
    #print("DEBUG: type(masterData) is", type(masterData))
    #print("DEBUG: type(confirmed) is", type(confirmed))
    """
    setup the gui in the provided window
    param _window: the tk in which GUI will be set up
    """
    def __init__(self, _window):
        if debug: print("data retrive")
        self.covid=CovidData()
        self.window=_window
        #instantiate the main window
        self.config()

        self.plotted = False
        """
        display message
        """
        explain_label = Label(master = self.window,
                        height = 1,
                        width = 140,
                        bg="#1f1f1f",
                        fg="#ffb700",
                        font=("Arial", 14),
                        text = "-->First select mode: Confirmed/Active/Death/Recovered, then press plot: highest/lowest 10"
                        ).grid(column=0,row=0,columnspan=3, sticky=W, padx=1, pady=1)
        """
        prepare graph background (also to lock the grid )
        """
        bg_label = Label(master = self.window,
                        height = 50,
                        width = 130,
                        bg="#1f1f1f",
                        ).grid(column=2,row=2,rowspan=15,sticky=NW)

        """
        explain how to search
        """
        searchExplain_label = Label(master = self.window,
                        height = 1,
                        width = 60,
                        bg="#1f1f1f",
                        fg="#ffb700",
                        font=("Arial", 13),
                        text = "Alternatively, enter country name to search, dose does not matter",
                        ).grid(column=2,row=1,sticky=NW, padx=20)
        """
        lookup entry box
        """
        self.Lookup_Entry = Entry(master = self.window,
                        width = 40,
                        bg="#ffb700",
                        )
        self.Lookup_Entry.grid(column=2,row=2,sticky=NW, padx=100)

        """
        associate the button "search" with data lookup
        """
        plotHigh_button = Button(master = self.window,
                        command=lambda: self.search(),
                        height = 2,
                        width = 20,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Search").grid(column=2,row=3,columnspan=2, sticky=NW, padx=150)

        """
        plot the top 10 country based on desired mode 
        """
        plotHigh_button = Button(master = self.window,
                        command = lambda: self.plot("top"),
                        height = 4,
                        width = 20,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Plot: top 10").grid(column=0,row=1,columnspan=2, sticky=EW,  padx=3)

        """
        associate the button ""clear" and clear() function
        """
        clear_button = Button(master = self.window,
                        command = lambda: self.clear(),
                        height = 4,
                        width = 10,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Clear").grid(column=0,row=2,sticky=EW)
        """
        A label that display the current mode
        """
        self.mode:StringVar=StringVar()
        self.mode.set("---")
        mode_label = Label(master = self.window,
                        height = 4,
                        width = 10,
                        fg="#ffb700",
                        bg="#1f1f1f",
                        font=("Arial", 12),
                        textvariable = self.mode).grid(column=1,row=2,sticky=EW)
        """
        the following 4 buttons change the mode of the class to be used from plotting data
        """
        confirm_button = Button(master = self.window,
                        command = lambda: self.setMode("confirmed"),
                        height = 4,
                        width = 10,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Confirmed").grid(column=0,row=3,sticky=EW)
        active_button = Button(master = self.window,
                        command = lambda: self.setMode("active"),
                        height = 4,
                        width = 10,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Active").grid(column=1,row=3,sticky=EW)
        deaths_button = Button(master = self.window,
                        command = lambda: self.setMode("deaths"),
                        height = 4,
                        width = 10,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Death").grid(column=0,row=4,sticky=EW)
        recovered_button = Button(master = self.window,
                        command = lambda: self.setMode("recovered"),
                        height = 4,
                        width = 10,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Recovered").grid(column=1,row=4,sticky=EW)
        """
        plot graph in high to low order by calling plot function 
        """

        plotLow_button = Button(master = self.window,
                        command = lambda: self.plot("bottom"),
                        height = 4,
                        width = 20,
                        bg="#ffb700",
                        fg="#1f1f1f",
                        relief="ridge",
                        text = "Plot: lowest 10").grid(column=0,row=5,columnspan=2, sticky=EW, padx=3)
        """
        display variable message/feedbak on action
        """
        self.message:StringVar=StringVar()
        self.message.set("Greeting, please select option to graph")
        explain_label = Label(master = self.window,
                        height = 2,
                        width = 80,
                        bg="#1f1f1f",
                        fg="#ffb700",
                        font=("Arial", 14),
                        textvariable=self.message,
                        ).grid(column=0,row=6,columnspan=3, sticky=W, padx=1, pady=1)

    """
    search based on content in entry box, result displayed on GUI
    """
    def search(self):
        #clear input and make loopup lower case
        lookup=self.Lookup_Entry.get().lower()
        self.Lookup_Entry.delete(0, END)
        counter=0
        #recovered and active is not counted as they are currently broken
        #search through confirmed case
        for x in self.covid.confirmed:
            counter+=1
            if (str(x[0]).lower()==lookup):
                self.message.set("Country: "+str(x[0])+"|| Confirmed: "+str(x[1])+" Ranked "+str(counter))
        counter=0
        #search through deaths count
        for x in self.covid.deaths:
            counter+=1
            if (str(x[0]).lower()==lookup):
                self.message.set(str(self.message.get())+"|| Deaths: "+str(x[1])+" Ranked "+str(counter))
                return
        self.message.set("no result, check country name: "+str(lookup))
    """
    configure the grid( and set up window)
    """
    def config(self):
        #window
        self.window.geometry("1000x570")
        self.window.title("Covid Data Visualization")
        self.window['background']='#1f1f1f'
        #col length set
        self.window.columnconfigure(0, weight=2)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=8)

    """
    Set mode based on parameter
    param mode: mode to set

    """
    def setMode(self, _mode):
        if (_mode!= ("confirmed" or "deaths" or "active" or "recovered")) and debug:
            print("setMode error")
        self.mode.set(_mode)

    """
    a callback function that presented the GUI and plot the data in graphbased on order and mode desire
    param order: order to plot data
    """
    def plot(self, order):
        """ a callback function for the button;
            plots a histogram of the top 10 confirmed cases 
        """
        global canvas
        #error message if rule is not followed
        if (self.plotted==True):
            self.message.set("Please clear current graph first")
            return
        elif (self.mode.get()=="---"):
            self.message.set("Please select an option to graph")
            return
        self.message.set(str(order)+" 10 countires with "+str(self.mode.get()) +" case is plotted")
        #figure set up
        fig = Figure(figsize = (8, 5))
        plot1= fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master = self.window) 
        #if debug: print(type(self.covid.getList(self.mode.get())))

        #plot by deisred behaviour
        if (order=="top"):
            count10 = [self.covid.getList(self.mode.get())[i] for i in range(10)]
        elif (order=="bottom"):
            count10 = [self.covid.getList(self.mode.get())[i] for i in range(self.covid.dataLen-11, self.covid.dataLen-1)]
        else: 
            count10:list={0}
        x = [count10[i][0] for i in range(10)]
        y = [count10[i][1] for i in range(10)]
        plot1.bar(x, y)
        for tick in plot1.get_xticklabels(): #rotate the text slightly
            tick.set_rotation(20) 
    
        #format graph
        canvas.draw()
        canvas.get_tk_widget().grid(column=2,row=1,rowspan=8,sticky=NW)
        self.plotted = True
        return

        
    """
    Clears the data on GUI

    """
    def clear(self):
        """ a callback for the Clear button """ 
        global canvas
        #message to restore
        self.message.set("cleared, please select an option to graph")
        self.mode.set("---")
        if self.plotted:
            canvas.get_tk_widget().destroy()
            self.plotted = False    

    """
    dsiplay country name
    """
    def displayName(self):
        for x in self.covid.confirmed:
            print(x[0])

"""
    Main function that set the window

"""
if __name__ == "__main__":
    window = Tk()
    Gui= CovidGUI(window)
    #uncomment to window lock
    #window.resizable(0, 0)

    #uncomment to display all country name
    #Gui.displayName()
    window.mainloop()
