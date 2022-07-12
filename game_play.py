import sys
from statistics import mode, mean, median

sys.path.append("five-letter-words")
from get_words import get_words
import random
import word_matcher as wm
import wordlist as wl

# print(get_words())


def main():
    while True:
        game_options = """Choose from the following:
        1) Regular play
        2) Guided play
        3) Solver for another game
        4) Automatic play--one game
        5) Automatic play--multiple games
        X) Exit

        """
        # TODO: change var to `game_type` here or `game_choice` below.
        game_choice = input(game_options)
        if game_choice.lower() == "x":
            print("bye!")
            quit()

        try:
            if int(game_choice) == 1:  # Normal play
                game_play(1, word_source=wm.FLW)
            elif int(game_choice) == 2:  # Guided play
                game_play(2, word_source=wm.FLW)
            elif int(game_choice) == 3:  # solver for another game
                game_play(3, word_source=wm.FLW)
            elif int(game_choice) == 4:  # one-time self-solver
                game_play(4, word_source=wm.FLW)
            elif int(game_choice) == 5:  # multiple self-solver
                number_of_tries = int(input("how many tries? "))
                game_results = autoplay(number_of_tries)
                _mea, _min, _max, _mdn, _mde = simple_stats(
                    [len(r["guesses"]) for r in game_results]
                )
                print(f"Solved {number_of_tries} games on average in {_mea} tries")
                print(f"minimum tries: {_min}")
                print(f"maximum tries: {_max}")
                print(f"median tries: {_mdn}")
                print(f"mode tries: {_mde}")
            else:
                raise
        except:
            print("boo hoo. try typing 1, 2, 3, 4, or 5.")


def autoplay(
    number_of_tries,
    game_type=4,
    answer_list=None,
    word_source=wm.FLW,
    choice_method="random",
    silent=True,
):
    # TODO: get this argument order consistent with `game_play`
    all_results = []
    if not answer_list:
        answer_list = [None] * number_of_tries
    for i in range(number_of_tries):
        all_results.append(
            game_play(game_type, answer_list[i], word_source, choice_method, silent)
        )
    return all_results


def simple_stats(nums):
    # _mea = sum(nums) / len(nums)
    _mea = mean(nums)
    _min = min(nums)
    _max = max(nums)
    _mdn = median(nums)
    _mde = mode(nums)
    return _mea, _min, _max, _mdn, _mde


def game_play(
    game_type=None,
    answer=None,
    word_source=wm.BWL,
    choice_method="random",
    silent=False,
):
    if word_source == wm.BWL:
        all_words = wl.wordlist
    if word_source == wm.FLW:
        all_words = get_words()
    # TODO: write a web scraper
    results = {}
    if not answer:
        answer = random.choice(all_words).lower()  # Just in case, pun intended
    results["answer"] = answer
    if not silent:
        print(answer)

    still_guessing = True
    remaining_word_list = all_words
    while still_guessing:
        if not game_type == 4:
            while True:
                guess = input("Enter guess: ").lower()
                if len(guess) != 5:
                    print("Must be 5 letters!")
                else:
                    break
        elif game_type == 4:
            guess = choose_new_word(remaining_word_list, choice_method)
        results = wm.guess_game(guess, results)
        if not silent:
            print(results)
        if not silent:
            show_results(results, game_type)
        # if not silent:
        # show_remaining_letters(results["eliminated_letters"])
        if results["guesses"][guess][0] == [0, 1, 2, 3, 4]:
            if not silent:
                print("You WON!!!!\n")
            still_guessing = False
        else:
            if not silent:
                show_eliminated_letters(results["eliminated_letters"])
            if game_type in (2, 4):
                remaining_word_list = remaining_words(
                    remaining_word_list,
                    guess,
                    results["guesses"][guess][0],
                    results["guesses"][guess][1],
                    results["eliminated_letters"],
                    results["double_letters"],
                )
                if game_type == 2:
                    show_remaining(remaining_word_list)
    return results


def show_results(results=None, game_type=1):
    for g, wr in results["guesses"].items():
        show_positions(g, *wr)


# show_positions(guess, *results["guesses"][guess])
def show_positions(guess, rightpos, wrongpos):
    # print(guess, rightpos, wrongpos)
    display = ""
    for i, l in enumerate(guess):
        if i not in (set(rightpos) | set(wrongpos)):
            _l = "_"
        elif i in rightpos:
            _l = l.upper()
        else:
            _l = l

        display += _l

    print(guess + ": " + " ".join(display) + " ")


def remaining_words(
    all_words, guess, rightpos, wrongpos, eliminated, max_repeat_letters
):
    rw = wm.remaining_eliminated(all_words, eliminated)
    rw = wm.remaining_rightpos(rw, guess, rightpos)
    rw = wm.remaining_wrongpos(rw, guess, wrongpos)
    rw = wm.remaining_repeated(rw, max_repeat_letters)
    return list(rw)


def show_eliminated_letters(eliminated):
    print(f"eliminated letters are: " + " ".join(eliminated))
    # TODO: ADD function to show correct, wrongpos, and unguessed letters


def show_remaining(remaining_word_list):
    print(f"there are {len(remaining_word_list)} possible answer words remaining.")
    verbose = input("do you want to see them? (<no> yes): ")
    if not verbose or verbose == "no":
        pass
    else:
        print("\n".join(remaining_word_list))


def choose_new_word(word_list, choice_method):
    if choice_method == "random":
        return random.choice(word_list).lower()  # Just in case, pun intended


if __name__ == "__main__":
    main()
