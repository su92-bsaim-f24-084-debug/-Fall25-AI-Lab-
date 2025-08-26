import getpass

print("Welcome to \"Hangman Game\"!")
while True:
    print('If you dont want to play the game just enter Q in name of Player 1')
    print("Player 1 will give the secret word.")
    print("Player 2 will guess the word.")

    p1 = input("Please Enter the name of Player1: ")
    if p1.lower() == 'q':
        print("Game Terminated.")
        exit()

    p2 = input("Please Enter the name of Player2: ")
    secret_word = getpass.getpass(f"The Word will not appear.\nNow {p1} will enter the secret word: ")
    secret_word = secret_word.lower()

    lives = 6
    w_g = []
    blanks = "_" * len(secret_word)

    while lives > 0 and '_' in blanks:
        print(f"\nWord = {blanks} :::::: Lives remaining = {lives}")
        print(f"Wrong guessed alphabets: {w_g}")

        guess = input(f"{p2} Please enter the guess: ")

        if not guess.isalpha() or len(guess) != 1:
            print("Wrong input!!!\nOnly Enter a single alphabet")
            continue

        if guess in blanks or guess in w_g:
            print("You have already guessed that alphabet.")
            continue

        if guess in secret_word:
            for i in range(len(secret_word)):
                if guess == secret_word[i]:
                    l1 = list(blanks)
                    l1[i] = guess
                    blanks = "".join(l1)
            print("Nice! You guessed right.")
        else:
            w_g.append(guess)
            lives -= 1
            print("Wrong Guess...")

    # Game result
    if '_' not in blanks:
        print(f"\n Congratulations {p2}!!! You won with {lives} lives left. The word was '{secret_word}'.")
    else:
        print(f"\n You failed to guess the word. The correct word was '{secret_word}'.")
