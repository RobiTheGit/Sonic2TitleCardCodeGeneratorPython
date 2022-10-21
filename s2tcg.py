import re
#some letters may not be accurate :(
letters = {
'a':'dc.w 5,	$85E2, $82F1, $posi	;A',
'b':'dc.w 5,	$85EA, $82F5, $poai	;B',
'c':'dc.w 5,	$85EA, $82F5, $posi  	;C',
'd':'dc.w 5,	$85E6, $82F3, $posi	;D',
'e':'dc.w 5,	$8580, $82C0, $posi	;E',
'f':'dc.w 5,	$85EA, $82F5, $posi	;F',
'g':'dc.w 5,	$85E6, $82F3, $posi	;G',
'h':'dc.w 5,	$85DE, $82EF, $posi	;H',
'i':'dc.w 1,	$85E2, $82F1, $posi	;I',
'j':'dc.w 5,	$85DE, $82EF, $posi	;J',
'k':'dc.w 5,	$85E2, $82F1, $posi	;K',
'l':'dc.w 5,	$85E0, $82F7, $posi  	;L',
'm':'dc.w 9,	$85DE, $82EF, $posi	;M',
'n':'dc.w 5,	$8584, $82C2, $posi	;N',
'o':'dc.w 5,	$8588, $82C4, $posi	;O',
'p':'dc.w 5,	$85EC, $82F6, $psoi	;P',
'q':'dc.w 5,	$85E2, $82F1, $posi	;Q',
'r':'dc.w 5,	$85E8, $82F4, $posi  	;R',
's':'dc.w 5,	$85F6, $82FB, $posi  	;S',
't':'dc.w 5,	$85E4, $82F2, $posi   	;T',
'u':'dc.w 5,	$85E6, $82F3, $posi	;U',
'v':'dc.w 5,	$85EA, $82F5, $posi	;V',
'w':'dc.w 9,	$85DE, $82EF, $posi	;W',
'x':'undefined',
'y':'dc.w 5,	$85E6, $82F3, $posi  	;Y',
'z':'dc.w 5,	$858C, $82C6, $posi  	;Z'
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
