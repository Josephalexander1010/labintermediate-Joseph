def get_secret_word():  
    return "indo"  

def main():
    secret_word = get_secret_word()  
    guessed_letters = []
    chances = 5

    while chances > 0:
        print("Word:", ''.join([letter if letter in guessed_letters else '_' for letter in secret_word]))
        guess = input("Guess a letter in my secret word: ")
        if len(guess) != 1:
            print("Please give me one letter.")
        elif not guess.isalpha():
            print("Please give me a letter.")
        elif guess.lower() in guessed_letters:  
            print("You already guessed that letter.")
        else:
            guessed_letters.append(guess)
            if guess.lower() in secret_word.lower():  
                print("Congrats, you guessed a letter!")
                if all(letter in guessed_letters for letter in secret_word):  
                    print("Congratulations! Correct!")
                    break  
            else:
                chances -= 1
                print("Better luck next time. You have {} chances left.".format(chances))

    if chances == 0:
        print("Sorry, The word was:", secret_word)

main()
