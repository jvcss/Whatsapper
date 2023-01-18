import re

def compara_com_emoji_fix(parte):
    map_emojis = {'zero': '0⃣' , 'one': '1⃣', 'one-thirty': '🕜'}
    OUTPUT = []
    done = False
    while not done:
        if ( re.search(r'\S+', parte) ):
            match = re.search(r'\S+', parte)
            common_string = match.group()

            #adiciona ao OUT e tira do parte
            emoji = [key for key, value in map_emojis.items() if value == match.group()]
            if (emoji):
                OUTPUT.append([key for key, value in map_emojis.items() if value == match.group()][0])
            else:
                OUTPUT.append(common_string)
            parte = re.sub(match.group(), '', parte,count=1)
        else:
            done = True
    return OUTPUT

#parte = ' 0⃣ 62 9 9918-4004 1⃣ 62 3091-7324'
#map_emojis = compara_com_emoji_fix(parte)
#print(map_emojis)
#['zero', '62', '9', '9918-4004', 'one', '62', '3091-7324']