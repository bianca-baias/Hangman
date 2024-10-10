import json

# Based on my counting function, I estimated that the following are the most common letters, in descending order
#vowels = ['i', 'e', 'a', 'o', 'u', 'ă', 'â' , 'î']
#consonants = ['r', 'l', 't', 'n', 'c', 's', 'm', 'd', 'p', 'g', 'b', 'f', 'v', 'z', 'h', 'ș', 'ț', 'j', 'k', 'x', 'q', 'w', 'y']

def read_file(filename):
    """
    Function to read a file and get every line as a value in a new list.
    """
    # Mention encoding to get rid of the extra "ï»¿" from the begining of the file;
    with open(filename, 'r', encoding='utf-8-sig') as file:
        words = file.readlines()
    return words


def check_vowels(word, vowels):
    """
    Input:
    - word (list): word[0] (str - id of the game), word[1] (str: partial word), word[2] (str: the complete word)
    
    Output:
    - guess_word (list): partial word after vowel guessing
    - trials (int): number of vowel trials for this word
    """
    
    trials = 0
    guess_word = list(word[1])
    
    for vowel in vowels:
        if vowel not in word[1].lower():
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


def check_consonants(word, consonants):
    """
    Input:
    - word (list): word[0] (str - id of the game), word[1] (list: the word after vowel guessing), word[2] (str: the complete word)
    
    Output:
    - trials (int): number of consonants trials for this word
    """
    
    trials = 0
    guess_word = word[1]
    
    for cons in consonants:
        if cons not in word[1]:
            trials += 1
            
            if cons in word[2].lower():
                indexes =  [i for i, letter in enumerate(word[2]) if letter.lower() == cons]
                #print(f"indexes for letter {cons}: {indexes}")
                for index in indexes:
                    guess_word[index] = cons.upper()
            
            as_string = ''.join(str(x) for x in guess_word)
            
            if as_string == word[2]:
                break
        
    return trials
    


def hangman(word, vowels, consonants):
    """
    Input:
    - word (list): word[0] (str - id of the game), word[1] (str: partial word), word[2] (str: the complete word)
    
    Output:
    - trials_v + trials_c (int): number of trials for both vowels and consonants
    """
    
    word[1], trials_v = check_vowels(word, vowels)
    
    trials_c = check_consonants(word, consonants)
    
    return trials_v + trials_c


def counting(words):
    """
    Counting function to check the most frequent letters in our dictionary. This will be the order of the letters to check in our game.
    Input:
    - words (list): list of all the games in our input file
    
    Output:
    - Will write the letters to a file, in descending order of apparition in our ditionary
    - sorted_by_values (dict): a dictionary containing the letters in descending order of apparition in our input dictionary
    """
    
    alphabet = "aăâbcdefghiîjklmnopqrsștțuvwxyz"
    result = {'a': 0, 'ă':0, 'â': 0, 'î': 0, 'ș': 0, 'ț': 0, 'b':0, 'c':0, 'd': 0, 'e': 0, 'f':0, 'g':0, "h":0, 'i':0, 'j':0, 'k':0, 'l':0,
                'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}
    complete_words = []
    
    # Get a list with only the complete words
    for word in words:
        # Get rid of the newline character at the end of the line
        new = word.strip("\n")
        word = new.split(";")
        complete_words.append(word[2])
    
    # For every word, count the appearace of every letter
    for word in complete_words:
        for ch in alphabet:
            as_list = list(word)
            result[ch] += as_list.count(ch.upper())
    
    sorted_by_values = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    
    # Optionally, write the result to a file
    with open("text.txt", 'w') as file:
        file.write(json.dumps(sorted_by_values))
    
    return sorted_by_values


def get_vowels_and_consonants(alphabet):
    """
    Separates the vowels and consonants, and appends them to a list ordered by their frequency.
    Input:
    - alphabet (dict): a dictionary containing all the alphabet letters, but ordered descending by their frequency in our dictionary.
    
    Output:
    - vowels (list): list of vowels in descending order
    - consonants (list): list of consonants in descending order
    """
    
    list_of_vowels = "aeiouăâî"
    vowels = []
    consonants = []
    
    for letter in alphabet.keys():
        if letter in list_of_vowels:
            vowels.append(letter)
        else:
            consonants.append(letter)
    
    return vowels, consonants


def main():
    words = read_file("cuvinte_de_verificat.txt")
    results = {}
    total = 0
    
    alphabet_order = counting(words)
    vowels, consonants = get_vowels_and_consonants(alphabet_order)
    
    for word in words:
        # Get rid of the newline character at the end of the line and separate the string by ';'
        new = word.strip("\n")
        word = new.split(";")
        
        # Call the hangman function and get the trials it took to guess it
        results[word[0]] = hangman(word, vowels, consonants)
    
    for trial in results.values():
        total += trial
    print(total)
    
main()