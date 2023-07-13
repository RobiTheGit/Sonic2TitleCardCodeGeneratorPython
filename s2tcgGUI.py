#!/usr/bin/python3 
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import re
import sys
import customtkinter
THEME = "DARK"
customtkinter.set_appearance_mode(THEME)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
'''
Letter Format
	dc.w        $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER
example: 
	dc.w        $0005, $85DE, $82EF, $FFD0; FIRST LETTER INDEX WHEN NOT (Z, O, N, E)
'''

"""
Generation Code
"""

global text
text = ''
global debug
debug = False

def GenerateMappings(): 
    global text
    global char
    global afterI
    global afterM
    global debug
    NegativeToPositive_Position = 65535 #position before setting position to $0
    SpaceBetweenLetter = 16 #$10, after M or W, 24/$18, after I, 8/$8
    Current_XPOS = 65428 #starts with the starting position
    after0 = False
    letter = 0
    Current_Index = 1500
    Current_2PIndex = 749
    Index_Increment = 2
    Index_Increment_2P = 2
    btext = re.sub(r"[^a-zA-Z ]", "", text)
    ntext = btext.replace(" ", "")
    hexi = hex(len(ntext)).upper()
    #start position setting code
    if len(btext) >= 10: 
        Current_XPOS = 65428
    elif len(btext) <= 9 and len(btext) > 6:
        Current_XPOS = 65446
    elif len(btext) <= 6 and len(btext) > 4:
        Current_XPOS = 0
        after0 = True
    else:
        Current_XPOS = 64 
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
         tk.messagebox.showerror(
         title='No Titlecard To Make!',
         message='You have no titlecard to generate!',
         options=None
         )
    else:
        proper = hexi.replace("0X", f"TC_{dispzone}:    dc.w $")
        output.insert(END,f';In Obj34_MapUnc_147BA Put\n')
        output.insert(END,f'{proper} \n')
    pos = -(len(code))
    if len(char) <= 15:
        for char in code:
            if letter >= 1:
                Index_Increment = 4 #the first letter is 2 and not 4
            if afterI == True:
                SpaceBetweenLetter = 4 #incrememnt the position less
                if afterIcount == 0:
                    Index_Increment = 4  #restore the default values
                    Index_Increment_2P = 2 
                    SpaceBetweenLetter = 8 
                else:
                    if afterIposcount == 0:
                        SpaceBetweenLetter = 16
                    else:
                        Current_XPOS += 8
                        afterIposcount = 0
            if afterM == True:
                SpaceBetweenLetter = 24   
                Index_Increment_2P = 3 
                Index_Increment = 6  #restore the default values
                if afterMcount == 0:
                    Index_Increment = 4  #restore the default values
                    Index_Increment_2P = 2 
                    SpaceBetweenLetter = 16
                    afterM = False
                else:
                    afterMcount -= 1 
                    if afterMposcount == 0:
                        Index_Increment = 4  #restore the default values
                        Index_Increment_2P = 2 
                        SpaceBetweenLetter = 16
                        afterM = False
                    else:
                        afterMposcount = 0
            Current_XPOS += SpaceBetweenLetter #Index_Increment position by the position Index_Incrementer, there is a reason this is defined after the afterM and afterI stuff
            if Current_XPOS <= NegativeToPositive_Position:
                char = char.lower()
                xpos_b = hex(Current_XPOS)
                if after0 == False:
                    XPOS = xpos_b.replace("0x", "").upper()
                else:
                    if Current_XPOS >= 16:
                        XPOS = xpos_b.replace("0x", "00").upper()
                    elif Current_XPOS <= 16:
                        XPOS =  xpos_b.replace("0x", "000").upper()
                    else:    
                        XPOS =  xpos_b.replace("0x", "000").upper()
            elif Current_XPOS >= NegativeToPositive_Position:
                Current_XPOS -= 65536
                xpos_b = hex(abs(Current_XPOS))
                if Current_XPOS >= 16:
                    XPOS = xpos_b.replace("0x", "00").upper()
                elif Current_XPOS <= 16:
                    XPOS =  xpos_b.replace("0x", "000").upper()
                else:    
                    XPOS =  xpos_b.replace("0x", "000").upper()
                after0 = True
            else:
                after0 = True
                Current_XPOS -= 65536
                xpos_b = hex(abs(Current_XPOS))
                if Current_XPOS >= 16:
                    XPOS = xpos_b.replace("0x", "00").upper()
                if Current_XPOS <= 16:
                    XPOS =  xpos_b.replace("0x", "000").upper()
                else:    
                    XPOS =  xpos_b.replace("0x", "000").upper()
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
                   afterIcount = 0
                if char == 'm' or char == 'w':
                   afterM = True 
                   afterMcount = 1
            else:
                if char != 'z' and char != 'o' and char != 'n' and char != 'e' and char != ' ' and char.isalpha():  
                    letter += 1 
                    result = int(Current_Index)+int(Index_Increment)
                    if afterI == True:
                        result -= 2
                    result2 = hex(result)
                    INDEX = result2.replace("0x", "").upper()
                    twopresult = int(Current_2PIndex)+int(Index_Increment_2P)
                    twopres2 = hex(twopresult) 
                    INDEX2P = twopres2.replace("0x", "").upper()
                    indexcode = (f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')
                    indexcode2 = (f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P} ')
                    if afterI == True:
                        result += 2
                    charlistcode.append(indexcode2)
                    output.insert(END,f'{indexcode} \n')
                    charlist.append(char)
                    Current_Index = result
                    Current_2PIndex = twopresult
                    if char == 'i':
                       afterI = True 
                       afterIcount = 0
                       afterIposcount = 1
                    if char == 'm' or char == 'w':
                       afterM = True 
                       afterMcount = 1 
                       afterMposcount = 1
                elif char == 'z':
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1
                elif char == 'o':
                    INDEX = '588'
                    INDEX2P = '2C4'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1 
                elif char == 'n':
                    INDEX = '584'
                    INDEX2P = '2C2'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1 
                elif char == 'e':
                    INDEX = '580'
                    INDEX2P = '2C0'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1 
                elif char == ' ':
                    Current_XPOS += 2
                    output.insert(END,'\n')

                else:
                     pass
        if len(code) == 0:
            pass
        else:
            output.insert(END, f'\n; Open "Mapping Locations" for locations of titlecards\n; Open Mappings.txt for a replacement for the original mappings')
            if len(ntext) > 16:
                output.insert(END,'\n;You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
                tk.messagebox.showerror(title='Error!', message='You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work', options=None) 
            if len(charlistcode) > 8:     
                output.insert(END,'\n;You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
                tk.messagebox.showerror(title='Error!', message='You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work', options=None)
            if after0 == True and Current_XPOS >= 112:
                tk.messagebox.showerror(title='Error!', message='Position Out Of bounds', options=None)
            if debug == True:
                output.insert(END, f'\n;Indexes: {charlist} {len(charlist)}\n;Code for above indexes:{charlistcode}\n;\tBut you can\'t stick n move')
"""
Tkinter Code
"""
def GenerateTitlecardFromText():
    global text
    global output
    global debug
    output.configure(state='normal')
    output.delete(1.0, END)
    GenerateMappings()
    output.configure(state='disabled')

class App(tk.Frame):
    global f
    def __init__(self, master):
        global text
        global output
        global debug
        global dbgvar
        global themevar
        global zone
        global ZoneMenu
        dbgvar = tk.IntVar()
        zone = tk.IntVar()
        themevar = tk.IntVar()
        super().__init__(master)
        self.pack()
#	Initilize left frame
        leftframe = customtkinter.CTkFrame(
        root
        )        
        leftframe.pack(side = LEFT, fill=BOTH, anchor = NE, padx = 5)
 #	Initilize top frame
        topframe = customtkinter.CTkFrame(
        root 
        )
        topframe.pack(side = TOP, fill=BOTH)
#	Initilize bottom frame
        bottomframe = customtkinter.CTkFrame(
        root 
        )
        bottomframe.pack(side = TOP, fill=BOTH, pady = 5)
#	Load icon for app
        photo = PhotoImage(file ="icon.png")
        root.iconphoto(False, photo)
#	Draw title
        Title = customtkinter.CTkLabel(
        topframe,
        text="SONIC 2 TITLECARD CODE GENERATOR PYTHON \nBy: RobiWanKenobi", 
        font = ('gaslight', 25)
        )        
        Title.pack(side = TOP, fill=BOTH)
#	Add label to tell peopel where inout goes
        inlbl = customtkinter.CTkLabel(
        leftframe, 
        text='Input Title Card Name Here'
        )
        inlbl.pack(side = TOP, anchor = NE)
#	Add level name input
        self.LevelName = customtkinter.CTkEntry(leftframe, placeholder_text="type level name")
        self.contents = tk.StringVar()
        self.contents.set("")
        self.LevelName["textvariable"] = self.contents 
        self.LevelName.bind('<Key-Return>', self.RunFromEnterKey)
        self.LevelName.pack(side = TOP, anchor = NE,)
#	Add button to generate the titlecard code
        Generate = customtkinter.CTkButton(leftframe, 
        text = '  Generate Code', 
        command = self.RunGeneration, 
        font = ('gaslight', 30),
        height=3, 
        width=9
        )
        Generate.pack(side = TOP, anchor = E)
#	Add button to open the titlecard letters popup
        TitlecardLetters = customtkinter.CTkButton(leftframe,
        text = 'Titlecard Letters', 
        command = self.TitlecardLetters_Popup, 
        font = ('gaslight', 30),
        height=3, 
        width=8
        )
        TitlecardLetters.pack(side = TOP, anchor = E)
#	Add button to open the about screen
        About = customtkinter.CTkButton(leftframe,
        text = '  About S2tcg.py',
        command = self.info,
        font = ('gaslight', 30),
        height=3, 
        width=8
        )
        About.pack(side = TOP, anchor = SE)
#	Add button to export the titlecard code
        Export = customtkinter.CTkButton(leftframe,
        text = 'Export Titlecard',
        command = self.ExportTitlecard,
        font = ('gaslight', 30),
        height=3, 
        width=8
        )
        Export.pack(side = TOP, anchor = SE)
#	Add button to open the mapping locations for titlecards popup
        MappingsLocations = customtkinter.CTkButton(leftframe,
        text = 'Mapping Locations',
        command = self.MappingLocations_Popup,
        font = ('gaslight', 30),
        height=3, 
        width=8
        )
        MappingsLocations.pack(side = TOP, anchor = SE)
#	Add the zone selector
        ZoneMenu = customtkinter.CTkOptionMenu(
        leftframe,
        variable = zone,
        values=[
        "EHZ",
        "CPZ",
        "ARZ",
        "CNZ",
        "HTZ",
        "MCZ",
        "OOZ",
        "MTZ",
        "SCZ",
        "WFZ",
        "DEZ",
        "HPZ"
        ]
        )
        ZoneMenu.pack(side = BOTTOM) 
        ZoneMenu.set(ZoneMenu._values[0]) 
#	Add the button to exit the program
        exitbutton = customtkinter.CTkButton(
        leftframe,
        text = '     Exit     ',
        command = self.ExitProgram, 
        font = ('gaslight', 30),
        height=3,
        width=8
        )
        exitbutton.pack(side = TOP, anchor = SE)
#	Add the copy to clipboard button
        copybutton = customtkinter.CTkButton(
        topframe,
        text = 'Copy To Clipboard',
        command = self.CopyToClipboard, 
        font = ('gaslight', 30),
        height=3,
        width=8
        )
        copybutton.pack(side = BOTTOM)
#	Add the debug flag checkbox
        DebugCheck = customtkinter.CTkCheckBox(
        topframe,
        text='See Debug Info',
        variable=dbgvar,
        onvalue=1,
        offvalue=0, 
        command=self.SetDebugFlag
        )
        DebugCheck.pack(side = BOTTOM)
#	Add the Light/Dark mode checkbox
        ThemeCheck = customtkinter.CTkCheckBox(
        topframe,
        text='Light Mode',
        variable=themevar,
        onvalue=1,
        offvalue=0, 
        command=self.ChangeAppTheme
        )
        ThemeCheck.pack(side = BOTTOM)
#	Add the output box
        output = customtkinter.CTkTextbox(
        bottomframe,
        state='disabled',
        height = 400,
        font = ("courier", 16)
        )
        output.pack(fill = BOTH)

#	Code To Export Titlecard Into a File

    def ExportTitlecard(self):
        global text
        if text == '':
            pass
        else:
            f = open(f'{text.upper()}.txt', 'a')
            titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()
            f.write(output.get(1.0, END))
            f.write(f'titleLetters	"{titleletters}"')
            f.close()

#	Code to run the generator

    def RunFromEnterKey(self, event):
        self.RunGeneration()

    def RunGeneration(self):
        global text
        global dispzone
        text = self.LevelName.get()
        dispzone = ZoneMenu.get()
        GenerateTitlecardFromText()

#	Code to set the debug flag

    def SetDebugFlag(self):
        global dbgvar
        global debug
        if dbgvar.get() == 0:
            debug = False
        elif dbgvar.get() == 1:
            debug = True
        else:
            debug = False

#	Code to change themes

    def ChangeAppTheme(self):
        global themevar
        global debug
        if themevar.get() == 0:
            THEME = "DARK"
        elif themevar.get() == 1:
            THEME = "LIGHT"
        else:
            THEME = "DARK"
        customtkinter.set_appearance_mode(THEME)  # Modes: system (default), light, dark

#	Code to copy output to clipboard

    def CopyToClipboard(self):
        root.clipboard_clear()
        root.clipboard_append(output.get(1.0, END))

#	Code to open the titlecard letters popup

    def TitlecardLetters_Popup(self):
        global text
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()
        top= customtkinter.CTkToplevel()
        top.geometry("600x400")
        top.resizable(False,False)
        top.title("Off_TitleCardLetters")
        customtkinter.CTkLabel(
        top,
        text= f'In Off_TitleCardLetters, for the zone title card you want to modify, where it says \ntitleLetters    "EMERALD HILL" or whatever zone you are replacing, \n you type in the zone\'s name, currently your titleLetters would have\n'
        ).pack()
        pep = customtkinter.CTkTextbox(top,
        state = 'normal',
        font = ("courier", 18)
        )
        pep.pack(fill = BOTH)
        customtkinter.CTkLabel(
        top,
        text= f'If you are using the 2007 Xenowhirl disasm, read Xenowhirl_Setup.txt\nUse the letter macros, and skip Z, O, N, & E\n'
        ).pack()
        pep.delete(1.0, END)
        pep.insert(END, f'titleLetters	"{titleletters}"',)
        pep.configure(state = 'disabled')
        customtkinter.CTkLabel(
        top,
        text= f'The order for title card letters is the same as the order for the mappings code'
        ).pack()

#	Code to open the titlecard mapping locations popup

    def MappingLocations_Popup(self):
        global text
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()
        top= customtkinter.CTkToplevel()
        top.geometry("550x250")
        top.resizable(False,False)
        top.title("Titlecard Mapping Label Translation")
        pep2 = customtkinter.CTkTextbox(top,
        state = 'normal',
        font = ("courier", 18)
        )
        LocFile = open("Locations.txt", "r")
        pep2.pack(fill = BOTH)
        pep2.delete(1.0, END)
        pep2.insert(END, LocFile.read(),)
        pep2.configure(state = 'disabled')


    def OpenAbout(self):
        tk.messagebox.showOpenAbout(
        title='About',
        message="Sonic 2 Titlecard Code Generator in Python aka. S2TCG.py, created by RobiWanKenobi in \nPython 3.10.", options=None
        )

    def ExitProgram(self):
        sys.exit(0)

# create the application
title = "Sonic 2 Titlecard Code Generator"
root = customtkinter.CTk(className="S2TCG")
root.geometry("900x500")
root.resizable(True,True)
myapp = App(root)
myapp.master.title(title)
myapp.mainloop()
