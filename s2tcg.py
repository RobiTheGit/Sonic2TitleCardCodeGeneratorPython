import re
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
letter = 0

index2p = {
1:'2EF',
2:'2F1',
3:'2F3',
4:'2F5',
5:'2F7',
6:'2F9',
7:'2FB',
8:'2FD',
9:'2FE',
10:'NA',
11:'NA',
12:'NA',
13:'NA',
14:'NA',
15:'NA'
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
current = 1500
increment = 2
text = str(input('Level Name > '))
ntext = text.replace(" ", "")
hexi = hex(len(ntext))
print('In Obj34_MapUnc_147BA Put')
proper = hexi.replace("0x", "TC_Zone    dc.w $")
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
            if afterIcount == 0:
              #  afterI = False
                increment = 4  
            else:
                afterIcount -= 1   
        if char in charlist:
            x = code.index(char) 
            print(charlistcode[x],f'${XPOS} ; {char.upper()}')
        else:
            if char != 'z' and char != 'o' and char != 'n' and char != 'e' and char != ' ':  
                letter += 1 
                result = int(current)+int(increment)
                result2 = hex(result)
                INDEX = result2.replace("0x", "")
                INDEX2P = index2p.get(letter)
                indexcode = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')
                indexcode2 = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P},')
                charlistcode.append(indexcode2)
                print(indexcode)
                charlist.append(char)
                current = result
                if char == 'i':
                   afterI = True 
                   afterIcount = 2                   
            elif char == 'z':
                letter += 1 
                INDEX = '58C'
                INDEX2P = '2C6'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' ) 
            elif char == 'o':
                letter += 1            
                INDEX = '588'
                INDEX2P = '2C4'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )            
            elif char == 'n':
                letter += 1             
                INDEX = '584'
                INDEX2P = '2C2'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )                      
            elif char == 'e':
                letter += 1             
                INDEX = '580'
                INDEX2P = '2C0'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )                
            elif char == ' ':
                print('')
            
    print('In Off_TitleCardLetters')
    print(f'titleLetters	"{text.upper()}"')
    if debug == True:
        print(charlist)
        print(charlistcode)
    if len(charlistcode) > 9:
        print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
else:
    print('You can only have a maximum of $E characters in sonic 2 title cards')
print(f'\n Fix spacing manually!')

