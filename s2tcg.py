import re
#letters are innacurate
letters = {
'a':'dc.w 5, $85E8, $82F4, $posi	; A',
'b':'dc.w 5, $85DE, $82EF, $posi	; B',
'c':'dc.w 5, $85E2, $82F1, $posi	; C',
'd':'dc.w 5, $85E6, $82F3, $posi	; D',
'e':'dc.w 5, $8580, $82C0, $posi	; E',
'f':'dc.w 5, $85EA, $82F5, $posi	; F',
'g':'dc.w 5, $85EE, $82F7, $posi	; G',
'h':'dc.w 5, $85F2, $82F9, $posi	; H',
'i':'dc.w 1, $85F6, $82FB, $posi	; I',
'j':'dc.w 5, $85F8, $82FC, $posi	; J',
'k':'dc.w 5, $85DE, $82EF, $posi	; K',
'l':'dc.w 5, $85E2, $82F1, $posi	; L',
'm':'dc.w 9, $85E6, $82F3, $posi	; M',
'n':'dc.w 5, $8584, $82C2, $posi	; N',
'o':'dc.w 5, $8588, $82C4, $posi	; O',
'p':'dc.w 5, $85EC, $82F6, $posi	; P',
'q':'dc.w 5, $85F0, $82F8, $posi	; Q',
'r':'dc.w 5, $85F4, $82FA, $posi	; R',
's':'dc.w 5, $85F8, $82FC, $posi	; S',
't':'dc.w 5, $85FC, $82FE, $posi	; T',
'u':'dc.w 5, $85100, $82100, $posi	; U',
'v':'dc.w 5, $85104, $82102, $posi	; V',
'w':'dc.w 9, $85108, $82104, $posi	; W',
'x':'dc.w 5, $8510E, $82107, $posi	; X',
'y':'dc.w 5, $85F2, $82F9, $posi	; Y',
'z':'dc.w 5, $858C, $82C6, $posi	; Z'
}
minpos = '$FFB1'
maxpos = '$70' 
text = str(input('Level Name > '))
ntext = text.replace(" ", "")
hexi = hex(len(ntext))
proper = hexi.replace("0x", "TC_Zone    dc.w $")
print(proper)
code = []
for char in ntext:
    code.append(char)
if len(char) <= 16:
    for char in code:
        try:
            print(letters[char])
        except KeyError:
            char = char.lower()
            print(letters[char])
    print(f'\n Spacing cannot be determined at the moment, so it is replaced with $posi, for now to start I reccomend the first letter at {minpos} and fix everything manually')
else:
    print('You can only have a maximum of 16 characters in sonic 2 title cards')
#print(example)
