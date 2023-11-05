#!/usr/bin/python3 
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from re import sub
from sys import exit
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
global DebugFlag
DebugFlag = False

def GenerateMappings(): 
    global text
    global CharacterOfTitleCard
    global LetterIsAfterI
    global LetterIsAfterM
    global DebugFlag
    NegativeToPositive_Position = 65535 #position before setting position to $0
    SpaceBetweenLetter = 16 #$10, after M or W, 24/$18, after I, 8/$8
    Current_XPOS = 65428 #starts with the starting position
    PositionsIsAfter0 = False
    CurrentCharacter = 0
    Current_Index = 1500
    Current_2PIndex = 749
    Index_Increment = 2
    Index_Increment_2P = 2
    REGEX_STEP = sub(r"[^a-zA-Z ]", "", text)
    LENGTH_STEP = REGEX_STEP.replace(" ", "")
    hexi = hex(len(LENGTH_STEP)).upper()
#   start position setting position
    if len(REGEX_STEP) >= 10: 
        Current_XPOS = 65428
    elif len(REGEX_STEP) <= 9 and len(REGEX_STEP) > 6:
        Current_XPOS = 65446
    elif len(REGEX_STEP) <= 6 and len(REGEX_STEP) > 2:
        Current_XPOS = 0
        PositionsIsAfter0 = True
    else:
        Current_XPOS = 64 
        PositionsIsAfter0 = True
    CharacterOfTitleCard = ''
    AllOfTheCharacters = []
    CharactersList = []
    SavedIndexes = []
    LetterIsAfterI = False 
    LetterIsAfterM = False
    for CharacterOfTitleCard in REGEX_STEP:
        AllOfTheCharacters.append(CharacterOfTitleCard.lower())
        
    if len(AllOfTheCharacters) == 0:
         tk.messagebox.showerror(
         title='No Titlecard To Make!',
         message='You have no titlecard to generate!',
         options=None
         )
    else:
        proper = hexi.replace("0X", f"TC_{ZoneNameForLabel}:    dc.w $")
        TitlecardOutput.insert(END,f';In Obj34_MapUnc_147BA Put\n')
        TitlecardOutput.insert(END,f'{proper} \n')
    pos = -(len(AllOfTheCharacters))
#getting the indexes
   if len(CharacterOfTitleCard) <= 15:
        for CharacterOfTitleCard in AllOfTheCharacters:
            if CurrentCharacter >= 1:
                Index_Increment = 4 #the first letter is 2 and not 4
                if LetterIsAfterI == True:
                    SpaceBetweenLetter = 4 #incrememnt the position less
                    if LetterIsAfterIcount == 0:
                        if LetterIsAfterM == False:
                            Index_Increment = 4  #restore the default values
                            Index_Increment_2P = 2
                        SpaceBetweenLetter = 8 
                    else:
                        if LetterIsAfterIposcount == 0:
                            Index_Increment = 6  #restore the default values
                            Index_Increment_2P = 3 
                            SpaceBetweenLetter = 16
                        else:
                            Index_Increment = 6  #restore the default values
                            Index_Increment_2P = 3                   
                            Current_XPOS += 8
                            LetterIsAfterIposcount = 0

                if LetterIsAfterM == True:
                    SpaceBetweenLetter = 24 
                    if LetterIsAfterI == False: 
                        Index_Increment_2P = 3 
                        Index_Increment = 6  #restore the default values
                    else:
                        Index_Increment = 4  #restore the default values
                        Index_Increment_2P = 2                     
                    if LetterIsAfterMcount == 0:
                        if LetterIsAfterI == False:
                            LetterIsAfterMcount += 1
                        else:
                            Index_Increment = 4  #restore the default values
                            Index_Increment_2P = 2 
                        SpaceBetweenLetter = 16
                        LetterIsAfterM = False
                    else:
                        LetterIsAfterMcount -= 1 
                        if LetterIsAfterMposcount == 0:
                            SpaceBetweenLetter = 16
                            LetterIsAfterM = False
                        else:
                            LetterIsAfterMposcount = 0

                else:
                    Index_Increment = 4  #restore the default values
                    Index_Increment_2P = 2 
                    SpaceBetweenLetter = 16     
#position
            Current_XPOS += SpaceBetweenLetter #Index_Increment position by the position Index_Incrementer, there is a reason this is defined after the LetterIsAfterM and LetterIsAfterI stuff
            if Current_XPOS <= NegativeToPositive_Position:
                CharacterOfTitleCard = CharacterOfTitleCard.lower()
                PreFinal_XPOS = hex(Current_XPOS)
                if PositionsIsAfter0 == False:
                    XPOS = PreFinal_XPOS.replace("0x", "").upper()
                else:
                    if Current_XPOS >= 16:
                        XPOS = PreFinal_XPOS.replace("0x", "00").upper()
                    elif Current_XPOS <= 16:
                        XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                    else:    
                        XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
            elif Current_XPOS >= NegativeToPositive_Position:
                Current_XPOS -= 65536
                PreFinal_XPOS = hex(abs(Current_XPOS))
                if Current_XPOS >= 16:
                    XPOS = PreFinal_XPOS.replace("0x", "00").upper()
                elif Current_XPOS <= 16:
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                else:    
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                PositionsIsAfter0 = True
            else:
                PositionsIsAfter0 = True
                Current_XPOS -= 65536
                PreFinal_XPOS = hex(abs(Current_XPOS))
                if Current_XPOS >= 16:
                    XPOS = PreFinal_XPOS.replace("0x", "00").upper()
                if Current_XPOS <= 16:
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                else:    
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
#width                    
            if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                CharacterWidth = '09'
            elif CharacterOfTitleCard == 'i':
                CharacterWidth = '01'
            else:
                CharacterWidth = '05'
#making the lines of code
            if CharacterOfTitleCard in CharactersList:
                x = CharactersList.index(CharacterOfTitleCard) 
                TitlecardOutput.insert(END,f'{SavedIndexes[x]}, ${XPOS} ; {CharacterOfTitleCard.upper()} \n')
                if CharacterOfTitleCard == 'i':
                   LetterIsAfterI = True 
                   LetterIsAfterIcount = 3
                   LetterIsAfterIposcount = 1
                if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                   LetterIsAfterM = True 
                   LetterIsAfterMcount = 3
                   LetterIsAfterMposcount = 1
            else:
                if CharacterOfTitleCard != 'z' and CharacterOfTitleCard != 'o' and CharacterOfTitleCard != 'n' and CharacterOfTitleCard != 'e' and CharacterOfTitleCard != ' ' and CharacterOfTitleCard.isalpha():  
                    CurrentCharacter += 1 
                    result = int(Current_Index)+int(Index_Increment)
                    if LetterIsAfterI == True:
                        result -= 2
                    result2 = hex(result)
                    INDEX = result2.replace("0x", "").upper()
                    twopresult = int(Current_2PIndex)+int(Index_Increment_2P)
                    twopres2 = hex(twopresult) 
                    INDEX2P = twopres2.replace("0x", "").upper()
                    CodeToOutput = (f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}')
                    CodeForSavedIndexes = (f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}')
                    if LetterIsAfterI == True:
                        result += 2 
                        if CharacterOfTitleCard == "m":
                            result += 2  
                    SavedIndexes.append(CodeForSavedIndexes)
                    TitlecardOutput.insert(END,f'{CodeToOutput} \n')
                    CharactersList.append(CharacterOfTitleCard)
                    Current_Index = result
                    Current_2PIndex = twopresult
                    if CharacterOfTitleCard == 'i':
                       LetterIsAfterI = True 
                       LetterIsAfterIcount = 3
                       LetterIsAfterIposcount = 1
                    if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                       LetterIsAfterM = True 
                       LetterIsAfterMcount = 3 
                       LetterIsAfterMposcount = 1
                elif CharacterOfTitleCard == 'z':
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    TitlecardOutput.insert(END,f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()} \n' ) 
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1
                elif CharacterOfTitleCard == 'o':
                    INDEX = '588'
                    INDEX2P = '2C4'
                    TitlecardOutput.insert(END,f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()} \n' ) 
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1 
                elif CharacterOfTitleCard == 'n':
                    INDEX = '584'
                    INDEX2P = '2C2'
                    TitlecardOutput.insert(END,f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()} \n' )
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1 
                elif CharacterOfTitleCard == 'e':
                    INDEX = '580'
                    INDEX2P = '2C0'
                    TitlecardOutput.insert(END,f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()} \n' )
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1 
                elif CharacterOfTitleCard == ' ':
                    Current_XPOS += 2
                    TitlecardOutput.insert(END,'\n')

                else:
                     pass
        if len(AllOfTheCharacters) == 0:
            pass
        else:
            TitlecardOutput.insert(END, f'\n; Open "Mapping Locations" for locations of titlecards\n; Open Mappings.txt for a replacement for the original mappings')
            if len(LENGTH_STEP) > 16:
                TitlecardOutput.insert(END,'\n;You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
                tk.messagebox.showerror(title='Error!', message='You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work', options=None) 
            if len(SavedIndexes) > 8:     
                TitlecardOutput.insert(END,'\n;You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
                tk.messagebox.showerror(title='Error!', message='You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work', options=None)
            if PositionsIsAfter0 == True and Current_XPOS >= 112:
                tk.messagebox.showerror(title='Error!', message='Position Out Of bounds', options=None)
            if DebugFlag == True:
                TitlecardOutput.insert(END, f'\n;Indexes: {CharactersList} {len(CharactersList)}\n;Code for above indexes:{SavedIndexes}\n;\tBut you can\'t stick n move')
"""
Tkinter Code
"""
def GenerateTitlecardFromText():
    global text
    global TitlecardOutput
    global DebugFlag
    TitlecardOutput.configure(state='normal')
    TitlecardOutput.delete(1.0, END)
    GenerateMappings()
    TitlecardOutput.configure(state='disabled')

class App(tk.Frame):
    global f
    def __init__(self, master):
        global text
        global TitlecardOutput
        global DebugFlag
        global DebugEnabledFlag
        global SwitchThemeFlag
        global zone
        global ZoneMenu
        DebugEnabledFlag = tk.IntVar()
        zone = tk.IntVar()
        SwitchThemeFlag = tk.IntVar()
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
        variable=DebugEnabledFlag,
        onvalue=1,
        offvalue=0, 
        command=self.SetDebugFlag
        )
        DebugCheck.pack(side = BOTTOM)
#	Add the Light/Dark mode checkbox
        ThemeCheck = customtkinter.CTkCheckBox(
        topframe,
        text='Light Mode',
        variable=SwitchThemeFlag,
        onvalue=1,
        offvalue=0, 
        command=self.ChangeAppTheme
        )
        ThemeCheck.pack(side = BOTTOM)
#	Add the TitlecardOutput box
        TitlecardOutput = customtkinter.CTkTextbox(
        bottomframe,
        state='disabled',
        height = 400,
        font = ("courier", 16)
        )
        TitlecardOutput.pack(fill = BOTH)

#	Code To Export Titlecard Into a File

    def ExportTitlecard(self):
        global text
        if text == '':
            pass
        else:
            f = open(f'{text.upper()}.txt', 'a')
            TitlecardLettersToLoad = sub(r"[^a-zA-Z,' ']", "", text).upper()
            f.write(TitlecardOutput.get(1.0, END))
            f.write(f'titleLetters	"{TitlecardLettersToLoad}"')
            f.close()

#	Code to run the generator

    def RunFromEnterKey(self, event):
        self.RunGeneration()

    def RunGeneration(self):
        global text
        global ZoneNameForLabel
        text = self.LevelName.get()
        ZoneNameForLabel = ZoneMenu.get()
        GenerateTitlecardFromText()

#	Code to set the debug flag

    def SetDebugFlag(self):
        global DebugEnabledFlag
        global DebugFlag
        if DebugEnabledFlag.get() == 0:
            DebugFlag = False
        elif DebugEnabledFlag.get() == 1:
            DebugFlag = True
        else:
            DebugFlag = False

#	Code to change themes

    def ChangeAppTheme(self):
        global SwitchThemeFlag
        global DebugFlag
        if SwitchThemeFlag.get() == 0:
            THEME = "DARK"
        elif SwitchThemeFlag.get() == 1:
            THEME = "LIGHT"
        else:
            THEME = "DARK"
        customtkinter.set_appearance_mode(THEME)  # Modes: system (default), light, dark

#	Code to copy TitlecardOutput to clipboard

    def CopyToClipboard(self):
        root.clipboard_clear()
        root.clipboard_append(TitlecardOutput.get(1.0, END))

#	Code to open the titlecard letters popup

    def TitlecardLetters_Popup(self):
        global text
        TitlecardLettersToLoad = sub(r"[^a-zA-Z,' ']", "", text).upper()
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
        pep.insert(END, f'titleLetters	"{TitlecardLettersToLoad}"',)
        pep.configure(state = 'disabled')
        customtkinter.CTkLabel(
        top,
        text= f'The order for title card letters is the same as the order for the mappings code'
        ).pack()

#	Code to open the titlecard mapping locations popup

    def MappingLocations_Popup(self):
        global text
        TitlecardLettersToLoad = sub(r"[^a-zA-Z,' ']", "", text).upper()
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
        exit(0)

# create the application
title = "Sonic 2 Titlecard Code Generator"
root = customtkinter.CTk(className="S2TCG")
root.geometry("900x500")
root.resizable(True,True)
myapp = App(root)
myapp.master.title(title)
myapp.mainloop()
