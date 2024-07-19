secretWord = "Indonesia"
guessed_letters = []
chances = 6
while chances > 0:
 guess = input("Guess a letter in my secret word: ")
 if len(guess) != 1:
    print("Please give me one letter.")
 elif not guess.isalpha():
    print("Please give me a letter.")
 elif guess.lower() in guessed_letters:
    print("You already guessed that letter.")
 else:
    guessed_letters.append(guess.lower())
 if guess.lower() in secretWord.lower():
    print("Congrats, you guessed a letter!")
 else:
    chances -= 1
    print("Better luck next time. You have {} chances left.".format(chances))