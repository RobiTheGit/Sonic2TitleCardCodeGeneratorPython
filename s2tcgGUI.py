import tkinter as tk
from tkinter import *
import re
import sys
global text

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
                pos_inc = 8
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
                    
            if cur_pos <= pos_br:
                cur_pos += pos_inc
                char = char.lower()
                xpos_b = hex(cur_pos)
                if after0 == False:
                    XPOS = xpos_b.replace("0x", "").upper()
                else:
                    XPOS = xpos_b.replace("0x", "00").upper()
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
                    indexcode2 = (f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P},')
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
                    letter += 1 
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                elif char == 'o':
                    letter += 1            
                    INDEX = '588'
                    INDEX2P = '2C4'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )            
                elif char == 'n':
                    letter += 1             
                    INDEX = '584'
                    INDEX2P = '2C2'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )                         
                elif char == 'e':
                    letter += 1             
                    INDEX = '580'
                    INDEX2P = '2C0'
                    output.insert(END,f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )               
                elif char == ' ':
                    print('')
                    cur_pos += 16                   
                    output.insert(END,'\n')
                else:
                     pass
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()          
        output.insert(END,f'In Off_TitleCardLetters\n')
        output.insert(END,f'titleLetters	"{titleletters}" make sure you have no special characters here though.')
        output.insert(END,f'\n Fix spacing manually!')
        if len(code) > 15:
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
        self.entrythingy = tk.Entry()
        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents 
        self.entrythingy.pack()
        B = tk.Button(text = 'Generate', command = self.getstr, relief = tk.RAISED)
        B.pack()
        greeting = tk.Label(text="""
        
                          
        
       
        
        
        
        
        
""")
        greeting.pack()
        output = tk.Text(state='disabled')
        output.pack()
    def getstr(self):
        global text
        text = self.contents.get()
        run()
# create the application
root = tk.Tk()
myapp = App(root)
myapp.master.title("S2TCG")
myapp.master.maxsize(1000, 400)
myapp.mainloop()


