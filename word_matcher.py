import random
from itertools import chain
import string

LETTERS = string.ascii_lowercase
FLW = "five_letter_words"
OWL = "wordle_official_answer_list"
BWL = "built_in_word_list"


def list_maker(n, l=5):
    return [("".join(random.choice(LETTERS) for _l in range(l))) for _n in range(n)]


def rightpos_check(guess, answer):
    return [
        _i
        for _i in range(max(len(guess), len(answer)))
        if ord(guess[_i]) ^ ord(answer[_i]) == 0
    ]


def wrongpos_check(guess, answer, rightpos=None):
    if not rightpos:
        rightpos = rightpos_check(guess, answer)
    wrongpos = []
    answer_remain = []
    guess_remain = []
    for _i, _l in enumerate(answer):
        if _i in rightpos:
            answer_remain.append("&")  # TODO: make this a null character
            guess_remain.append("%")  # NOTE: if these are the same, use test below
        else:
            answer_remain.append(_l)
            guess_remain.append(guess[_i])

    for _i, _gl in enumerate(guess_remain):
        if _gl in answer_remain:
            if True:
                # if answer_remain[_i] != _gl:  # NOTE: Use this test if replace characters are the same
                if _gl not in guess_remain[:_i]:
                    wrongpos.append(_i)
                elif guess_remain[:_i].count(_gl) < answer_remain.count(_gl):
                    wrongpos.append(_i)
    return wrongpos


def new_double_letter_check(guess, rightpos, wrongpos):
    allrightpos = set(chain(wrongpos, rightpos))
    rightletters = list([guess[i] for i in allrightpos])
    max_repeat_letters = {}
    for _i, _l in enumerate(rightletters):
        _c = guess.count(_l)
        _c2 = rightletters.count(_l)
        if _c > _c2:
            max_repeat_letters[_l] = _c2
    return max_repeat_letters


def double_letter_aggregate(new, prev={}):
    return prev.update(new)


def position_check(guess, answer):
    rightpos = rightpos_check(guess, answer)
    wrongpos = wrongpos_check(guess, answer, rightpos)
    return guess, rightpos, wrongpos


def eliminated_letters(currlist, guess, rightpos, wrongpos):
    return set(currlist) | new_eliminated_letters(guess, rightpos, wrongpos)


def new_eliminated_letters(guess, rightpos, wrongpos):
    allrightpos = set(chain(wrongpos, rightpos))
    rightletters = set([guess[i] for i in allrightpos])
    wrongletters = set(guess) - rightletters
    return wrongletters


def check_all(guess, answer):
    _, rightpos, wrongpos = position_check(guess, answer)
    double_letters = new_double_letter_check(guess, rightpos, wrongpos)
    eliminated_letters = new_eliminated_letters(guess, rightpos, wrongpos)
    return rightpos, wrongpos, double_letters, eliminated_letters


def guess_game(new_guess, results=None):
    new_results = {}
    if not results:
        results = {}
    answer = results.get("answer")
    if not answer:
        raise Exception(
            "No answer in results dictionary. The guessing game must know the answer!"
        )
        # TODO: STOP!!!!!!
    double_letters = results.get("double_letters")
    eliminated_letters = results.get("eliminated_letters")
    guesses = results.get("guesses")
    if not double_letters:
        double_letters = {}
    if not eliminated_letters:
        eliminated_letters = set()
    if not guesses:
        guesses = {}
        new_results["guesses"] = {}
    _r, _w, _d, _e = check_all(new_guess, answer)
    _d.update(double_letters)  # _d |= would be the best way
    _e = _e | eliminated_letters  # _e |= would be the best way
    new_results["eliminated_letters"] = _e
    new_results["double_letters"] = _d
    new_results["guesses"] = guesses
    new_results["guesses"][new_guess] = (_r, _w)
    new_results["answer"] = answer
    return new_results


def remaining_eliminated(wordlist, x_letters=None):
    if x_letters:
        return [w for w in wordlist if (set() == (set(w) & set(x_letters)))]
    else:
        return wordlist


def remaining_repeated(wordlist, repeated_letters=None):
    if repeated_letters:
        d = {}
        for l in repeated_letters:
            d[l] = {w for w in wordlist if (letter_count(w, l) <= repeated_letters[l])}
        # TODO -- this has to be super inefficient to loop through the iterators twice
        # TODO -- not only that, but we'll do this calculation lots of extra times across
        # the game.
        # Start somewhere
        r = d[l]
        for l in repeated_letters:
            r = r.intersection(d[l])
        return r
    else:
        return wordlist


def remaining_wrongpos_dict(wordlist, guess=None, wrongpos=None, strict=False):
    # TODO: This needs to wrap a pair of functions that do the filtering for just one letter
    # TODO: Convert this to use yield or some form of map and lambda
    remaining_words = {}
    for pos in wrongpos:
        wrongletter = guess[pos]
        key = ("wrongpos", wrongletter, pos)
        remaining_words[key] = {
            w for w in wordlist if wrongletter in w[:pos] + w[pos + 1 :]
        }
        if strict:
            remaining_words[key] = {
                w for w in remaining_words[key] if w[pos : pos + 1] == wrongletter
            } ^ remaining_words[key]

    return remaining_words


def remaining_dict_crush(word_dict):
    wpdl = list(word_dict.values())
    return wpdl[0].intersection(*wpdl)


def remaining_wrongpos(wordlist, guess=None, wrongpos=None, strict=False):
    """
    Return, from a starting wordlist, only words that have the letter from the guess
    at least somewhere besides the indicated 'wrong' position.

    With 'strict', a word containing the letter somewhere else AND in the wrong position
    will be eliminated (i.e., if it has a double of the given letter and one of the
    doubles is in the position that has been eliminated.)
    """
    if not guess:
        raise Exception("Cannot determine remaining words without a guess")

    if not wrongpos:
        return wordlist

    wpd = remaining_wrongpos_dict(wordlist, guess, wrongpos, strict)
    return remaining_dict_crush(wpd)


def remaining_rightpos_dict(wordlist, guess=None, rightpos=None):
    # TODO: This needs to wrap a pair of functions that do the filtering for just one letter
    # TODO: Convert this to use yield or some form of map and lambda
    remaining_words = {}
    for pos in rightpos:
        rightletter = guess[pos]
        key = ("rightpos", rightletter, pos)
        remaining_words[key] = {w for w in wordlist if w[pos : pos + 1] == rightletter}

    return remaining_words


def remaining_rightpos(wordlist, guess=None, rightpos=None):
    """
    Return, from a starting wordlist, only words that have the letter from the guess
    exactly in the 'right' position.
    """
    if not guess:
        raise Exception("Cannot determine remaining words without a guess")

    if not rightpos:
        return wordlist

    wpd = remaining_rightpos_dict(wordlist, guess, rightpos)
    return remaining_dict_crush(wpd)


def letter_count(word=None, letter=None):
    """Return the number of times a particular letter shows up in a string.
    Found this on https://www.geeksforgeeks.org/python-count-occurrences-of-a-character-in-string/
    """
    # TODO: This count could be a property of the wordlist -- each word could have an associated
    # count dictionary that would very quickly be compared to the repeated letter filter.
    # TODO: Add flag to permit case-sensitivity
    if word and letter:
        # using lambda + sum() + map() to get count
        # counting e
        return sum(map(lambda x: 1 if letter.lower() in x else 0, word.lower()))
    else:
        return 0


def remaining(guess, wordlist, rightpos=None, wrongpos=None, x_letters=None):
    if not rightpos:
        rightpos = []
    if not wrongpos:
        wrongpos = []

    remains = []
    # for word in wordlist:
    # if
    # remains.append(word)

    return remains


def possible_matches(guess, wordlist):
    """returns the set of all words sharing at least one letter with the guessed word"""
    s_g = set(guess)
    r = []
    for w in wordlist:
        if not (set() == (set(w) & s_g)):
            r.append(w)
    return r


if __name__ == "__main__":
    wl = list_maker(10)
    print(wl)

    print(xor_two_str(wl[1], wl[2]))
    print(position_check(wl[1], wl[2]))
