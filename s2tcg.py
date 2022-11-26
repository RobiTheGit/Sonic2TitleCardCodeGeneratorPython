import re
export = False #set this to True if you want to export the code to a file
if export == True:
    f = open('titlecard.txt', 'x')
#Letter Format

#dc.w $VERTOFF+WIDTH, $PRI+INDEX, $PRI+INDEX2P, $XPOS ; LETTER

#s2.asm will handle lowercase letters just fine

def gen(): 
    global export
    if export == True:
        global f
    debug = False
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
    if export == True:
        f.write(f'In Obj34_MapUnc_147BA Put\n')
    proper = hexi.replace("0x", "TC_Zone    dc.w $")
    if export == True:    
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
                if export == True:
                    f.write(f'{charlistcode[x]},${XPOS} ; {char.upper()} \n')
            else:
                if char != 'z' and char != 'o' and char != 'n' and char != 'e' and char != ' ':  
                    letter += 1 
                    result = int(current)+int(increment)
                    result2 = hex(result)
                    INDEX = result2.replace("0x", "").upper()
                    twopresult = int(twopcurrent)+int(twopinc)
                    twopres2 = hex(twopresult) 
                    INDEX2P = twopres2.replace("0x", "").upper()
                    indexcode = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')
                    indexcode2 = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P},')
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
                elif char == 'z':
                    letter += 1 
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True:
                        f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' ) 
                elif char == 'o':
                    letter += 1            
                    INDEX = '588'
                    INDEX2P = '2C4'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True:
                        f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )            
                elif char == 'n':
                    letter += 1             
                    INDEX = '584'
                    INDEX2P = '2C2'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True: 
                         f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )                         
                elif char == 'e':
                    letter += 1             
                    INDEX = '580'
                    INDEX2P = '2C0'
                    print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                    if export == True:
                        f.write(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()} \n' )               
                elif char == ' ':
                    print('')
                    if export == True:
                        f.write('\n')
            
        print('In Off_TitleCardLetters')
        if export == True:
            f.write(f'In Off_TitleCardLetters\n')
        print(f'titleLetters	"{text.upper()}"')
        if export == True:
            f.write(f'titleLetters	"{text.upper()}"')        
        if debug == True:
            print(charlist)
            print(charlistcode)
        if len(charlistcode) > 9:
            print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            if export == True:
                f.write('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
        if len(code) > 15:
            print('You can only have a maximum of $E characters in sonic 2 title cards')
            if export == True:
                f.write('You can only have a maximum of $E characters in sonic 2 title cards')
            
        print(f'\n Fix spacing manually!')
        if export == True:
            f.write(f'\n Fix spacing manually! The code can also be found in titlecard.txt, make sure to delete it before making a new one')
gen()
