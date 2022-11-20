import re
#some letters may need to have changes to not cause issues

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
9:'5FE',
10:'602',
11:'606',
12:'60A',
13:'60E',
14:'612',
15:'616'
}
pos = -1
XPOSLIST = ['FFA4','FFB4','FFC4','FFD4','FFE4','FFF4','0000','0010','0020','0030','0040','0050','0060','0070','0080']
minpos = '$FFB1'
maxpos = '$70' 
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
print(code)
if len(char) <= 15:
    for char in code:
        pos += 1
        char = char.lower()
        XPOS = XPOSLIST[pos]
        if char in charlist:
            code2 = code.index(char)
            print(charlistcode[code2],f'${XPOS} ; {char.upper()}')
        else:
            if char != 'z' and char != 'o' and char != 'n' and char != 'e':
                letter += 1 
                INDEX = index1p.get(letter)
                INDEX2P = '2EF'
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
            
    print(f'\n Fix spacing manually! 2 player vs not supported!')
    print(f'titleLetters	"{text.upper()}"')
    print(charlist)
else:
    print('You can only have a maximum of $E characters in sonic 2 title cards')
#print(example)
