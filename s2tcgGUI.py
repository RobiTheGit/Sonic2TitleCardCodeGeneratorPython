import tkinter as tk
from tkinter import *
import re
import sys
global text
text = ''
def gen(): 
    global text
    global char
    global afterI
    global afterM
    debug = False
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
    btext = re.sub(r"[^a-zA-Z,' ']", "", text)
    ntext = btext.replace(" ", "")
    hexi = hex(len(ntext)).upper()
    if len(textt) >= 10:
        cur_pos = 65428
    elif len(textt) <= 9 and len(text) > 5:
        cur_pos = 0
        after0 = True            
    else:
        cur_pos = 28 
        after0 = True        
    proper = hexi.replace("0X", "TC_Zone    dc.w $")
    output.insert(END,f'In Obj34_MapUnc_147BA Put\n')
    output.insert(END,f'{proper} \n')
    char = ''
    code = []
    charlist = []
    charlistcode = []
    afterI = False 
    afterM = False
    afterS = False      
    for char in btext:
        code.append(char.lower())
        
    if len(code) == 0:
        pass
    pos = -(len(code))
    if len(char) <= 15:
        for char in code:
            if letter >= 1:
                increment = 4
            if afterI == True:
                increment = 2
                twopinc = 1
                pos_inc = 4
                if afterIcount == 0:
                    increment = 4
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
            if afterS == True:
                pos_inc = 18                    
                if afterScount == 0:
                    pos_inc = 16
                else:
                    afterScount -= 1                    
            if cur_pos <= pos_br:
                cur_pos += pos_inc
                char = char.lower()
                xpos_b = hex(cur_pos)
                if after0 == False:
                    XPOS = xpos_b.replace("0x", "").upper()
                else:
                    XPOS = xpos_b.replace("0x", "00").upper()
            elif cur_pos >= pos_br:
                cur_pos = 0
                XPOS = '0000'
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
                if char == 's':
                    afterS = True 
                    afterScount = 1 
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
                    if char == 's':
                        afterS = True 
                        afterScount = 1                 
                elif char == 'z':
          #          letter += 1 
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                elif char == 'o':
         #           letter += 1            
                    INDEX = '588'
                    INDEX2P = '2C4'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )            
                elif char == 'n':
        #            letter += 1             
                    INDEX = '584'
                    INDEX2P = '2C2'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )                         
                elif char == 'e':
       #             letter += 1             
                    INDEX = '580'
                    INDEX2P = '2C0'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )               
                elif char == ' ':
                    cur_pos += 2                   
                    output.insert(END,'\n')
                else:
                     pass
        output.insert(END,f'\n Fix spacing manually!')
        if len(code) > 16:
            output.insert(END,'You can only have a maximum of $E characters in sonic 2 title cards, this code will not work') 
        if len(charlistcode) > 8:     
            output.insert(END,'You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
        if debug == True:
            output.insert(END, f'{charlist}\n{charlistcode}')
def run():
    global text
    global output
    output.configure(state='normal')
    output.delete(1.0, END)
    gen()
    output.configure(state='disabled')       
    
#Letter Format
#dc.w $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER
class App(tk.Frame):
    global f
    def __init__(self, master):
        global text
        global output
        super().__init__(master)
        self.pack()        
        photo = PhotoImage(file ="icon.png")
        root.iconphoto(False, photo)        
        Title = tk.Label(text="SONIC 2 TITLECARD CODE GENERATOR PYTHON", font = ('gaslight', 18))
        Title.pack()
        self.entrythingy = tk.Entry()
        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.pack()
        B = tk.Button(text = 'GENERATE', command = self.getstr, relief = tk.RAISED, anchor = W, font = ('gaslight', 18))
        B.pack()
        B2 = tk.Button(text = 'TITLECARD LETTERS', command = self.open_popup, font = ('gaslight', 18))
        B2.pack()
        greeting = tk.Label(text="""
        
          
        
""")
        greeting.pack()
        output = tk.Text(state='disabled')
        output.pack()
    def getstr(self):
        global text
        text = self.contents.get()
        run()
    def open_popup(self):
        global text
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()
        top= Toplevel()
        top.geometry("1100x600")
        top.title("GITHUB Off_TitleCardLetters")
        Label(top, text= f'in off_titlecardletters, for the zone title card you want to modify,\n where it says \ntitleletters    "zonename"\n type in the zone\'s name where i use the placeholder "zonename", \ncurrently your titleletters would have\n', font = ('gaslight', 24)).pack()
        pep = Text(top, state = 'normal')
        pep.insert(END, f'titleLetters	"{titleletters}"',)
        pep.configure(state = 'disabled')
        pep.pack()
        
# create the application
root = tk.Tk(className="S2TCG")
myapp = App(root)
myapp.master.title("S2TCG")
myapp.mainloop()


