#!/usr/bin/python3 
from re import sub
from sys import exit
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
DebugFlag = False
def GenerateTitlecardFromText(): 
    global text
    global f
    NegativeToPositive_Position = 65535 #position before setting position to $0
    SpaceBetweenLetter = 16 #$10, after M or W, 24/$18, after I, 8/$8
    Current_XPOS = 65428 #starts with the starting position
    PositionsIsAfter0 = False
    CurrentCharacter = 0
    Current_Index = 1500
    Current_2PIndex = 749
    Index_Increment = 2
    Index_Increment_2P = 2
    LetterIsAfterI = False 
    LetterIsAfterM = False
    REGEX_STEP = sub(r"[^a-zA-Z ]", "", text)
    LENGTH_STEP = REGEX_STEP.replace(" ", "")
    if export == True:
        if len(REGEX_STEP) == 0:
            pass
        else:
            f = open(f'{REGEX_STEP.upper()}.txt', 'a')
    hexi = hex(len(LENGTH_STEP)).upper()
    if len(REGEX_STEP) >= 10: 
        Current_XPOS = 65428
    elif len(REGEX_STEP) <= 9 and len(REGEX_STEP) > 6:
        Current_XPOS = 65446
    elif len(REGEX_STEP) <= 6 and len(REGEX_STEP) > 2:
        Current_XPOS = 0
        PositionsIsAfter0 = True            
    else:
        Current_XPOS = 64 
        PositionsIsAfter0 = True
    if len(REGEX_STEP) == 0:
        print('No title card to generate!')
        exit(0)  
    if export == True:     
        f.write(';In Obj34_MapUnc_147BA Put')
        f.write('\n')
    proper = hexi.replace("0X", "TC_LVL:    dc.w $")
    if export == True:
        f.write(f'{proper}')
        f.write('\n')
    print(f';In Obj34_MapUnc_147BA Put\n{proper}')
    AllOfTheCharacters = []
    CharactersList = []
    SavedIndexes = []
    for CharacterOfTitleCard in REGEX_STEP:
        AllOfTheCharacters.append(CharacterOfTitleCard.lower())
    if len(AllOfTheCharacters) == 0:
        print('No title card to generate!')
        exit(0)
    pos = -(len(AllOfTheCharacters))
    if len(CharacterOfTitleCard) <= 15:
        for CharacterOfTitleCard in AllOfTheCharacters:
            if CurrentCharacter >= 1:
                Index_Increment = 4 #the first letter is 2 and not 4
                if LetterIsAfterI == True:
                    SpaceBetweenLetter = 4 #incrememnt the position less
                    if LetterIsAfterIcount == 0:
                        if LetterIsAfterM == False:
                            Index_Increment = 4  #restore the default values
                            Index_Increment_2P = 2 
                        SpaceBetweenLetter = 8 
                    else:
                        if LetterIsAfterIposcount == 0:
                            Index_Increment = 6  #restore the default values
                            Index_Increment_2P = 3 
                            SpaceBetweenLetter = 16
                        else:
                            Index_Increment = 6  #restore the default values
                            Index_Increment_2P = 3                   
                            Current_XPOS += 8
                            LetterIsAfterIposcount = 0

                if LetterIsAfterM == True:
                    SpaceBetweenLetter = 24 
                    if LetterIsAfterI == False: 
                        Index_Increment_2P = 3 
                        Index_Increment = 6  #restore the default values
                    else:
                        Index_Increment = 4  #restore the default values
                        Index_Increment_2P = 2                     
                    if LetterIsAfterMcount == 0:
                        if LetterIsAfterI == False:
                            LetterIsAfterMcount += 1
                        else:
                            Index_Increment = 4  #restore the default values
                            Index_Increment_2P = 2 
                        SpaceBetweenLetter = 16
                        LetterIsAfterM = False
                    else:
                        LetterIsAfterMcount -= 1 
                        if LetterIsAfterMposcount == 0:
                            SpaceBetweenLetter = 16
                            LetterIsAfterM = False
                        else:
                            LetterIsAfterMposcount = 0                  
            Current_XPOS += SpaceBetweenLetter #Index_Increment position by the position Index_Incrementer, there is a reason this is defined after the LetterIsAfterM and LetterIsAfterI stuff
            if Current_XPOS <= NegativeToPositive_Position:
                CharacterOfTitleCard = CharacterOfTitleCard.lower()
                PreFinal_XPOS = hex(Current_XPOS)
                if PositionsIsAfter0 == False:
                    XPOS = PreFinal_XPOS.replace("0x", "").upper()
                else:
                    if Current_XPOS >= 16:
                        XPOS = PreFinal_XPOS.replace("0x", "00").upper()
                    elif Current_XPOS <= 16:
                        XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                    else:    
                        XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
            elif Current_XPOS >= NegativeToPositive_Position:
                Current_XPOS -= 65536
                PreFinal_XPOS = hex(abs(Current_XPOS))
                if Current_XPOS >= 16:
                    XPOS = PreFinal_XPOS.replace("0x", "00").upper()
                elif Current_XPOS <= 16:
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                else:    
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                PositionsIsAfter0 = True
            else:
                PositionsIsAfter0 = True                                           
                Current_XPOS -= 65536
                PreFinal_XPOS = hex(abs(Current_XPOS))
                if Current_XPOS >= 16:
                    XPOS = PreFinal_XPOS.replace("0x", "00").upper()
                if Current_XPOS <= 16:
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
                else:    
                    XPOS =  PreFinal_XPOS.replace("0x", "000").upper()
            if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                CharacterWidth = '09'
            elif CharacterOfTitleCard == 'i':
                CharacterWidth = '01'
            else:
                CharacterWidth = '05'
            if CharacterOfTitleCard in CharactersList:
                x = CharactersList.index(CharacterOfTitleCard) 
                output.insert(END,f'{SavedIndexes[x]}, ${XPOS} ; {CharacterOfTitleCard.upper()} \n')
                if CharacterOfTitleCard == 'i':
                   LetterIsAfterI = True 
                   LetterIsAfterIcount = 3
                   LetterIsAfterIposcount = 1
                if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':
                   LetterIsAfterM = True 
                   LetterIsAfterMcount = 3
                   LetterIsAfterMposcount = 1
                if export == True: 
                    f.write(f'{SavedIndexes[x]} ${XPOS} ; {CharacterOfTitleCard.upper()}')
                    f.write('\n')
                print(f'{SavedIndexes[x]} ${XPOS} ; {CharacterOfTitleCard.upper()}')
            else:
                if CharacterOfTitleCard != 'z' and CharacterOfTitleCard != 'o' and CharacterOfTitleCard != 'n' and CharacterOfTitleCard != 'e' and CharacterOfTitleCard != ' ' and CharacterOfTitleCard.isalpha():  
                    CurrentCharacter += 1 
                    FinalIndex_Dec = int(Current_Index)+int(Index_Increment)
                    if LetterIsAfterI == True:
                        FinalIndex_Dec -= 2                 
                    Index2Hex = hex(FinalIndex_Dec)
                    INDEX = Index2Hex.replace("0x", "").upper()
                    TwoPlayerFinalIndex = int(Current_2PIndex)+int(Index_Increment_2P)
                    TwoPlayerFinalIndex_REGEX_STEP = hex(TwoPlayerFinalIndex) 
                    INDEX2P = TwoPlayerFinalIndex_REGEX_STEP.replace("0x", "").upper()
                    CodeToOutput = (f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}')
                    CodeForSavedIndexes = (f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P},')
                    if LetterIsAfterI == True:
                        FinalIndex_Dec += 2 
                        if CharacterOfTitleCard == "m":
                            FinalIndex_Dec += 2  
                    SavedIndexes.append(CodeForSavedIndexes)   
                    if export == True: 
                        f.write(CodeToOutput)
                        f.write('\n')
                    print(CodeToOutput)
                    CharactersList.append(CharacterOfTitleCard)
                    Current_Index = FinalIndex_Dec
                    Current_2PIndex = TwoPlayerFinalIndex
                    if CharacterOfTitleCard == 'i':
                       LetterIsAfterI = True 
                       LetterIsAfterIcount = 3
                       LetterIsAfterIposcount = 1                                                                                                           
                    if CharacterOfTitleCard == 'm' or CharacterOfTitleCard == 'w':

                       LetterIsAfterM = True 
                       LetterIsAfterMcount = 3
                       LetterIsAfterMposcount = 1                                           
                elif CharacterOfTitleCard == 'z':
                    INDEX = '58C'
                    INDEX2P = '2C6'
                    if export == True:
                        f.write(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}' )
                        f.write('\n')
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1                    
                    print(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}')                    
                elif CharacterOfTitleCard == 'o':
                    INDEX = '588'
                    INDEX2P = '2C4'
                    if export == True:
                        f.write(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}' )
                        f.write('\n')
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1                     
                    print(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}')                              
                elif CharacterOfTitleCard == 'n':
                    INDEX = '584'
                    INDEX2P = '2C2'
                    if export == True:
                        f.write(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}' ) 
                        f.write('\n')
                    
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1                         
                    print(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}')               
                elif CharacterOfTitleCard == 'e':
                    INDEX = '580'
                    INDEX2P = '2C0'
                    if export == True:
                        f.write(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}' )
                        f.write('\n') 
                    if LetterIsAfterI == True:
                       LetterIsAfterIcount += 1
                    if LetterIsAfterM == True:
                       LetterIsAfterMcount += 1
                    print(f'\tdc.w $00{CharacterWidth}, $8{INDEX}, $8{INDEX2P}, ${XPOS} ; {CharacterOfTitleCard.upper()}')           
                elif CharacterOfTitleCard == ' ':
                    if export == True:
                        f.write('\n')
                    Current_XPOS += 2
                    print('\n')                 
                else:
                     pass
        TitlecardLettersToLoad = sub(r"[^a-zA-Z,' ']", "", text).upper()          
        if export == True:
            f.write(f'In Off_TitleCardLetters\ntitleLetters	"{TitlecardLettersToLoad}" make sure you have no special characters here though.\nIf you are using the 2007 Xenowhirl disasm, read Xenowhirl_Setup.txt, and use the letter macros, and skip Z, O, N, & E')
        print(f'In Off_TitleCardLetters\ntitleLetters	"{TitlecardLettersToLoad}" make sure you have no special characters here though.\nIf you are using the 2007 Xenowhirl disasm, read Xenowhirl_Setup.txt, and use the letter macros, and skip Z, O, N, & E')
        if DebugFlag == True:
            if export == True:
                f.write(f';Indexes: {CharactersList} {len(CharactersList)}\n;Code for above indexes:{SavedIndexes}\n\t;But you can\'t stick n move')  
                f.write('\n')
            print(';Indexes: {CharactersList} {len(CharactersList)}\n;Code for above indexes:{SavedIndexes}\n\t;But you can\'t stick n move')     
        if len(SavedIndexes) > 8:
            if export == True:
                f.write(';You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            print('You can only have $8 unique indexes excluding Z,O,N, and E, this code will not work')
            if export == True:
                f.write('\n')
        if len(LENGTH_STEP) > 16:
            if export == True:
                f.write(';You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
            print('You can only have a maximum of $10 characters in sonic 2 title cards, this code will not work')
            if export == True:
                f.write('\n')
        if PositionsIsAfter0 == True and Current_XPOS >= 112:
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
    exit(0)
GenerateTitlecardFromText() #run the code
