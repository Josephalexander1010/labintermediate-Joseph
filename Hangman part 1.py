def main ():
    secret = "word"
    guess = "_" *len(secret)
    correct = []
    print ("The word have",len(secret),"letters")

    while True:
        print ("Guess this",guess)
        letter = input("Guess the letter !").lower()
        if letter in secret:
            correct.append(letter)
            newguess = ""
            for i in range(len(secret)):
                if secret[i] == letter:
                    newguess += letter
                else:
                    newguess += guess[i]
            guess = newguess
            print("You have guessed the letter")
            if "_" not in guess:
                print("You have guessed the word =",secret)
                break
        elif not letter.isalpha():
            print("Please input a letter")
        else:
            print("You have not guessed the letter")

main() 