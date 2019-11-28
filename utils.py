import itertools
import json
import random
import re
import string


class Util:

    # Class is created for the files to load only once.

    def __init__(self, constantJSON='data/constants.json'):
        with open(constantJSON, 'r') as file:
            constants = json.load(file)

        #self.keywords = constants["triggers"]
        self.subreddits = constants["subreddits"]

        with open('data/songs.json', 'r') as file:
            songs = json.load(file)

        self.all_lyrics = self._get_all_lyrics_list(songs)

        self.spellchecker = SpellChecker(self.all_lyrics)

    def _get_all_lyrics_list(self, songs):
        song_list = [song for song in songs.values()]
        massive_list = [lyric for lyric in song_list]
        un_nested_list = list(itertools.chain.from_iterable(massive_list))
        return un_nested_list

    def get_next_lyric(self, text):
        """ Checks if the trigger words to call the bot are present in the string """

        is_return_lyric = False

        for lyric in self.all_lyrics:
                # If this is the lyric to return.
                if is_return_lyric:
                    return lyric
                # Checks if comment is a lyric.
                try:
                    if re.search(text.lower(), lyric.lower(), re.IGNORECASE):
                        is_return_lyric = True
                except re.error:
                    print("Nothing to repeat?")

        # Returns nothing if not.
        return None

    """def get_random_quote(self):
        Returns random quote from quotes file

        return random.choice(self.quotes).upper()"""

    def get_subs(self):
        "Returns a list of all the subs where the bot should be active."
        return self.subreddits

class SpellChecker():
    """Find and fix simple spelling errors.
    based on Peter Norvig
    http://norvig.com/spell-correct.html
    """

    def __init__(self, names):
        self.model = set(names)

    def __known(self, words):
        for w in words:
            if w in self.model:
                return w
        return None

    def __edits(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = (a + b[1:] for a, b in splits if b)
        transposes = (a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1)
        replaces = (a + c + b[1:] for a, b in splits for c in string.ascii_lowercase if b)
        inserts = (a + c + b for a, b in splits for c in string.ascii_lowercase)
        return itertools.chain(deletes, transposes, replaces, inserts)

    def correct(self, word):
        """returns input word or fixed version if found"""
        return self.__known([word]) or self.__known(self.__edits(word)) or word
