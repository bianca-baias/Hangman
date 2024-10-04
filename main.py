import json

# Based on my counting function, I estimated that the following are the most common letters, in descending order
vowels = ['i', 'e', 'a', 'o', 'u', 'ă', 'â' , 'î']
consonants = ['r', 'l', 't', 'n', 'c', 's', 'm', 'd', 'p', 'g', 'b', 'f', 'v', 'z', 'h', 'ș', 'ț', 'j', 'k', 'x', 'q', 'w', 'y']

def read_file(filename):
    """
    Function to read a file and get every line as a value in a new list.
    """
    # Mention encoding to get rid of the extra "ï»¿" from the begining of the file;
    with open(filename, 'r', encoding='utf-8-sig') as file:
        words = file.readlines()
    return words


def check_vowels(word):
    """
    """
    trials = 0
    guess_word = list(word[1])
    
    for vowel in vowels:
        trials += 1
        if vowel in word[2].lower():
            indexes =  [i for i, letter in enumerate(word[2]) if letter.lower() == vowel]
            #print(f"indexes for letter {vowel}: {indexes}")
            for index in indexes:
                guess_word[index] = vowel.upper()
        
        as_string = ''.join(str(x) for x in guess_word)
        
        if as_string == word[2]:
            break
        
    return guess_word, trials


def check_consonants(word):
    """
    """
    
    trials = 0
    guess_word = word[1]
    
    for cons in consonants:
        trials += 1
        if cons in word[2].lower():
            indexes =  [i for i, letter in enumerate(word[2]) if letter.lower() == cons]
            #print(f"indexes for letter {cons}: {indexes}")
            for index in indexes:
                guess_word[index] = cons.upper()
        
        as_string = ''.join(str(x) for x in guess_word)
        
        if as_string == word[2]:
            break
        
    return as_string, trials
    


def hangman(word):
    """
    Cod: word[0]
    Guess: word[1]
    Correct: word[2]
    - trials (int): number of times used to guess the word;
    """
    cuvinte = []
    word[1], trials_v = check_vowels(word)
    
    cuv, trials_c = check_consonants(word)
    cuvinte.append(cuv)
    
    
    return cuvinte, trials_v + trials_c


def numarare(cuvinte):
    
    alfabet = "aăâbcdefghiîjklmnopqrsștțuvwxyz"
    rezultat = {'a': 0, 'ă':0, 'â': 0, 'î': 0, 'ș': 0, 'ț': 0, 'b':0, 'c':0, 'd': 0, 'e': 0, 'f':0, 'g':0, "h":0, 'i':0, 'j':0, 'k':0, 'l':0,
                'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}
    
    for word in cuvinte:
        for ch in alfabet:
            cv = list(word[0])
            rezultat[ch] += cv.count(ch.upper())
        
    sorted_by_values = dict(sorted(rezultat.items(), key=lambda item: item[1], reverse=True))
    with open("text.txt", 'w') as file:
        file.write(json.dumps(sorted_by_values))


def main():
    words = read_file("cuvinte_de_verificat.txt")
    results = {}
    total = 0
    cuvinte = []
    for word in words:
        # Get rid of the newline character at the end of the line
        new = word.strip("\n")
        word = new.split(";")
        cuvint, results[word[0]] = hangman(word)
        cuvinte.append(cuvint)
    
    numarare(cuvinte)
    
    for trial in results.values():
        total += trial
    print(total)
    
main()