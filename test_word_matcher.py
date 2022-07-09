import pytest
from word_matcher import (
    list_maker,
    remaining,
    remaining_eliminated,
    remaining_repeated,
    remaining_wrongpos,
    remaining_wrongpos_dict,
    remaining_dict_crush,
    remaining_rightpos,
    remaining_rightpos_dict,
    new_eliminated_letters,
    new_double_letter_check,
    eliminated_letters,
    position_check,
    possible_matches,
    letter_count,
    check_all,
    guess_game,
)
from wordlist import wordlist


def test_list_maker():
    assert isinstance(list_maker(0), list)


def test_position_check():
    guess = "guers"
    answer = "answe"
    assert position_check(guess, answer) == ("guers", [], [2, 4])

    guess = "segus"
    answer = "ansse"
    assert position_check(guess, answer) == ("segus", [], [0, 1, 4])

    guess = "gsuse"
    answer = "ansse"
    assert position_check(guess, answer) == ("gsuse", [3, 4], [1])

    guess = "lllssl"
    answer = "lqqlll"
    assert position_check(guess, answer) == ("lllssl", [0, 5], [1, 2])

    # Prefer a rightly positioned letter multiple over a wrongly positioned one
    guess = "llllsl"
    answer = "lqqlll"
    assert position_check(guess, answer) == ("llllsl", [0, 3, 5], [1])

    guess = "llsssl"
    answer = "lqqlll"
    assert position_check(guess, answer) == ("llsssl", [0, 5], [1])

    guess = "lllsss"
    answer = "qqqlll"
    assert position_check(guess, answer) == ("lllsss", [], [0, 1, 2])

    guess = "pulls"
    answer = "spill"
    assert position_check(guess, answer) == ("pulls", [3], [0, 2, 4])

    guess = "answe"
    answer = "answe"
    assert position_check(guess, answer) == ("answe", [0, 1, 2, 3, 4], [])

    guess = "gusse"
    answer = "answe"
    # Omit the second 's' and do not report any wrong positions
    assert position_check(guess, answer) == ("gusse", [2, 4], [])

    guess = "gsuse"
    answer = "answe"
    # Only report one wrong-position 's'
    assert position_check(guess, answer) == ("gsuse", [4], [1])

    guess = "guess"
    answer = "answe"
    # Only report first wrong-position 's'
    assert position_check(guess, answer) == ("guess", [], [2, 3])


def test_new_double_letter_check():
    guess = "gusse"
    answer = "answe"
    (_, rightpos, wrongpos) = position_check(guess, answer)
    assert new_double_letter_check(guess, rightpos, wrongpos) == {"s": 1}


def test_eliminated_letters():
    currset = {"z", "b", "r"}  # The answer is 'answe' and we guessed 'zebra' before
    guess = "guess"
    rightpos, wrongpos = ([], [2, 3])
    _new_set_of_eliminated_letters = {"z", "b", "r", "g", "u"}
    test_result = eliminated_letters(currset, guess, rightpos, wrongpos)
    assert test_result ^ _new_set_of_eliminated_letters == set()


def test_new_eliminated_letters():
    guess = "guess"
    rightpos, wrongpos = ([], [2, 3])
    _new_set_of_eliminated_letters = {"g", "u"}
    test_result = new_eliminated_letters(guess, rightpos, wrongpos)
    assert test_result ^ _new_set_of_eliminated_letters == set()


def test_possible_matches():
    guess = "wards"
    wordlist = [
        "rides",
        "drive",
        "snort",
        "green",
        "trove",
        "zebra",
        "couch",
        "adieu",
        "sport",
        "bicep",
        "quick",
    ]
    _possible_matches = [
        "rides",
        "drive",
        "snort",
        "green",
        "trove",
        "zebra",
        "adieu",
        "sport",
    ]
    test_result = possible_matches(guess, wordlist)
    assert test_result == _possible_matches


def test_remaining():
    assert isinstance(remaining("guess", list_maker(10)), list)
    guess = "guess"
    wordlist = [
        "answe",
        "asnwe",
        "anwes",
        "anwse",
        "ansew",
        "naswe",
        "nsawe",
    ]
    orig_rigwron = position_check(guess, wordlist[4])
    assert orig_rigwron == ("guess", [], [2, 3])


def test_remaining_eliminated():
    eliminated_letters = {"s"}
    wordlist = [
        "sword",
        "snort",
        "sport",
        "snoop",
        "folly",
        "throw",
        "holly",
        "moldy",
        "dolly",
    ]
    assert isinstance(remaining_eliminated(wordlist, eliminated_letters), list)
    wl_answer = [
        "folly",
        "throw",
        "holly",
        "moldy",
        "dolly",
    ]
    assert wl_answer == remaining_eliminated(wordlist, eliminated_letters)


def test_remaining_repeated():
    repeated_letters = {"t": 1, "o": 3}
    wl = [
        "sword",
        "snort",
        "snoort",
        "snooort",
        "snoooort",
        "green",
        "trove",
        "sport",
        "snoop",
        "ebony",
        "other",
        "throw",
        "otter",
        "stone",
        "phone",
    ]
    assert isinstance(remaining_repeated(wl, repeated_letters), set)
    wl_answer = {
        "ebony",
        "green",
        "other",
        "phone",
        "snooort",
        "snoop",
        "snoort",
        "snort",
        "sport",
        "stone",
        "sword",
        "throw",
        "trove",
    }
    assert wl_answer == remaining_repeated(wl, repeated_letters)


def test_remaining_wrongpos():
    wordset = {
        "dates",
        "fight",
        "grunt",
        "light",
        "mates",
        "other",
        "otter",
        "saint",
        "snort",
        "sport",
        "stays",
        "stone",
        "table",
        "their",
        "throw",
        "trove",
        "truck",
        "water",
    }
    answer = {"dates", "mates", "saint", "table", "water"}
    assert answer == remaining_wrongpos(wordset, "grate", [2, 3], True)


def test_remaining_wrongpos_dict():
    wordset = {
        "dates",
        "fight",
        "grunt",
        "light",
        "mates",
        "other",
        "otter",
        "saint",
        "snort",
        "sport",
        "stays",
        "stone",
        "table",
        "their",
        "throw",
        "trove",
        "truck",
        "water",
    }
    answer = {
        ("wrongpos", "a", 2): {"dates", "mates", "saint", "table", "water"},
        ("wrongpos", "t", 3): {
            "dates",
            "fight",
            "grunt",
            "light",
            "mates",
            "other",
            "otter",
            "saint",
            "snort",
            "sport",
            "stays",
            "stone",
            "table",
            "their",
            "throw",
            "trove",
            "truck",
            "water",
        },
    }
    assert answer == remaining_wrongpos_dict(wordset, "grate", [2, 3], True)


def test_remaining_dict_crush():
    wpdl = {
        ("wrongpos", "g", 0): {"bangs", "fight", "light", "singe", "sings"},
        ("wrongpos", "t", 3): {
            "dates",
            "fight",
            "grunt",
            "light",
            "mates",
            "other",
            "otter",
            "saint",
            "snort",
            "sport",
            "stays",
            "stone",
            "table",
            "their",
            "throw",
            "trove",
            "truck",
            "water",
        },
    }
    answer = {"fight", "light"}
    assert answer == remaining_dict_crush(wpdl)


def test_remaining_rightpos_dict():
    wl = wordlist
    answer = {
        ("rightpos", "t", 0): {
            "table",
            "their",
            "throw",
            "train",
            "trick",
            "trope",
            "trove",
            "truck",
        },
        ("rightpos", "r", 1): {
            "bread",
            "drive",
            "green",
            "grime",
            "grunt",
            "train",
            "trick",
            "trope",
            "trove",
            "truck",
            "write",
            "wrong",
        },
    }
    assert answer == remaining_rightpos_dict(wl, "truck", [0, 1])


def test_remaining_rightpos():
    wl = wordlist
    answer = {"train", "trick", "truck", "trope", "trove"}
    assert answer == remaining_rightpos(wl, "truck", [0, 1])


def test_letter_count():
    assert 4 == letter_count("GUESSguess", "s")


def test_check_all():
    guess = "gusse"
    answer = "ansew"
    a0 = check_all(guess, answer)
    assert a0 == ([2], [4], {"s": 1}, {"g", "u"})


def test_guess_game_broken():
    ## Test the Exception for empty results
    guess = "gusse"
    with pytest.raises(Exception):
        guess_game(
            guess,
        )
    results = {}
    results["answer"] = "ansew"
    a1 = {
        "guesses": {"gusse": ([2], [4])},
        "eliminated_letters": {"g", "u"},
        "double_letters": {"s": 1},
        "answer": "ansew",
    }
    assert a1 == guess_game(guess, results)
    a2 = {
        "eliminated_letters": {"g", "l", "u"},
        "double_letters": {"s": 1},
        "guesses": {"gusse": ([2], [4]), "glass": ([], [2, 3])},
        "answer": "ansew",
    }
    assert a2 == guess_game("glass", a1)
