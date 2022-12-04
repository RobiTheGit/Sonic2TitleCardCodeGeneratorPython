import re
import sys
export = False #set this to True if you want to export the code to a file
if export == True:
    f = open('titlecard.txt', 'x')
#Letter Format
#dc.w $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER
def gen(): 
    global export
    if export == True:
        global f
    debug = False
#position variables
    pos_br = 65520 #position before setting position to $0
    pos_inc = 16 #$10, after M or W, 24/$18, after I, 8/$8
    cur_pos = 65428 #starts with the starting position
    after0 = False
#index variables    
    letter = 0
    current = 1500
    twopcurrent = 749
    increment = 2
    twopinc = 2
#Text Variables
    text = str(input('Level Name > '))
    btext = re.sub(r"[^a-zA-Z,' ']", "", text)
    ntext = btext.replace(" ", "")
    hexi = hex(len(ntext)).upper()
    if len(text) >= 10:
        cur_pos = 65428
    elif len(text) <= 9 and len(text) > 5:
        cur_pos = 0
        after0 = True            
    else:
        cur_pos = 28 
        after0 = True        
    print('In Obj34_MapUnc_147BA Put')
    proper = hexi.replace("0X", "TC_Zone    dc.w $")
    if export == True:
        f.write(f'In Obj34_MapUnc_147BA Put\n')
        f.write(f'{proper} \n')
    print(proper)
    code = []
    charlist = []
    charlistcode = []
    for char in btext:
        code.append(char.lower())
    if len(code) == 0:
        sys.exit(0)
#Positioning code   
        afterI = False 
        afterM = False 
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
#Width Setting Code
            if char == 'm' or char == 'w':
                width = '09'
            elif char == 'i':
                width = '01'
            else:
                width = '05'
#Mappings Generation Code                                        
            if char in charlist:
                x = charlist.index(char) 
                print(charlistcode[x],f'${XPOS} ; {char.upper()}')
                if export == True:
                    f.write(f'{charlistcode[x]},${XPOS} ; {char.upper()} \n')
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
                    print(indexcode)
                    if export == True:
                        f.write(f'{indexcode} \n')
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
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True:
                        f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                elif char == 'o':
                    letter += 1            
                    INDEX = '588'
                    INDEX2P = '2C4'
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True:
                        f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )            
                elif char == 'n':
                    letter += 1             
                    INDEX = '584'
                    INDEX2P = '2C2'
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True: 
                         f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )                         
                elif char == 'e':
                    letter += 1             
                    INDEX = '580'
                    INDEX2P = '2C0'
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True:
                        f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )               
                elif char == ' ':
                    print('')
                    cur_pos += 16                   
                    if export == True:
                        f.write('\n')
                else:
                     pass
#Misc Code  
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()          
        print('In Off_TitleCardLetters')
        print(f'titleLetters	"{titleletters}" make sure you have no special characters here though.')
        if debug == True:
            print(charlist)
            print(charlistcode)         
        if len(charlistcode) > 8:
            print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
        if len(code) > 15:
            print('You can only have a maximum of $E characters in sonic 2 title cards, this code will not work')
        if export == False:
            print(f'\n Fix spacing manually!') 
#Exporting Code For The Things Above           
        if export == True:
            f.write(f'In Off_TitleCardLetters\n')
            f.write(f'titleLetters	"{titleletters}"make sure you have no special characters here though.')
            print(f'\n Fix spacing manually! The code can also be found in titlecard.txt, make sure to delete it before making a new one')
            f.write(f'\n Fix spacing manually! Rename this file or delete it, or turn off export before running s2tcg.py again')
            if len(code) > 15:
                f.write('You can only have a maximum of $E characters in sonic 2 title cards, this code will not work') 
            if len(charlistcode) > 8:     
                  f.write('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            if debug == True:
                f.write(f'{charlist}\n{charlistcode}')
    sys.exit(0)
gen()
