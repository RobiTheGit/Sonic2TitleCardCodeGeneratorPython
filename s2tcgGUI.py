import tkinter as tk
from tkinter import *
from tkinter import messagebox
import re
import sys
'''
Letter Format
dc.w $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER
example: dc.w $0005, $85DE, $82EF, $FFD0; FIRST LETTER INDEX WHEN NOT (Z, O, N, E)
'''
"""
Generation Code
"""
global text
text = ''
global debug
debug = False
def gen(): 
    global text
    global char
    global afterI
    global afterM
    global debug
    pos_br = 65520 #position before setting position to $0
    pos_inc = 16 #$10, after M or W, 24/$18, after I, 8/$8
    cur_pos = 65428 #starts with the starting position
    after0 = False
    letter = 0
    current = 1500
    twopcurrent = 749
    increment = 2
    twopinc = 2
    textt = text
    btext = re.sub(r"[^a-zA-Z ]", "", textt)
    ntext = btext.replace(" ", "")
    hexi = hex(len(ntext)).upper()
    if len(btext) >= 10:
        cur_pos = 65428
    elif len(btext) <= 9 and len(btext) > 5:
        cur_pos = 0
        after0 = True            
    else:
        cur_pos = 28 
        after0 = True        
    char = ''
    code = []
    charlist = []
    charlistcode = []
    afterI = False 
    afterM = False
    for char in btext:
        code.append(char.lower())
        
    if len(code) == 0:
         tk.messagebox.showerror(title='No Title Card To Make!', message='You have no title card to generate!', options=None)
    else:
        proper = hexi.replace("0X", "TC_EHZ    dc.w $")
        output.insert(END,f';In Obj34_MapUnc_147BA Put\n')
        output.insert(END,f'{proper} ; EHZ can be changed to the word it is, EHZ\'s is word_147E8 \n')
    pos = -(len(code))
    if len(char) <= 15:
        for char in code:
            if letter >= 1:
                increment = 4 #the first letter is 2 and not 4
            if afterI == True:
                increment = 2 #this is only changed on i from $8 to $4
                twopinc = 1 #same as above
                pos_inc = 4 #incrememnt the position less
                if afterIcount == 0:
                    increment = 4  #restore the default values
                    twopinc = 2 
                    pos_inc = 16 
                else:
                    afterIcount -= 1  
            if afterM == True:
                pos_inc = 24                    
                if afterMcount == 0:
                    pos_inc = 16
                else:
                    afterMcount -= 1 
            cur_pos += pos_inc #increment position by the position incrementer, there is a reason this is defined after the afterM and afterI stuff
            if cur_pos <= pos_br:
                char = char.lower()
                xpos_b = hex(cur_pos)
                if after0 == False:
                    XPOS = xpos_b.replace("0x", "").upper() #this is for dissam compatibility
                else:
                    XPOS = xpos_b.replace("0x", "00").upper() #this is also for dissam compatibility
            elif cur_pos >= pos_br:
                cur_pos = 0
                XPOS = '0000' #this is for dissam compatibility but also that is how the values work 
                after0 = True 
            else:
                cur_pos = 0
                XPOS = '0000'
                after0 = True                              
            if char == 'm' or char == 'w':
                width = '09'
            elif char == 'i':
                width = '01'
            else:
                width = '05'
            if char in charlist:
                x = charlist.index(char) 
                output.insert(END,f'{charlistcode[x]},${XPOS} ; {char.upper()} \n')
                if char == 'i':
                   afterI = True 
                   afterIcount = 1
                if char == 'm' or char == 'w':
                   afterM = True 
                   afterMcount = 1
            else:
                if char != 'z' and char != 'o' and char != 'n' and char != 'e' and char != ' ' and char.isalpha():  
                    letter += 1 
                    result = int(current)+int(increment)
                    result2 = hex(result)
                    INDEX = result2.replace("0x", "").upper()
                    twopresult = int(twopcurrent)+int(twopinc)
                    twopres2 = hex(twopresult) 
                    INDEX2P = twopres2.replace("0x", "").upper()
                    indexcode = (f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')
                    indexcode2 = (f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P} ')
                    charlistcode.append(indexcode2)    
                    output.insert(END,f'{indexcode} \n')
                    charlist.append(char)
                    current = result
                    twopcurrent = twopresult
                    if char == 'i':
                       afterI = True 
                       afterIcount = 2
                    if char == 'm' or char == 'w':
                       afterM = True 
                       afterMcount = 2                
                elif char == 'z':
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                elif char == 'o':
                    INDEX = '588'
                    INDEX2P = '2C4'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )            
                elif char == 'n':
                    INDEX = '584'
                    INDEX2P = '2C2'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )                         
                elif char == 'e':
                    INDEX = '580'
                    INDEX2P = '2C0'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )               
                elif char == ' ':
                    cur_pos += 2                   
                    output.insert(END,'\n')
                else:
                     pass
        if len(code) == 0:
            pass
        else:        
            output.insert(END,f'\n ;Fix spacing manually!')
            if len(ntext) > 16:
                output.insert(END,'\n;You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
                tk.messagebox.showerror(title='Error!', message='You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work', options=None) 
            if len(charlistcode) > 8:     
                output.insert(END,'\n;You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
                tk.messagebox.showerror(title='Error!', message='You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work', options=None)
            if debug == True:
                output.insert(END, f'\n;Indexes: {charlist} {len(charlist)}\n;Code for above indexes:{charlistcode}\n;\tBut you can\'t stick n move')
"""
Tkinter Code
"""
def run():
    global text
    global output
    global debug
    output.configure(state='normal')
    output.delete(1.0, END)
    gen()
    output.configure(state='disabled')
class App(tk.Frame):
    global f
    def __init__(self, master):
        global text
        global output
        global debug
        global var1
        var1 = tk.IntVar()
        super().__init__(master)
        self.pack()
        leftframe = Frame(root, relief="raised")
        leftframe.pack(side = LEFT, fill=BOTH, anchor = NE, padx = 5)
        topframe = Frame(root)
        topframe.pack(side = TOP, fill=BOTH)        
        bottomframe = Frame(root)
        bottomframe.pack(side = TOP, fill=BOTH, pady = 5)
        photo = PhotoImage(file ="icon.png")
        root.iconphoto(False, photo)        
        Title = tk.Label(topframe,text="SONIC 2 TITLECARD CODE GENERATOR PYTHON \nBY: RobiWanKenobi", font = ('gaslight', 18))
        Title.pack(side = TOP, fill=BOTH)
        inlbl = tk.Label(leftframe, text='Input Title Card Name Here')
        inlbl.pack(side = TOP, anchor = NE)
        self.entrythingy = tk.Entry(leftframe)
        self.contents = tk.StringVar()
        self.contents.set("")
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.bind('<Key-Return>', self.enterrun)
        self.entrythingy.pack(side = TOP, anchor = NE,)
        B = tk.Button(leftframe, 
        text = 'Generate Code', 
        command = self.getstr, 
        font = ('gaslight', 18),
        height=3, 
        width=8)
        B.pack(side = TOP, anchor = NE)
        B2 = tk.Button(leftframe,
        text = 'Titlecard Letters', 
        command = self.open_popup, 
        font = ('gaslight', 18),
        height=3, 
        width=8)
        B2.pack(side = TOP, anchor = E)
        B3 = tk.Button(leftframe,
        text = 'About S2tcg.py',
        command = self.info,
        font = ('gaslight', 18),
        height=3, 
        width=8)
        B3.pack(side = TOP, anchor = SE)
        exitbutton = tk.Button(leftframe,
        text = 'EXIT',
        command = self.exit, 
        font = ('gaslight', 18),
        height=3,
        width=8)
        exitbutton.pack(side = TOP, anchor = SE)        
        c1 = tk.Checkbutton(topframe, text='See Debug Info',variable=var1, onvalue=1, offvalue=0, command=self.debugset)
        c1.pack(side = BOTTOM)
        output = tk.Text(bottomframe, state='disabled')
        output.pack( expand = 1, fill = BOTH)
    def enterrun(self, event):
        self.getstr()
    def getstr(self):
        global text
        text = self.contents.get()
        run()
    def debugset(self):
        global var1
        global debug
        if var1.get() == 0:
            debug = False
        elif var1.get() == 1:
            debug = True
        else:
            debug = False
    def open_popup(self):
        global text
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()
        top= Toplevel()
        top.geometry("550x200")
        top.resizable(False,False)
        top.title("GITHUB Off_TitleCardLetters")
        Label(top, text= f'In Off_TitleCardLetters, for the zone title card you want to modify, where it says \ntitleLetters    "EMERALD HILL" or whatever zone you are replacing, \n you type in the zone\'s name, currently your titleLetters would have\n').pack()
        pep = Text(top, state = 'normal')
        pep.pack()
        pep.delete(1.0, END)
        pep.insert(END, f'titleLetters	"{titleletters}"',)
        pep.configure(state = 'disabled')
    def info(self):
        tk.messagebox.showinfo(title='About', message='Sonic 2 Titlecard Code Generator in Python, created by RobiWanKenobi in \nPython 3.10 . \nIf you want to support htis project, I have no way to currently :( .', options=None)
    def exit(self):
        sys.exit(0)        
# create the application
title = "Sonic 2 Titlecard Code Generator"
root = tk.Tk(className="S2TCG")
root.geometry("850x450")
root.resizable(True,True)
myapp = App(root)
myapp.master.title(title)
myapp.mainloop()
