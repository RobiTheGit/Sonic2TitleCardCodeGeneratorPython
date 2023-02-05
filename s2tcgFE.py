import re
import sys
from sys import argv
try:
    script, text = argv
except:
    text = str(input('Level Name > '))
        
'''    
Letter Format
dc.w $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER
example: dc.w $0005, $85DE, $82EF, $0010; FIRST LETTER INDEX WHEN NOT (Z, O, N, E)
'''
debug = False
def gen(): 
    global text
    try:
        f = open('Titlecard.txt', 'a')
    except:
        print('error')
    pos_br = 65520 #position before setting position to $0
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
    hexi = hex(len(ntext)).upper()
    if len(btext) >= 10:
        cur_pos = 65428
    elif len(btext) <= 9 and len(btext) > 5:
        cur_pos = 0
        after0 = True            
    else:
        cur_pos = 28 
        after0 = True 
    if len(btext) == 0:
        print('No title card to generate!')
        sys.exit(0)       
    f.write(';In Obj34_MapUnc_147BA Put')
    f.write('\n')
    proper = hexi.replace("0X", "TC_EHZ    dc.w $")
    f.write(f'{proper} ; EHZ can be changed to the word it is or the title card name it is, the word for EHZ is word_147E8')
    f.write('\n')
    if debug == True:
        print(f';In Obj34_MapUnc_147BA Put\n{proper} ; EHZ can be changed to the word it is or the title card name it is, the word for EHZ is word_147E8\n')
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
                    if cur_pos >= 16:
                        XPOS = xpos_b.replace("0x", "00").upper() #this is also for dissam compatibility
                    elif cur_pos <= 16:
                        XPOS =  xpos_b.replace("0x", "000").upper()
                    else:    
                        XPOS =  xpos_b.replace("0x", "000").upper()
            elif cur_pos >= pos_br:
                cur_pos -= 65536
                xpos_b = hex(abs(cur_pos))
                if cur_pos >= 16:
                    XPOS = xpos_b.replace("0x", "00").upper() #this is also for dissam compatibility
                elif cur_pos <= 16:
                    XPOS =  xpos_b.replace("0x", "000").upper()
                else:    
                    XPOS =  xpos_b.replace("0x", "000").upper()
                after0 = True
            else:
                cur_pos -= 65536
                xpos_b = hex(cur_pos)
                if cur_pos >= 16:
                    XPOS = xpos_b.replace("0x", "00").upper() #this is also for dissam compatibility
                elif cur_pos <= 16:
                    XPOS =  xpos_b.replace("0x", "000").upper()
                else:    
                    XPOS =  xpos_b.replace("0x", "000").upper()
                after0 = True            
            if char == 'm' or char == 'w':
                width = '09'
            elif char == 'i':
                width = '01'
            else:
                width = '05'                                      
            if char in charlist:
                x = charlist.index(char) 
                f.write(f'{charlistcode[x]} ${XPOS} ; {char.upper()}')
                f.write('\n')
                if debug == True:
                    print(f'{charlistcode[x]} ${XPOS} ; {char.upper()}')
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
                    f.write(indexcode)
                    f.write('\n')
                    if debug == True:
                        print(indexcode)
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
                    f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    f.write('\n')
                    if debug == True:
                        print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')                    
                elif char == 'o':
                    INDEX = '588'
                    INDEX2P = '2C4'
                    f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    f.write('\n') 
                    if debug == True:
                        print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')                              
                elif char == 'n':
                    INDEX = '584'
                    INDEX2P = '2C2'
                    f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' ) 
                    f.write('\n')     
                    if debug == True:  
                        print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')               
                elif char == 'e':
                    INDEX = '580'
                    INDEX2P = '2C0'
                    f.write(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    f.write('\n') 
                    if debug == True:  
                        print(f'\tdc.w $00{width}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')           
                elif char == ' ':
                    f.write('\n')
                    cur_pos += 2
                    if debug == True:
                        print('\n')                 
                else:
                     pass
        titleletters = re.sub(r"[^a-zA-Z,' ']", "", text).upper()          
        f.write(f'In Off_TitleCardLetters\ntitleLetters	"{titleletters}" make sure you have no special characters here though.')
        if debug == True:
            print(f'In Off_TitleCardLetters\ntitleLetters	"{titleletters}" make sure you have no special characters here though.')
        if debug == True:
            f.write(f';Indexes: {charlist} {len(charlist)}\n;Code for above indexes:{charlistcode}\n\t;But you can\'t stick n move')  
            f.write('\n')       
        if len(charlistcode) > 8:
            f.write(';You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            f.write('\n')
        if len(ntext) > 16:
            f.write(';You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
            print('You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
            f.write('\n')
        if after0 == True and cur_pos >= 127:
            f.write(';Position Out Of bounds')
            print('Position Out Of bounds')
            f.write('\n')
    f.close()
    sys.exit(0)
gen() #run the code
