from tkinter import *
import requests
from requests import Session
import json
import _thread
from chatty import create
from tornado.ioloop import IOLoop
import codecs
import serial
from serial.tools import list_ports
from time import sleep

class ConfettiDisplay(Frame):

    def __init__(self, master):
        Frame.__init__(self,master)

        self.master=master

        self.startvariable=1
        self.initWindow()
        self.defaults()
        self.pack()
        self.checkboxdisabler()

    def initWindow(self):
        self.gui= Frame()

        self.streamjarLabel = Label(self.gui, text='StreamJar:')

        self.streamjarframe = Frame(self.gui)


        self.goalreached = IntVar()
        self.goalreachedcb = Checkbutton(self.gui, text="Launch Confetti if goal is reached",variable=self.goalreached, command=self.checkboxdisabler)

        self.donation = IntVar()
        self.donationcb = Checkbutton(self.streamjarframe, text="Launch Confetti if a user donates at least $",variable=self.donation, command=self.checkboxdisabler)

        self.donationamount = StringVar()
        self.donationamountenty = Entry(self.streamjarframe, textvariable=self.donationamount,width=7)
        self.donationamountenty.bind('<KeyPress>',self.onlyNumbers)

        self.percentreachedframe = Frame(self.gui)

        self.percentreached = IntVar()
        self.percentreachedcb = Checkbutton(self.percentreachedframe, text="Lauch Confetti every ",variable=self.percentreached, command=self.checkboxdisabler)

        self.percentreachedamount = StringVar()
        self.percentreachedamountentry = Entry(self.percentreachedframe,textvariable=self.percentreachedamount,width=5)
        self.percentreachedamountentry.bind('<KeyPress>', self.onlyNumbers)

        self.percentinfo = Label(self.percentreachedframe, text="% (goes over 100)")

        self.APIkeyframe = Frame(self.gui)

        self.APILabel = Label(self.APIkeyframe, text="API key:")

        self.APIkey = StringVar()
        self.APIkeyentry = Entry(self.APIkeyframe, textvariable=self.APIkey)

        self.beamLabel = Label(self.gui,text="Beam:")

        self.newsubscriber = IntVar()
        self.newsubscribercb = Checkbutton(self.gui,text="Launch Confetti for every new subscriber",variable=self.newsubscriber, command=self.checkboxdisabler)

        self.bloginframe = Frame(self.gui)

        self.busernamelabel = Label(self.bloginframe, text="Username:")

        self.busername = StringVar()
        self.busernameentry = Entry(self.bloginframe, textvariable=self.busername)

        self.bpasswordlabel = Label(self.bloginframe, text="Password:")

        self.bpassword = StringVar()
        self.bpasswordentry = Entry(self.bloginframe, textvariable=self.bpassword)

        self.confettibotlabel = Label(self.gui,text="Confettibot (Beam chat bot):")

        self.confettibot = IntVar()
        self.confettibotcb = Checkbutton(self.gui, text="Allow Beam subscribers to run the command ", variable=self.confettibot, command=self.checkboxdisabler)

        self.confettibotcommand = StringVar()
        self.confettibotcommandentry = Entry(self.gui, textvariable=self.confettibotcommand, justify=CENTER)

        self.innerconfettibot = Frame(self.gui)

        self.cbcommandinfo = Label(self.innerconfettibot, text="       to launch confetti")

        self.timespermonth = StringVar()
        self.timespermonthentry = Entry(self.innerconfettibot, textvariable=self.timespermonth, width=3, justify=CENTER)
        self.timespermonthentry.bind('<KeyPress>', self.onlyNumbers)

        self.morecommandinfo = Label(self.innerconfettibot, text=" time(s) until it is ")

        self.resetsubscriberpoints = Button(self.innerconfettibot, text="Reset", command=self.resetsubpoints)

        self.nonsubscriberslabel = Label(self.gui, text="       Nonsubscribers who run the command will be told:")

        self.indentframe = Frame(self.gui)

        self.blankLabel = Label(self.indentframe, text="       ")

        self.confettibotchattext = Text(self.indentframe, width=34, height=5, wrap='word')
        self.confettibotchattext.bind('<Return>',self.noEnterInText)

        self.secondindentframe = Frame(self.gui)

        self.blankLabel2 = Label(self.secondindentframe, text="           ")

        self.confettibotchatfrequency = IntVar()
        self.confettibotchatfrequencycb = Checkbutton(self.secondindentframe, text="Have ConfettiBot display this message", variable=self.confettibotchatfrequency, command=self.checkboxdisabler)

        self.cbchatfrequencyinfo = Label(self.secondindentframe, text="       in stream chat every now and then")

        self.displaylabel = Label(self.gui, text="")

        self.confettiactivatedframe = Frame(self.gui)

        self.confettiactivatedlabel = Label(self.confettiactivatedframe, text="Confetti Poppers Loaded: ")

        self.confettiactivatedentryvariable = StringVar()
        self.confettiactivatedentry = Entry(self.confettiactivatedframe, textvariable=self.confettiactivatedentryvariable, width=5)
        self.confettiactivatedentry.bind('<KeyPress>', self.onlyNumbers)

        self.button = Button(self.gui, text=" Start ", command=self.start)

        self.calibrate = Button(self.gui, text= "Tighten", command=self.tighten, state=DISABLED)

        self.testconfetti = Button(self.gui, text="Launch Confetti", command=self.activatemotorfunction, state=DISABLED)

    def pack(self):
        self.gui.pack(padx=10,pady=5)
        self.streamjarLabel.grid(row=0,sticky=W)
        self.goalreachedcb.grid(row=1,sticky=W)
        self.streamjarframe.grid(row=2, sticky=W)
        self.donationcb.grid(row=0,sticky=W)
        self.donationamountenty.grid(row=0,column=1,sticky=W)
        self.percentreachedframe.grid(row=3, sticky=W)
        self.percentreachedcb.grid()
        self.percentreachedamountentry.grid(row=0,column=1)
        self.percentinfo.grid(row=0,column=2)
        self.APIkeyframe.grid(row=4)
        self.APILabel.grid()
        self.APIkeyentry.grid(row=0, column=1)
        self.beamLabel.grid(row=5,sticky=W)
        self.newsubscribercb.grid(row=7,sticky=W)
        self.bloginframe.grid(row=6)
        self.busernamelabel.grid(row=0,column=0,sticky=W)
        self.busernameentry.grid(row=0,column=1,sticky=E)
        self.bpasswordlabel.grid(row=1, column=0,sticky=W)
        self.bpasswordentry.grid(row=1, column=1,sticky=E)
        #self.confettibotlabel.grid(row=8,sticky=W)
        self.confettibotcb.grid(row=9, sticky=W)
        self.confettibotcommandentry.grid(row=10)
        self.innerconfettibot.grid(row=11, sticky=W)
        self.cbcommandinfo.grid()
        self.timespermonthentry.grid(row=0, column=1)
        self.morecommandinfo.grid(row=0, column=2)
        self.resetsubscriberpoints.grid(row=0,column=3)
        self.nonsubscriberslabel.grid(row=12, sticky=W)
        self.indentframe.grid(row=13, sticky=W)
        self.blankLabel.grid()
        self.confettibotchattext.grid(row=0, column=1,sticky=E)
        self.secondindentframe.grid(row=14, sticky=W)
        self.blankLabel2.grid()
        self.confettibotchatfrequencycb.grid(row=0,column=1, sticky=W)
        self.cbchatfrequencyinfo.grid(row=1,column=1,sticky=W)
        self.displaylabel.grid(row=15)
        self.confettiactivatedframe.grid(row=16)
        self.confettiactivatedlabel.grid()
        self.confettiactivatedentry.grid(row=0, column=1)
        self.button.grid(row=17)
        self.calibrate.grid(row=18)
        self.calibrate.config(state=DISABLED)
        self.testconfetti.grid(row=19)

    def defaults(self):
        defaulter = open("defaults.txt", "r")
        self.line=defaulter.readlines()
        self.goalreached.set(int(self.line[3]))
        self.donation.set(int(self.line[5]))
        self.percentreached.set(int(self.line[7]))
        self.newsubscriber.set(int(self.line[9]))
        self.confettibot.set(int(self.line[11]))
        self.confettibotchatfrequency.set(int(self.line[13]))
        self.donationamount.set(self.line[15][0:len(self.line[15])-1])
        self.percentreachedamount.set(self.line[17][0:len(self.line[17])-1])
        self.APIkey.set(self.line[19][0:len(self.line[19])-1])
        self.busername.set(self.line[21][0:len(self.line[21])-1])
        self.bpassword.set(self.line[23][0:len(self.line[23])-1])
        self.confettibotcommand.set(self.line[25][0:len(self.line[25])-1])
        self.timespermonth.set(self.line[27][0:len(self.line[27])-1])
        self.confettibotchattext.insert('1.0',self.line[29][0:len(self.line[29])-1])
        defaulter.close()

    def checkboxdisabler(self):
        if self.newsubscriber.get()==0+self.confettibot.get()+self.confettibotchatfrequency.get()==0:
            self.busernamelabel.config(state=DISABLED)
            self.busernameentry.config(state=DISABLED)
            self.bpasswordlabel.config(state=DISABLED)
            self.bpasswordentry.config(state=DISABLED)
        else:
            self.busernamelabel.config(state=NORMAL)
            self.busernameentry.config(state=NORMAL)
            self.bpasswordlabel.config(state=NORMAL)
            self.bpasswordentry.config(state=NORMAL)
        if self.confettibot.get()==0:
            self.confettibotcommandentry.config(state=DISABLED)
            self.timespermonthentry.config(state=DISABLED)
            self.resetsubscriberpoints.config(state=DISABLED)
        else:
            self.confettibotcommandentry.config(state=NORMAL)
            self.timespermonthentry.config(state=NORMAL)
            self.resetsubscriberpoints.config(state=NORMAL)
        if self.confettibot.get()+self.confettibotchatfrequency.get()==0:
            self.confettibotchattext.config(state=DISABLED, bg='gray95', fg='gray')
        else:
            self.confettibotchattext.config(state=NORMAL, bg='white', fg='black')
        if self.goalreached.get()+self.donation.get()+self.percentreached.get()==0:
            self.APILabel.config(state=DISABLED)
            self.APIkeyentry.config(state=DISABLED)
        else:
            self.APILabel.config(state=NORMAL)
            self.APIkeyentry.config(state=NORMAL)

    def noEnterInText(self,event):
        return 'break'

    def onlyNumbers(self,event):
        if event.char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\b'):
            pass
        else:
            return 'break'

    def start(self):
        checks = [self.goalreached.get(),self.donation.get(),self.percentreached.get(),self.newsubscriber.get(),self.confettibot.get(),self.confettibotchatfrequency.get()]
        if sum(checks[0:6])==0:
            self.displaylabel.config(text="Check something you silly goose",bg='indian red')
            return
        self.noErrors = 0
        self.activatemotor = 0
        self.chats = 0
        if not self.confettiactivatedentryvariable.get() or int(self.confettiactivatedentryvariable.get())==0:
            self.displaylabel.config(text="Invalid Confetti Popper Amount", bg='indian red')
            self.noErrors = 1
            return
        if checks[1] == 1:
            if not self.donationamount.get():
                self.displaylabel.config(text="Invalid donation amount",bg='indian red')
                self.noErrors = 1
                return
            if int(self.donationamount.get()) <= 0:
                self.displaylabel.config(text="Invalid donation amount",bg='indian red')
                self.noErrors = 1
                return
            _thread.start_new_thread(self.donationTester, (self.donationamount.get(), self.APIkey.get()))
        if checks[0] + checks[2] > 0:
            send = 100
            if checks[2] == 1:
                if not self.percentreachedamount.get():
                    self.displaylabel.config(text="Invalid percent",bg='indian red')
                    self.noErrors = 1
                    return
                if int(self.percentreachedamount.get()) == 0:
                    self.displaylabel.config(text="Invalid percent",bg='indian red')
                    self.noErrors = 1
                    return
                send = int(self.percentreachedamount.get())
            _thread.start_new_thread(self.goalTester, (send, self.APIkey.get()))
        if checks[4]==1:
            if not self.timespermonth.get():
                self.displaylabel.config(text="Invalid times per month entry",bg='indian red')
                self.noErrors = 1
                return
            if not self.confettibotcommand.get():
                self.displaylabel.config(text="Invalid command",bg='indian red')
                self.noErrors = 1
                return
            if int(self.timespermonth.get()) <= 0:
                self.displaylabel.config(text="Invalid times per month entry",bg='indian red')
                self.noErrors = 1
                return
        if checks[3] + checks[4] + checks[5] > 0:
            try:
                self.session = Session()
                self.login_response = self.session.post("https://beam.pro/api/v1/users/login", data={
                    "username": self.busername.get(),
                    "password": self.bpassword.get()
                })
                self.login_response.json().get("channel").get("id")
            except:
                self.session.close()
                self.noErrors = 1
                self.displaylabel.config(text="Invalid username or passord",bg='indian red')
                return
            else:
                if checks[3] == 1:
                    _thread.start_new_thread(self.newSubscriberTester, (
                        self.login_response.json().get("channel").get("id"),
                        self.login_response.headers.get('X-CSRF-Token')))
                if checks[4] + checks[5] > 0:
                    _thread.start_new_thread(self.confettiBotTester, (10,10))
        self.displaylabel.config(text="Program is Running",bg='green3')
        self.goalreachedcb.config(state=DISABLED)
        self.donationcb.config(state=DISABLED)
        self.donationamountenty.config(state=DISABLED)
        self.percentreachedcb.config(state=DISABLED)
        self.percentreachedamountentry.config(state=DISABLED)
        self.percentinfo.config(state=DISABLED)
        self.APILabel.config(state=DISABLED)
        self.APIkeyentry.config(state=DISABLED)
        self.newsubscribercb.config(state=DISABLED)
        self.busernamelabel.config(state=DISABLED)
        self.busernameentry.config(state=DISABLED)
        self.bpasswordlabel.config(state=DISABLED)
        self.bpasswordentry.config(state=DISABLED)
        self.confettibotcb.config(state=DISABLED)
        self.confettibotcommandentry.config(state=DISABLED)
        self.cbcommandinfo.config(state=DISABLED)
        self.timespermonthentry.config(state=DISABLED)
        self.morecommandinfo.config(state=DISABLED)
        self.nonsubscriberslabel.config(state=DISABLED)
        self.confettibotchattext.config(state=DISABLED,bg='gray95',fg='gray')
        self.confettibotchatfrequencycb.config(state=DISABLED)
        self.cbchatfrequencyinfo.config(state=DISABLED)
        _thread.start_new_thread(self.activateMotorTester, (10,10))
        self.button.config(command=self.stop,text="Stop")
        self.calibrate.config(state=NORMAL)
        self.testconfetti.config(state=NORMAL)
        _thread.start_new_thread(self.storedefaults, (10, 10))
        self.turnon()

    def storedefaults(self,unused,unused2):
        self.line[3] =str(self.goalreached.get())+"\n"
        self.line[5] =str(self.donation.get())+"\n"
        self.line[7] =str(self.percentreached.get())+"\n"
        self.line[9] =str(self.newsubscriber.get())+"\n"
        self.line[11] =str(self.confettibot.get())+"\n"
        self.line[13] =str(self.confettibotchatfrequency.get())+"\n"
        self.line[15] =self.donationamount.get()+"\n"
        self.line[17] =self.percentreachedamount.get()+"\n"
        self.line[19] =self.APIkey.get()+"\n"
        self.line[21] =self.busername.get()+"\n"
        self.line[23] =self.bpassword.get()+"\n"
        self.line[25] =self.confettibotcommand.get()+"\n"
        self.line[27] =self.timespermonth.get()+"\n"
        self.line[29] =self.confettibotchattext.get('1.0', 'end-1c')+"\n"
        store_defaults=open("defaults.txt",'w')
        for info in self.line:
            store_defaults.write(info)
        store_defaults.close()

    def donationTester(self,amount,key):
        latestdonation=""
        while self.noErrors==0:
            try:
                donationinfo = requests.get(url="https://streamjar.tv/api/v1/donations?apikey=" + key,params={'test':'true','limit': 1})
                if '{"error":"Invalid key."}' in donationinfo.text:
                    self.displaylabel.config(text="Invalid API key",bg='indian red')
                    self.noErrors=1
                    break
                donationstats=json.loads(donationinfo.text)
                if not donationstats:
                    pass
                else:
                    if latestdonation=="":
                        latestdonation = donationstats[0].get('id')
                    if int(donationstats[0].get('amount'))>=int(amount) and latestdonation!=donationstats[0].get('id'):
                        self.activatemotor=self.activatemotor+1
                        latestdonation = donationstats[0].get('id')

            except:
                self.displaylabel.config(text="Unexpected Error in Donation Tester",bg='indian red')
                self.noErrors=1

    def goalTester(self,percent,key):
        initialpercent=-10
        id=""
        cancel = 1
        while self.noErrors==0:
            try:
                goalinfo = requests.get(url="https://streamjar.tv/api/v1/goals?apikey=" + key)
                goalstats = json.loads(goalinfo.text)
                if not goalstats:
                    self.displaylabel.config(text="Didn't find a streamjar goal",bg='indian red')
                    self.noErrors=1
                    return
                active=0
                for index, goals in enumerate(goalstats):
                    if goalstats[index].get('active') == True:
                        active=1
                        if id==goalstats[index].get('id'):
                            if initialpercent==-10:
                                initialpercent=int(goalstats[index].get('current'))*100/int(goalstats[index].get('total'))
                                if initialpercent>=100 and self.percentreached.get()==0:
                                    cancel=0
                            if int(goalstats[index].get('current'))*100/int(goalstats[index].get('total'))-percent*(initialpercent//percent)>=percent and cancel!=0:
                                self.activatemotor=self.activatemotor+1
                                initialpercent=-10
                                print("Confetti!")
                        else:
                            initialpercent=-10
                            id=goalstats[index].get('id')
                if active==0:
                    self.displaylabel.config(text="All streamjar goals are inactive",bg='indian red')
                    self.noErrors=1
                    return
            except:
                self.displaylabel.config(text="Unexpected Error in Goal Tester",bg='indian red')
                self.noErrors = 1

    def newSubscriberTester(self,channelid,token):
        subscribers=-10
        while self.noErrors==0:
            try:
                basicinfo = self.session.get("https://beam.pro/api/v1/channels/"+str(channelid)+"/details",headers={"X-CSRF-Token": token})
                if subscribers==-10 or basicinfo.json().get("numSubscribers")<subscribers:
                    subscribers=basicinfo.json().get("numSubscribers")
                if basicinfo.json().get("numSubscribers")>subscribers:
                    self.activatemotor=self.activatemotor+basicinfo.json().get("numSubscribers")-subscribers
                    subscribers=basicinfo.json().get("numSubscribers")
            except:
                self.displaylabel.config(text="Unexpected Error in New Subscriber Tester",bg='indian red')
                self.noErrors = 1

    def confettiBotTester(self,unused,unused2):
        try:
            class configfile():
                BEAM_ADDR = 'https://beam.pro'

                # Username of the account.
                USERNAME = 'ConfettiBot'

                # Password of the account.
                PASSWORD = 'confetti123'

                # The id of the channel you want to connect to.
                CHANNEL = self.login_response.json().get("channel").get("id")

            def on_message(a):
                if str(a.get('message'))!="None":
                    self.chats=self.chats+1
                    if self.confettibotchatfrequency.get()*self.chats>=int(self.line[35])+2: #It actually only does 2 less than the value
                        self.chats=0
                        self.sendchat.message(self.confettibotchattext.get('1.0', 'end-1c'))
                    if self.confettibotcommand.get() == a.get('message').get('message')[0].get('text') and 'ConfettiBot' not in a.get('user_name') and self.confettibot.get()==1:
                        if 'Subscriber' in a.get('user_roles') or a.get('user_name')=="Iwonderifthereisamaxcharacterlim":
                            subscriberpoints = open("subscriberpoints.txt", 'r')
                            subscriberpointslist = subscriberpoints.readlines()
                            for index, subscribers in enumerate(subscriberpointslist):
                                subscriberpointslist[index] = subscribers.strip('\n')
                            subscriberpoints.close()
                            try:
                                indexnumber=subscriberpointslist.index(a.get('user_name'))
                            except:
                                subscriberpointslist.append(a.get('user_name'))
                                subscriberpointslist.append('1')
                                self.activatemotor=self.activatemotor+1
                                if not str(self.line[33][0:len(self.line[33]) - 1]):
                                    pass
                                else:
                                    if self.line[33][0:len(self.line[33]) - 1].find("@") != -1:
                                        if self.line[33][0:len(self.line[33]) - 1].find("@")==len(self.line[33][0:len(self.line[33]) - 1])-1:
                                            self.sendchat.message(self.line[33][0:len(self.line[33]) - 1]+a.get('user_name'))
                                        else:
                                            self.sendchat.message(
                                                self.line[33][:self.line[33][0:len(self.line[33]) - 1].find("@") + 1] + a.get(
                                                    'user_name') + self.line[33][
                                                                   self.line[33][0:len(self.line[33]) - 1].find("@") + 1:len(
                                                                       self.line[33]) - 1])
                                    else:
                                        self.sendchat.message(self.line[33][0:len(self.line[33])])
                            else:
                                if int(subscriberpointslist[indexnumber+1])<int(self.timespermonth.get()):
                                    subscriberpointslist[indexnumber + 1]=str(int(subscriberpointslist[indexnumber+1])+1)
                                    self.activatemotor=self.activatemotor+1
                                else:
                                    if not str(self.line[31][0:len(self.line[31]) - 1]):
                                        pass
                                    else:
                                        if self.line[31][0:len(self.line[31]) - 1].find("@") != -1:
                                            if self.line[31][0:len(self.line[31]) - 1].find("@") == len(
                                                    self.line[31][0:len(self.line[31]) - 1]) - 1:
                                                self.sendchat.message(
                                                    self.line[31][0:len(self.line[31]) - 1] + a.get('user_name'))
                                            else:
                                                self.sendchat.message(
                                                    self.line[31][
                                                    :self.line[31][0:len(self.line[31]) - 1].find("@") + 1] + a.get(
                                                        'user_name') + self.line[31][
                                                                       self.line[31][0:len(self.line[31]) - 1].find(
                                                                           "@") + 1:len(
                                                                           self.line[31]) - 1])
                                        else:
                                            self.sendchat.message(self.line[31][0:len(self.line[31])])
                            for index, subscribers in enumerate(subscriberpointslist):
                                subscriberpointslist[index] = subscriberpointslist[index]+"\n"
                            updatedsubscriberpoints = open("subscriberpoints.txt", 'w')
                            for info in subscriberpointslist:
                                updatedsubscriberpoints.write(info)
                            updatedsubscriberpoints.close()
                        else:
                            self.sendchat.message(self.confettibotchattext.get('1.0', 'end-1c'))
            if self.startvariable==1:
                self.sendchat = create(configfile)
                self.sendchat.authenticate(configfile.CHANNEL)
                self.sendchat.message("ConfettiBot Activated")
                self.sendchat.on("message", on_message)
            IOLoop.instance().start()

        except:
            self.displaylabel.config(text="Unexpected Error in Confetti Bot Tester",bg='indian red')
            self.noErrors = 1

    def turnon(self):
        try:
            if self.startvariable==1:
                #sleep(1)
                pass
            self.sendchat.message("ConfettiBot Activated")
        except:
            pass

    def activateMotorTester(self,time,unused):
        try:
            portName = [port.device for port in list_ports.comports()]
            self.ser = serial.Serial(portName[0], 9600, timeout=1)
        except:
            self.displaylabel.config(text="Couldn't find confetti launcher",bg='indian red')
            self.noErrors = 1
        else:
            string1 = "AFFF0101DF"
            string2 = "AFFF0202DF"
            turnon = codecs.decode(string1, 'hex_codec')
            turnoff = codecs.decode(string2, 'hex_codec')
            while self.noErrors==0:
                try:
                    if self.activatemotor>0 and int(self.confettiactivatedentryvariable.get())>0:
                        self.ser.write(turnon)
                        sleep(getdouble(self.line[37]))
                        self.ser.write(turnoff)
                        self.activatemotor=self.activatemotor-1
                        self.confettiactivatedentryvariable.set(str(int(self.confettiactivatedentryvariable.get())-1))
                except:
                    self.displaylabel.config(text="Unexpected Error in Activate Motor",bg='indian red')
                    self.noErrors = 1
                if int(self.confettiactivatedentryvariable.get())==0:
                    try:
                        self.sendchat.message("ConfettiBot temporarily powering down...")
                    except:
                        pass
                    self.stop()
            self.ser.close()

    def tighten(self):
        string1 = "AFFF0101DF"
        string2 = "AFFF0202DF"
        turnon = codecs.decode(string1, 'hex_codec')
        turnoff = codecs.decode(string2, 'hex_codec')
        self.ser.write(turnon)
        sleep(.5)
        self.ser.write(turnoff)

    def activatemotorfunction(self):
        self.activatemotor=self.activatemotor+1

    def resetsubpoints(self):
        reset=open("subscriberpoints.txt",'w')
        reset.write("")
        reset.close()

    def stop(self):
        self.noErrors=1
        self.activatemotor = 0
        self.startvariable=0
        try:
            self.sendchat.message("ConfettiBot temporarily powering down...")
            IOLoop.instance().stop()
            self.session.close()
        except:
            pass
        self.displaylabel.config(text="", bg='gray95')
        self.goalreachedcb.config(state=NORMAL)
        self.donationcb.config(state=NORMAL)
        self.donationamountenty.config(state=NORMAL)
        self.percentreachedcb.config(state=NORMAL)
        self.percentreachedamountentry.config(state=NORMAL)
        self.percentinfo.config(state=NORMAL)
        self.APILabel.config(state=NORMAL)
        self.APIkeyentry.config(state=NORMAL)
        self.newsubscribercb.config(state=NORMAL)
        self.busernamelabel.config(state=NORMAL)
        self.busernameentry.config(state=NORMAL)
        self.bpasswordlabel.config(state=NORMAL)
        self.bpasswordentry.config(state=NORMAL)
        self.confettibotcb.config(state=NORMAL)
        self.confettibotcommandentry.config(state=NORMAL)
        self.cbcommandinfo.config(state=NORMAL)
        self.timespermonthentry.config(state=NORMAL)
        self.morecommandinfo.config(state=NORMAL)
        self.nonsubscriberslabel.config(state=NORMAL)
        self.confettibotchattext.config(state=NORMAL, bg='white', fg='black')
        self.confettibotchatfrequencycb.config(state=NORMAL)
        self.cbchatfrequencyinfo.config(state=NORMAL)
        self.button.config(command=self.start, text="Start")
        self.calibrate.config(state=DISABLED)
        self.testconfetti.config(state=DISABLED)


root = Tk()

root.title('Confetti Launcher')

app = ConfettiDisplay(root)

root.mainloop()