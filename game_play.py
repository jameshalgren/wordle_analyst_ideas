import sys

sys.path.append("five-letter-words")
from get_words import get_words
import random
import word_matcher as wm

# print(get_words())


def main():
    while True:
        game_options = """Choose from the following:
        1) Regular play
        2) Guided play
        3) Solver
        X) Exit

        """
        game_choice = input(game_options)
        if game_choice.lower() == "x":
            print("bye!")
            quit()
        elif int(game_choice) == 1:  # Normal play
            game_play(1)
        elif int(game_choice) == 2:  # Guided play
            game_play(2)
        elif int(game_choice) == 3:  # Solver for another game
            game_play(3)
        else:
            print("boo hoo. try typing 1, 2, or 3.")


def game_play(game_type=None):
    all_words = get_words()
    results = {}
    answer = random.choice(all_words)
    results["answer"] = answer
    print(answer)

    still_guessing = 1
    while still_guessing == 1:
        while True:
            guess = input("Enter guess: ")
            if len(guess) != 5:
                print("Must be 5 letters!")
            else:
                break
        results = wm.guess_game(guess, results)
        print(results)
        if results["guesses"][guess][0] == [0, 1, 2, 3, 4]:
            print("You WON!!!!")
            still_guessing = 0


if __name__ == "__main__":
    main()
