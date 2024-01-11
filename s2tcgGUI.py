#!/usr/bin/python3 
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from re import sub
from sys import exit
import customtkinter
from customtkinter import *
from tkinter.filedialog import asksaveasfile
THEME = "DARK"
set_appearance_mode(THEME)  # Modes: system (default), light, dark
set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
"""
Generation Code
"""

global text, DebugFlag, LabelFlag, DisasmLabel
text = '' 
DebugFlag = False 
LabelFlag = False 
DisasmLabel = 0

def GenerateMappings(): 
#========================================================
#   Variable Setup
#========================================================
    global text, CharacterOfTitleCard, LetterIsAfterI, LetterIsAfterM, DebugFlag, LabelFlag
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
#========================================================
#   Start position setting code
#========================================================
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
#========================================================
#   Setup Code
#========================================================
    if len(AllOfTheCharacters) == 0:
         showerror(title='No Titlecard To Make!', message='You have no titlecard to generate!', options=None)
    else:
        if LabelFlag == False:
            proper = hexi.replace("0X", f"TC_{ZoneNameForLabel}:    dc.w $")
        else:
            proper = hexi.replace("0X", f"{ZoneNameForLabel}:    dc.w $")
            
        TitlecardOutput.insert(END,f';In Obj34_MapUnc_147BA Put\n')
        TitlecardOutput.insert(END,f'{proper}      \n')
        

    pos = -(len(AllOfTheCharacters))
#========================================================
#   Character Index Code
#========================================================
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
#========================================================
#   Position Calculation Code
#========================================================
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
#========================================================
#   Character Width Setting Code
#========================================================
            if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                CharacterWidth = '9'
            elif CharacterOfTitleCard == 'i':
                CharacterWidth = '1'
            else:
                CharacterWidth = '5'
#========================================================
#   Generation of Each Line code
#========================================================
            if CharacterOfTitleCard in CharactersList:
                x = CharactersList.index(CharacterOfTitleCard) 
                TitlecardOutput.insert(END,f'{SavedIndexes[x]}, ${XPOS} ;{CharacterOfTitleCard.upper()} \n')
                if CharacterOfTitleCard == 'i':
                   LetterIsAfterI = True 
                   LetterIsAfterIcount = 3
                   LetterIsAfterIposcount = 1
                if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                   LetterIsAfterM = True 
                   LetterIsAfterMcount = 3
                   LetterIsAfterMposcount = 1
#====================================================================
#   Generate Lines For Characters We Don't Already Have The Index Of
#====================================================================
            else:
                if CharacterOfTitleCard != 'z' and CharacterOfTitleCard != 'o' and CharacterOfTitleCard != 'n' and CharacterOfTitleCard != 'e' and CharacterOfTitleCard != ' ' and CharacterOfTitleCard.isalpha():  
                    CurrentCharacter += 1 
                    FinalIndex_Dec = int(Current_Index)+int(Index_Increment)
                    if LetterIsAfterI == True:
                        FinalIndex_Dec -= 2
                    Index2Hex = hex(FinalIndex_Dec)
                    INDEX = Index2Hex.replace("0x", "").upper()
                    TwoPlayerFinalIndex = int(Current_2PIndex)+int(Index_Increment_2P)
                    TwoPlayerFinalIndex_REGEX_STEP = hex(TwoPlayerFinalIndex) 
                    INDEX2P = TwoPlayerFinalIndex_REGEX_STEP.replace("0x", "").upper()
                    CodeForSavedIndexes = (f'\tdc.w {CharacterWidth}, $8{INDEX}, $8{INDEX2P}')
                    if LetterIsAfterI == True:
                        FinalIndex_Dec += 2 
                        if CharacterOfTitleCard == "m":
                            FinalIndex_Dec += 2  
                    SavedIndexes.append(CodeForSavedIndexes)
                    TitlecardOutput.insert(END,f'\tdc.w {CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ;{CharacterOfTitleCard.upper()} \n')
                    CharactersList.append(CharacterOfTitleCard)
                    Current_Index = FinalIndex_Dec
                    Current_2PIndex = TwoPlayerFinalIndex
                    if CharacterOfTitleCard == 'i':
                       LetterIsAfterI = True 
                       LetterIsAfterIcount = 3
                       LetterIsAfterIposcount = 1
                    if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                       LetterIsAfterM = True 
                       LetterIsAfterMcount = 3 
                       LetterIsAfterMposcount = 1
#========================================================
#   Z, O, N, & E line creation
#========================================================
                elif CharacterOfTitleCard == 'z':
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    TitlecardOutput.insert(END,f'\tdc.w {CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ;{CharacterOfTitleCard.upper()} \n') 
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1
                elif CharacterOfTitleCard == 'o':
                    INDEX = '588'
                    INDEX2P = '2C4'
                    TitlecardOutput.insert(END,f'\tdc.w {CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ;{CharacterOfTitleCard.upper()} \n') 
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1 
                elif CharacterOfTitleCard == 'n':
                    INDEX = '584'
                    INDEX2P = '2C2'
                    TitlecardOutput.insert(END,f'\tdc.w {CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ;{CharacterOfTitleCard.upper()} \n')
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1 
                elif CharacterOfTitleCard == 'e':
                    INDEX = '580'
                    INDEX2P = '2C0'
                    TitlecardOutput.insert(END,f'\tdc.w {CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ;{CharacterOfTitleCard.upper()} \n')
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1 
#========================================================
#   Code For Spaces
#========================================================
                elif CharacterOfTitleCard == ' ':
                    Current_XPOS += 2
                    TitlecardOutput.insert(END,'\n')

                else:
                     pass

        if len(AllOfTheCharacters) == 0:
            highlight(TitlecardOutput)
            pass
        else:
            TitlecardOutput.insert(END, f'\n; Open "Mapping Locations" for locations of titlecards\n; Open Mappings.txt for a replacement for the original mappings')
            highlight(TitlecardOutput)
#========================================================
#   Error Handling Code
#========================================================
            if len(LENGTH_STEP) > 16:
                TitlecardOutput.insert(END,'\n;You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
                highlight(TitlecardOutput)
                showerror(title='Error!', message='You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work', options=None) 
            if len(SavedIndexes) > 8:     
                TitlecardOutput.insert(END,'\n;You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
                highlight(TitlecardOutput)
                showerror(title='Error!', message='You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work', options=None)
            if PositionsIsAfter0 == True and Current_XPOS > 128:
                showerror(title='Error!', message='Position Out Of bounds', options=None)
            if DebugFlag == True:
                TitlecardOutput.insert(END, f'\n;Indexes: {CharactersList} {len(CharactersList)}\n;Code for above indexes:{SavedIndexes}\n;\tBut you can\'t stick n move')
                highlight(TitlecardOutput)
#========================================================
#   Syntax Highlighting Code
#========================================================
def highlight(text_to_highlight):
        for tag in text_to_highlight.tag_names():
            text_to_highlight.tag_delete(tag)
        red_highlight = ['.*?:']
        green_highlight = ['dc.w']
        blue_highlight = [';.*?$']
        orange_highlight = [f'\$.*?,', '.*?,', '\$.*? ', '".*?"']
#========================================================
#   Text In Red
#========================================================
        for word in red_highlight:  
            idx = "1.0"
            while True:
                length = IntVar()
                idx = text_to_highlight.search(r'(?:^|\s)' + word + r'(?:\s|$)', idx, nocase=1, stopindex='end',count=length, regexp = True)
                if idx:
                    idx2 = text_to_highlight.index("%s+%dc" % (idx, length.get()))
                    text_to_highlight.tag_add("red", idx, idx2)
                    text_to_highlight.tag_config("red", foreground="#ff2b2b")
                    idx = idx2
                else: 
                    break
#========================================================
#   Text In Orange
#========================================================
        for word in orange_highlight:  
            idx = "1.0"
            while True:
                length = IntVar()
                idx = text_to_highlight.search(word, idx, nocase=0, stopindex='end',count=length, regexp = True)
                if idx:
                    idx2 = text_to_highlight.index("%s+%dc" % (idx, length.get()))
                    text_to_highlight.tag_add("orange", idx, idx2)
                    text_to_highlight.tag_config("orange", foreground="#ffb238")
                    idx = idx2
                else: 
                    break
#========================================================
#   Text In Green
#========================================================
        for word in green_highlight:  
            idx = "1.0"
            while True:
                length = IntVar()
                idx = text_to_highlight.search(r'(?:^|\s)' + word + r'(?:\s|$)', idx, nocase=1, stopindex='end',count=length, regexp = True)
                if idx:
                    idx2 = text_to_highlight.index("%s+%dc" % (idx, length.get()))
                    text_to_highlight.tag_add("green", idx, idx2)
                    text_to_highlight.tag_config("green", foreground="#74b543")
                    idx = idx2
                else: 
                    break
#========================================================
#   Text In Blue
#========================================================
        for word in blue_highlight:  
            idx = "1.0"
            while True:
                length = IntVar()
                idx = text_to_highlight.search(f'{word}', idx, nocase=1, stopindex='end',count=length, regexp = True)
                if idx:
                    idx2 = text_to_highlight.index("%s+%dc" % (idx, length.get()))
                    text_to_highlight.tag_add("blue", idx, idx2)
                    text_to_highlight.tag_config("blue", foreground="#0197f6")
                    idx = idx2
                else: 
                    break
#========================================================
#   Generation Init Code
#========================================================
def GenerateTitlecardFromText():
    global text, TitlecardOutput, DebugFlag
    TitlecardOutput.configure(state='normal')
    TitlecardOutput.delete(1.0, END)
    GenerateMappings()
    TitlecardOutput.configure(state='disabled')

"""
Tkinter Code
"""

class App(Frame):
    global f
    def __init__(self, master):
        global BTNCLR, TXTCLR, text, TitlecardOutput, DebugFlag, DebugEnabledFlag, SwitchThemeFlag, zone, ZoneMenu, DisasmLabel, leftframe, topframe, bottomframe
        if THEME == "DARK":
           BTNCLR = "#272829"
           TXTCLR = "white"
        else:
           BTNCLR = "white"
           TXTCLR = "#272829"   
        DebugEnabledFlag = IntVar()
        zone = IntVar()
        DisasmLabel = IntVar()
        SwitchThemeFlag = IntVar()
        super().__init__(master)
        self.pack()
#========================================================================
#	Initilize left frame
#========================================================================
        leftframe = CTkFrame(root)
        leftframe.pack(side = LEFT, fill=BOTH, anchor = NE, padx = 5)
#========================================================================
 #	Initilize top frame
 #========================================================================
        topframe = CTkFrame(root)
        topframe.pack(side = TOP, fill=BOTH)
#========================================================================
#	Initilize bottom frame
#========================================================================
        bottomframe = CTkFrame(root)
        bottomframe.pack(side = TOP, fill=BOTH, pady = 5)
#========================================================================
#	Load icon for app
#========================================================================
        try:
            photo = PhotoImage(file ="icon.png")
            root.iconphoto(False, photo)
        except:
            pass
#========================================================================
#   Draw title
#========================================================================
        Title = CTkLabel(topframe, text="SONIC 2 TITLECARD CODE GENERATOR PYTHON \nBy: RobiWanKenobi", font = ('gaslight', 25))        
        Title.pack(side = TOP, fill=BOTH)
#========================================================================
#   Add label to tell people where input goes
#========================================================================
        inlbl = CTkLabel(leftframe, text='Input Title Card Name Here')
        inlbl.pack(side = TOP, anchor = NE)
#========================================================================
#   Add level name input
#========================================================================
        self.LevelName = CTkEntry(leftframe, placeholder_text="type level name")
        self.contents = StringVar()
        self.contents.set("")
        self.LevelName["textvariable"] = self.contents 
        self.LevelName.bind('<Key-Return>', self.RunFromEnterKey)
        self.LevelName.pack(side = TOP, anchor = NE,)
#========================================================================
#   Add button to generate the titlecard code
#========================================================================
        Generate = CTkButton(leftframe, fg_color=BTNCLR, text_color=TXTCLR, text = '  Generate Code', command = self.RunGeneration, font = ('gaslight', 30), height=3, width=9)
        Generate.pack(side = TOP, anchor = E)
#========================================================================
#   Add button to open the titlecard letters popup
#========================================================================
        TitlecardLetters = CTkButton(leftframe, fg_color=BTNCLR, text_color=TXTCLR, text = 'Titlecard Letters', command = self.TitlecardLetters_Popup, font = ('gaslight', 30), height=3, width=8)
        TitlecardLetters.pack(side = TOP, anchor = E)
#========================================================================
#   Add button to open the about screen
#========================================================================
        About = CTkButton(leftframe, fg_color=BTNCLR, text_color=TXTCLR, text = '  About S2tcg.py', command = self.OpenAbout, font = ('gaslight', 30), height=3, width=8)
        About.pack(side = TOP, anchor = SE)
#========================================================================
#   Add button to export the titlecard code
#========================================================================
        Export = CTkButton(leftframe, fg_color=BTNCLR, text_color=TXTCLR, text = 'Export Titlecard', command = self.ExportTitlecard, font = ('gaslight', 30), height=3, width=8)
        Export.pack(side = TOP, anchor = SE)
#========================================================================
#   Add button to open the mapping locations for titlecards popup
#========================================================================
        MappingsLocations = CTkButton(leftframe, fg_color=BTNCLR, text_color=TXTCLR, text = 'Mapping Locations', command = self.MappingLocations_Popup, font = ('gaslight', 30) ,height=3, width=8)
        MappingsLocations.pack(side = TOP, anchor = SE)
#========================================================================
#   Add the zone selector
#========================================================================
        ZoneList = ["EHZ","CPZ","ARZ","CNZ","HTZ","MCZ","OOZ","MTZ","SCZ","WFZ","DEZ","HPZ"]
        OldLabl = ['word_147E8', 'word_14A1E', 'word_14A88', 'word_149C4', 'word_14894', 'word_14972', 'word_14930', 'word_14842', 'word_14AE2', 'word_14B24', 'word_14B86', 'word_148CE']
        ZoneMenu = CTkOptionMenu(leftframe, fg_color=BTNCLR, text_color=TXTCLR,variable = zone,values=ZoneList)
        ZoneMenu.pack(side = BOTTOM) 
        ZoneMenu.set(ZoneMenu._values[0]) 
#========================================================================
#   Add the button to exit the program
#========================================================================
        exitbutton = CTkButton(
        leftframe, 
        fg_color=BTNCLR, text_color=TXTCLR, text = '     Exit     ', command = self.ExitProgram, font = ('gaslight', 30), height=3, width=8)
        exitbutton.pack(side = TOP, anchor = SE)
#========================================================================
#   Add the copy to clipboard button
#========================================================================
        copybutton = CTkButton(topframe, fg_color=BTNCLR, text_color=TXTCLR, text = 'Copy To Clipboard', command = self.CopyToClipboard, font = ('gaslight', 30), height=3, width=8)
        copybutton.pack(side = BOTTOM)
#========================================================================
#   Add the debug flag checkbox
#========================================================================
        DebugCheck = CTkCheckBox(topframe, text='See Debug Info', variable=DebugEnabledFlag, onvalue=1, offvalue=0, command=self.SetDebugFlag)
        DebugCheck.pack(side = BOTTOM)
#========================================================================
#   Add the Light/Dark mode checkbox
#========================================================================
        ThemeCheck = CTkCheckBox(topframe, text='Light Mode', variable=SwitchThemeFlag, onvalue=1, offvalue=0, command=self.ChangeAppTheme)
        ThemeCheck.pack(side = BOTTOM)
#========================================================================
#   Add the checkbox that makes the generator use the stock disasm labels
#========================================================================
        DisasmLabelCheck = CTkCheckBox(topframe, text='Use Regular Disasm Labels', variable=DisasmLabel, onvalue=1, offvalue=0, command=self.EnableNormalLabels)
        DisasmLabelCheck.pack(side = BOTTOM)
#========================================================================
#   Add the TitlecardOutput box
#========================================================================
        TitlecardOutput = CTkTextbox(bottomframe, state='disabled', height = 400, font = ("courier", 16))
        TitlecardOutput.pack(fill = BOTH)
#========================================================================
#   Code To Export Titlecard Into a File
#========================================================================
    def ExportTitlecard(self):
        global text
        if text == '':
            pass
        else:
            filename = asksaveasfile()
            f = open(str(filename), 'a')
            TitlecardLettersToLoad = sub(r"[^a-zA-Z,' ']", "", text).upper()
            f.write(TitlecardOutput.get(1.0, END))
            f.write(f'titleLetters	"{TitlecardLettersToLoad}"')
            f.close()
#========================================================
#   Code to run the generator
#========================================================
    def RunFromEnterKey(self, event):
        self.RunGeneration()
    def RunGeneration(self):
        global text, ZoneNameForLabel
        text = self.LevelName.get()
        OldLabl = ['word_147E8', 'word_14A1E', 'word_14A88', 'word_149C4', 'word_14894', 'word_14972', 'word_14930', 'word_14842', 'word_14AE2', 'word_14B24', 'word_14B86', 'word_148CE']
        if LabelFlag == False:
            ZoneNameForLabel = ZoneMenu.get()
        else:
            ZoneNameForLabel = OldLabl[ZoneMenu._values.index(ZoneMenu.get())]
        GenerateTitlecardFromText()
#========================================================
#   Code to set the debug flag
#========================================================
    def SetDebugFlag(self):
        global DebugEnabledFlag, DebugFlag
        if DebugEnabledFlag.get() == 0:
            DebugFlag = False
        elif DebugEnabledFlag.get() == 1:
            DebugFlag = True
        else:
            DebugFlag = False
#========================================================
#   Code to change themes
#========================================================
    def ChangeAppTheme(self):
        global BTNCLR, TXTCLR, SwitchThemeFlag
        
        if SwitchThemeFlag.get() == 0:
            THEME = "DARK"
            BTNCLR = "#272829"
            TXTCLR = "white"
        elif SwitchThemeFlag.get() == 1:
            THEME = "LIGHT"
            BTNCLR = "white"
            TXTCLR = "#272829"
        else:
            THEME = "DARK"
            BTNCLR = "#272829"
            TXTCLR = "white"
        for widget in leftframe.winfo_children():
            widget.configure(fg_color=BTNCLR, text_color=TXTCLR,)
        for widget in topframe.winfo_children():
            widget.configure(fg_color=BTNCLR, text_color=TXTCLR,)
        for widget in bottomframe.winfo_children():
            widget.configure(fg_color=BTNCLR, text_color=TXTCLR,)
        set_appearance_mode(THEME)  # Modes: system (default), light, dark
#========================================================        
#   Code to use the disasmebly labels
#========================================================
    def EnableNormalLabels(self):
        global DisasmLabel, LabelFlag
        if DisasmLabel.get() == 0:
            LabelFlag = False
        elif DisasmLabel.get() == 1:
            LabelFlag = True
        else:
            LabelFlag = False
#========================================================       
#   Code to copy TitlecardOutput to clipboard
#========================================================
    def CopyToClipboard(self):
        root.clipboard_clear()
        root.clipboard_append(TitlecardOutput.get(1.0, END))
#========================================================
#   Code to open the titlecard letters popup
#========================================================
    def TitlecardLetters_Popup(self):
        global text
        TitlecardLettersToLoad = sub(r"[^a-zA-Z,' ']", "", text).upper()
        top= CTkToplevel()
        top.geometry("600x400")
        top.resizable(False,False)
        top.title("Off_TitleCardLetters")
        CTkLabel(
        top,
        text= f'In Off_TitleCardLetters, for the zone title card you want to modify, where it says \ntitleLetters    "EMERALD HILL" or whatever zone you are replacing, \n you type in the zone\'s name, currently your titleLetters would have\n'
        ).pack()
        pep = CTkTextbox(top,
        state = 'normal',
        font = ("courier", 18)
        )
        pep.pack(fill = BOTH)
        CTkLabel(
        top,
        text= f'If you are using the 2007 Xenowhirl disasm, read Xenowhirl_Setup.txt\nUse the letter macros, and skip Z, O, N, & E\n' #Why you'd be using this disasm still, I have no clue
        ).pack()
        pep.delete(1.0, END)
        pep.insert(END, f'titleLetters	"{TitlecardLettersToLoad}"',)
        pep.configure(state = 'disabled')
        CTkLabel(
        top,
        text= f'The order for title card letters is the same as the order for the mappings code'
        ).pack()
#========================================================
#   Code to open the titlecard mapping locations popup
#========================================================
    def MappingLocations_Popup(self):
        global text
        TitlecardLettersToLoad = sub(r"[^a-zA-Z,' ']", "", text).upper()
        top= CTkToplevel()
        top.geometry("550x250")
        top.resizable(False,False)
        top.title("Titlecard Mapping Label Translation")
        pep2 = CTkTextbox(top,
        state = 'normal',
        font = ("courier", 18)
        )
        LocFile = open("Locations.txt", "r")
        pep2.pack(fill = BOTH)
        pep2.delete(1.0, END)
        pep2.insert(END, LocFile.read(),)
        pep2.configure(state = 'disabled')
#========================================================
#   Code To Open The About Popup
#========================================================
    def OpenAbout(self):
        showinfo(
        title='About',
        message="Sonic 2 Titlecard Code Generator in Python aka. S2TCG.py, created by RobiWanKenobi in \nPython 3.10.", options=None
        )
#========================================================
#   Code To Exit The Program
#========================================================
    def ExitProgram(self):
        exit(0)
#========================================================
#   Create The Application
#========================================================
title = "Sonic 2 Titlecard Code Generator"
root = CTk(className="S2TCG")
root.geometry("900x500")
root.resizable(True,True)
myapp = App(root)
myapp.master.title(title)
myapp.mainloop()
#========================================================================
#   END OF CODE
#========================================================================
