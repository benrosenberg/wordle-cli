# wordle implementation

import random
import re

# six tries to get 5-letter word 

with open('words_alpha.txt', 'r') as f:
    all_words = [l[:-1] for l in f.readlines()]

with open('5k.txt', 'r') as f: # source: https://github.com/mahsu/IndexingExercise/blob/master/5000-words.txt
    common_words = [l[:-1] for l in f.readlines()]

five_letters = [w for w in common_words if len(w) == 5 and w[0].islower()] # contains \n at the end

# print(len(five_letters)) # 832

word = random.choice(five_letters).upper()

def valid(attempt):
    attempt = attempt.lower()
    if attempt in all_words and len(attempt) == 5:
        return True
    elif attempt in all_words:
        return 'Too short' if len(attempt) < 5 else 'Too long'
    else:
        return 'Not in dictionary'

def result(attempt, word):
    attempt = attempt.upper()
    if attempt == word:
        print('Correct!')
        return True
    if (validity := valid(attempt)) != True:
        print(validity)
        return False
    # out_list = [
    #     'X', # CORRECT LOCATION
    #     'O', # INCORRECT LOCATION
    #     '_'  # NOT IN WORD
    # ]
    out = ''
    letter_counts = {l:([0,0],word.count(l)) for l in set(attempt)}
    for i,letter in enumerate(attempt):
        if word.count(letter) > 0:
            if word.find(letter,i) == attempt.find(letter,i):
                out += 'X'
                letter_counts[letter][0][0] += 1 # correct place
            else:
                out += 'O'
                letter_counts[letter][0][1] += 1 # incorrect place
        else:
            out += '_'

    for letter,counts in letter_counts.items():
        if sum(counts[0]) <= counts[1]:
            continue # no issues possible
        if sum(counts[0]) > counts[1]:
            # print(f'issue with letter {letter}')
            # THERE IS AN ISSUE. This should not be possible.
            temp = list(out)
            diff = sum(counts[0]) - counts[1]
            # print(f'diff of {diff}')
            word_indices = [i for i,l in enumerate(word) if l == letter]
            attempt_indices = [i for i,l in enumerate(attempt) if l == letter]
            # print(word_indices)
            # print(attempt_indices)
            # go backwards and remove relevant stuff
            pointer = len(attempt) - 1
            while diff > 0 and pointer >= 0:
                # print(pointer, temp)
                if pointer in attempt_indices:
                    if pointer not in word_indices:
                        temp[pointer] = '_'
                        diff -= 1
                pointer -= 1
            out = ''.join(temp)
        

    return '  ' + out

# attempt = 'TOOTS'
# word =    'ALOOF'

# print(result(attempt, word))

def kb_render(used_letters, word, attempts):
    word = word.upper()
    used_letters = [u.upper() for u in used_letters]
    for i,a in enumerate(attempts):
        attempts[i] = a.upper()

    keyboard = '''
               Q W E R T Y U I O P
                A S D F G H J K L
                 Z X C V B N M
               '''
    blank = re.sub(r"[A-Z]", "?", keyboard)

    for letter in used_letters:
        if letter not in word:
            idx = keyboard.index(letter)
            blank = blank[:idx] + '_' + blank[idx+1:]
    
    for letter in used_letters:
        # check for incorrectly-positioned letters
        if letter in word:
            positions_of_letter = [a.find(letter) for a in attempts if a.find(letter) != -1]
            indices_in_word = [i for i,l in enumerate(word) if l == letter]
            if len(set(indices_in_word) & set(positions_of_letter)) == 0:
                idx = keyboard.index(letter)
                blank = blank[:idx] + letter.lower() + blank[idx+1:] # make letters with incorrect location lowercase
            else:
                idx = keyboard.index(letter)
                blank = blank[:idx] + letter + blank[idx+1:]

    return blank


tries = 0
got_it = False 
used_letters = set()
attempts = []
while tries < 6:
    tries += 1
    attempt = input('> ')
    out = result(attempt, word)
    if out == True:
        if tries == 1:
            print(f'It only took you one try!')    
        else:
            print(f'It only took you {tries} tries.')
        break
    elif out == False:
        tries -= 1 # don't use up a try
        continue
    else:
        used_letters |= set(attempt)
        attempts.append(attempt)
        print(out)
        print(kb_render(used_letters, word, attempts))
else:
    print(f'Too bad, you didn\'t get it.\nThe word was {word}.')
