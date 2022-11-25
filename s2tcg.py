import re
f = open('titlecard.txt', 'x')
#Since Jade Valley Doesn't Work, I will provide you the code for it
#TC_ZONE:		dc.w $A
#	dc.w $0005, $85DE, $82EF, $FFD0 ; J
#	dc.w $0005, $85E2, $82F1, $FFE0 ; A
#	dc.w $0005, $85E6, $82F3, $FFF0 ; D
#	dc.w $0005, $8580, $82C0, $0000 ; E
#	
#	dc.w $0005, $85EA, $82F5, $0020 ; V
#	dc.w $0005, $85E2, $82F1, $0030 ; A
#	dc.w $0005, $85EE, $82F7, $0040 ; L
#	dc.w $0005, $85EE, $82F7, $0050 ; L
#	dc.w $0005, $8580, $82C0, $0060 ; E
#	dc.w $0005, $85F2, $82F9, $0070 ; Y
#Letter Format
#dc.w $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER
#s2.asm will handle lowercase letters just fine
def gen(): 
    debug = True
    width = {
'a':'05',
'b':'05',
'c':'05',
'd':'05',
'e':'05',
'f':'05',
'g':'05',
'h':'05',
'i':'01',
'j':'05',
'k':'05',
'l':'05',
'm':'09',
'n':'05',
'o':'05',
'p':'05',
'q':'05',
'r':'05',
's':'05',
't':'05',
'u':'05',
'v':'05',
'w':'09',
'x':'05',
'y':'05',
'z':'05'
}
    XPOSLIST = {
-14:'FFA4',
-13:'FFB4',
-12:'FFC4',
-11:'FFD4',
-10:'FFE4',
-9:'FFF4',
-8:'0000',
-7:'0010',
-6:'0020',
-5:'0030',
-4:'0040',
-3:'0050',
-2:'0060',
-1:'0070',
0:'0080'
}   
    letter = 0
    current = 1500
    twopcurrent = 749
    increment = 2
    twopinc = 2
    text = str(input('Level Name > '))
    ntext = text.replace(" ", "")
    hexi = hex(len(ntext))
    print('In Obj34_MapUnc_147BA Put')
    f.write(f'In Obj34_MapUnc_147BA Put\n')
    proper = hexi.replace("0x", "TC_Zone    dc.w $")
    f.write(f'{proper} \n')
    print(proper)
    code = []
    charlist = []
    charlistcode = []
    for char in text:
        code.append(char.lower())   
        afterI = False  
        pos = -(len(code))
    if len(char) <= 15:
        for char in code:
            pos += 1
            char = char.lower()
            XPOS = XPOSLIST.get(pos)
            if letter >= 1:
                increment = 4
            if afterI == True:
                increment = 2
                twopinc = 1
                if afterIcount == 0:
                    increment = 4
                    twopinc = 2
                else:
                    afterIcount -= 1   
            if char in charlist:
                x = code.index(char) 
                print(charlistcode[x],f'${XPOS} ; {char.upper()}')
                f.write(f'{charlistcode[x]},${XPOS} ; {char.upper()} \n')
            else:
                if char != 'z' and char != 'o' and char != 'n' and char != 'e' and char != ' ':  
                    letter += 1 
                    result = int(current)+int(increment)
                    result2 = hex(result)
                    INDEX = result2.replace("0x", "")
                    twopresult = int(twopcurrent)+int(twopinc)
                    twopres2 = hex(twopresult) 
                    INDEX2P = twopres2.replace("0x", "")
                    indexcode = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')
                    indexcode2 = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P},')
                    charlistcode.append(indexcode2)    
                    print(indexcode)
                    f.write(f'{indexcode} \n')
                    charlist.append(char)
                    current = result
                    twopcurrent = twopresult
                    if char == 'i':
                       afterI = True 
                       afterIcount = 2                   
                elif char == 'z':
                    letter += 1 
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                elif char == 'o':
                    letter += 1            
                    INDEX = '588'
                    INDEX2P = '2C4'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )            
                elif char == 'n':
                    letter += 1             
                    INDEX = '584'
                    INDEX2P = '2C2'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' ) 
                    f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )                         
                elif char == 'e':
                    letter += 1             
                    INDEX = '580'
                    INDEX2P = '2C0'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' ) 
                    f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )               
                elif char == ' ':
                    print('')
                    f.write('\n')
            
        print('In Off_TitleCardLetters')
        f.write(f'In Off_TitleCardLetters\n')
        print(f'titleLetters	"{text.upper()}"')
        f.write(f'titleLetters	"{text.upper()}"')        
        if debug == True:
            print(charlist)
            print(charlistcode)
        if len(charlistcode) > 9:
            print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
        else:
            print('You can only have a maximum of $E characters in sonic 2 title cards')
            print(f'\n Fix spacing manually! Also, Sonic 2 can handle lowercase $A-$F. The code can also be found in titlecard.txt, make sure to delete it before making a new one')
gen()
