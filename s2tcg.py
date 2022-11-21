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
#combined letters are posible, but this is for standard use cases
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

index1p = {
1:'5DE',
2:'5E2',
3:'5E6',
4:'5EA',
5:'5EE',
6:'5F2',
7:'5F6',
8:'5FA',
9:'5FC',
10:'NA',
11:'NA',
12:'NA',
13:'NA',
14:'NA',
15:'NA'
}
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
pos = -1
XPOSLIST = {
0:'FFA4',
1:'FFB4',
2:'FFC4',
3:'FFD4',
4:'FFE4',
5:'FFF4',
6:'0000',
7:'0010',
8:'0020',
9:'0030',
10:'0040',
11:'0050',
12:'0060',
13:'0070',
14:'0080'
}

text = str(input('Level Name > '))
ntext = text.replace(" ", "")
hexi = hex(len(ntext))
proper = hexi.replace("0x", "TC_Zone    dc.w $")
print(proper)
code = []
charlist = []
charlistcode = []
for char in ntext:
    code.append(char.lower())
#print(code)
pos = -1
print('In Obj34_MapUnc_147BA Put')
if len(char) <= 15:
    for char in code:
        pos += 1
        char = char.lower()
        XPOS = XPOSLIST.get(pos)
        if char in charlist:
            x = code.index(char) 
            print(charlistcode[x],f'${XPOS} ; {char.upper()}')
        else:
            if char != 'z' and char != 'o' and char != 'n' and char != 'e':
                letter += 1 
                INDEX = index1p.get(letter)
                INDEX2P = index2p.get(letter)
                indexcode = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}')
                indexcode2 = (f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P},')
                charlistcode.append(indexcode2)
                print(indexcode)
                charlist.append(char)
            elif char == 'z':
                INDEX = '58C'
                INDEX2P = '2C6'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' ) 
            
            elif char == 'o':
                INDEX = '588'
                INDEX2P = '2C4'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
             
            elif char == 'n':
                INDEX = '584'
                INDEX2P = '2C2'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
                        
            elif char == 'e':
                INDEX = '580'
                INDEX2P = '2C0'
                print(f'\tdc.w $00{width[char]}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {char.upper()}' )
            
    print(f'\n Fix spacing manually!')
    print('In Off_TitleCardLetters')
    print(f'titleLetters	"{text.upper()}"')
    print(charlist)
    print(charlistcode)
    if len(charlistcode) > 9:
        print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
else:
    print('You can only have a maximum of $E characters in sonic 2 title cards')

