#!/usr/bin/python3 
import re
import sys
from sys import argv
global export
export = input('Would you like to export the titlecard when it is generated. ')
if export.upper() == "TRUE" or export.upper() == "YES":
    export = True
else:
    export = False
try:
    script, text = argv
except:
    text = str(input('Level Name > '))   
'''
Letter Format
	dc.w        $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER
example: 
	dc.w        $0005, $85DE, $82EF, $FFD0; FIRST LETTER INDEX WHEN NOT (Z, O, N, E)
'''
debug = False
def gen(): 
    global text
    global f
    pos_br = 65535 #position before setting position to $0
    pos_inc = 16 #$10, after M or W, 24/$18, after I, 8/$8
    cur_pos = 65428 #starts with the starting position
    after0 = False
    letter = 0
    current = 1500
    twopcurrent = 749
    increment = 2
    twopinc = 2
    afterI = False 
    afterM = False
    btext = re.sub(r"[^a-zA-Z ]", "", text)
    ntext = btext.replace(" ", "")
    if export == True:
        if len(btext) == 0:
            pass
        else:
            f = open(f'{btext.upper()}.txt', 'a')
    hexi = hex(len(ntext)).upper()
    if len(btext) >= 10: 
        cur_pos = 65428
    elif len(btext) <= 9 and len(btext) > 6:
        cur_pos = 65446
    elif len(btext) <= 6 and len(btext) > 4:
        cur_pos = 0
        after0 = True            
    else:
        cur_pos = 64 
        after0 = True
    if len(btext) == 0:
        print('No title card to generate!')
        sys.exit(0)  
    if export == True:     
        f.write(';In Obj34_MapUnc_147BA Put')
        f.write('\n')
    proper = hexi.replace("0X", "TC_LVL:    dc.w $")
    if export == True:
        f.write(f'{proper}')
        f.write('\n')
    print(f';In Obj34_MapUnc_147BA Put\n{proper}')
    code = []
    charlist = []
    charlistcode = []
    for char in btext:
        code.append(char.lower())
    if len(code) == 0:
        print('No title card to generate!')
        sys.exit(0)
    pos = -(len(code))
    if len(char) <= 15:
        for char in code:
            if letter >= 1:
                increment = 4 #the first letter is 2 and not 4
            if afterI == True:
                pos_inc = 4 #incrememnt the position less
                if afterIcount == 0:
                    increment = 4  #restore the default values
                    twopinc = 2 
                    pos_inc = 8 
                else:
                    if afterIposcount == 0:
                        pos_inc = 16
                    else:
                        cur_pos += 8
                        afterIposcount = 0                      
            if afterM == True:
                pos_inc = 24   
                twopinc = 3 
                increment = 6  #restore the default values                 
                if afterMcount == 0:
                    increment = 4  #restore the default values
                    twopinc = 2 
                    pos_inc = 16
                    afterM = False                    
                else:
                    afterMcount -= 1 
                    if afterMposcount == 0:
                        increment = 4  #restore the default values
                        twopinc = 2 
                        pos_inc = 16
                        afterM = False
                    else:
                        afterMposcount = 0                  
            cur_pos += pos_inc #increment position by the position incrementer, there is a reason this is defined after the afterM and afterI stuff
            if cur_pos <= pos_br:
                char = char.lower()
                xpos_b = hex(cur_pos)
                if after0 == False:
                    XPOS = xpos_b.replace("0x", "").upper()
                else:
                    if cur_pos >= 16:
                        XPOS = xpos_b.replace("0x", "00").upper()
                    elif cur_pos <= 16:
                        XPOS =  xpos_b.replace("0x", "000").upper()
                    else:    
                        XPOS =  xpos_b.replace("0x", "000").upper()
            elif cur_pos >= pos_br:
                cur_pos -= 65536
                xpos_b = hex(abs(cur_pos))
                if cur_pos >= 16:
                    XPOS = xpos_b.replace("0x", "00").upper()
                elif cur_pos <= 16:
                    XPOS =  xpos_b.replace("0x", "000").upper()
                else:    
                    XPOS =  xpos_b.replace("0x", "000").upper()
                after0 = True
            else:
                after0 = True                                           
                cur_pos -= 65536
                xpos_b = hex(abs(cur_pos))
                if cur_pos >= 16:
                    XPOS = xpos_b.replace("0x", "00").upper()
                if cur_pos <= 16:
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
                if export == True: 
                    f.write(f'{charlistcode[x]} ${XPOS} ; {char.upper()}')
                    f.write('\n')
                print(f'{charlistcode[x]} ${XPOS} ; {char.upper()}')
            else:
                if char != 'z' and char != 'o' and char != 'n' and char != 'e' and char != ' ' and char.isalpha():  
                    letter += 1 
                    result = int(current)+int(increment)
                    if afterI == True:
                        result -= 2                    
                    result2 = hex(result)
                    INDEX = result2.replace("0x", "").upper()
                    twopresult = int(twopcurrent)+int(twopinc)
                    twopres2 = hex(twopresult) 
                    INDEX2P = twopres2.replace("0x", "").upper()
                    indexcode = (f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')
                    indexcode2 = (f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P} ')
                    if afterI == True:
                        result += 2 
                    charlistcode.append(indexcode2)   
                    if export == True: 
                        f.write(indexcode)
                        f.write('\n')
                    print(indexcode)
                    charlist.append(char)
                    current = result
                    twopcurrent = twopresult
                    if char == 'i':
                       afterI = True 
                       afterIcount = 1
                       afterIposcount = 1                                                                                                           
                    if char == 'm' or char == 'w':
                       afterM = True 
                       afterMcount = 1
                       afterMposcount = 1                                           
                elif char == 'z':
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    if export == True:
                        f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                        f.write('\n')
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1                    
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')                    
                elif char == 'o':
                    INDEX = '588'
                    INDEX2P = '2C4'
                    if export == True:
                        f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                        f.write('\n')
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1                     
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')                              
                elif char == 'n':
                    INDEX = '584'
                    INDEX2P = '2C2'
                    if export == True:
                        f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' ) 
                        f.write('\n')
                    
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1                         
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')               
                elif char == 'e':
                    INDEX = '580'
                    INDEX2P = '2C0'
                    if export == True:
                        f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                        f.write('\n') 
                    if afterI == True:
                       afterIcount += 1
                    if afterM == True:
                       afterMcount += 1
                    print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')           
                elif char == ' ':
                    if export == True:
                        f.write('\n')
                    cur_pos += 2
                    print('\n')                 
                else:
                     pass
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()          
        if export == True:
            f.write(f'In Off_TitleCardLetters\ntitleLetters	"{titleletters}" make sure you have no special characters here though.\nIf you are using the 2007 Xenowhirl disasm, read Xenowhirl_Setup.txt, and use the letter macros, and skip Z, O, N, & E')
        print(f'In Off_TitleCardLetters\ntitleLetters	"{titleletters}" make sure you have no special characters here though.\nIf you are using the 2007 Xenowhirl disasm, read Xenowhirl_Setup.txt, and use the letter macros, and skip Z, O, N, & E')
        if debug == True:
            if export == True:
                f.write(f';Indexes: {charlist} {len(charlist)}\n;Code for above indexes:{charlistcode}\n\t;But you can\'t stick n move')  
                f.write('\n')
            print(';Indexes: {charlist} {len(charlist)}\n;Code for above indexes:{charlistcode}\n\t;But you can\'t stick n move')     
        if len(charlistcode) > 8:
            if export == True:
                f.write(';You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            if export == True:
                f.write('\n')
        if len(ntext) > 16:
            if export == True:
                f.write(';You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
            print('You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
            if export == True:
                f.write('\n')
        if after0 == True and cur_pos >= 112:
            if export == True:
                f.write(';Position Out Of bounds')
            print('Position Out Of bounds')
            if export == True:
                f.write('\n')

        if export == True:
            f.write(f'\n; Check The Wiki on GitHub or Locations.txt for the locations of the mappings\n; Look in Mappings.txt for a replacement for the original mappings')
        print(f'\n; Check The Wiki on GitHub or Locations.txt for the locations of the mappings\n; Look in Mappings.txt for a replacement for the original mappings')

    if export == True:
        f.close()
    sys.exit(0)
gen() #run the code
