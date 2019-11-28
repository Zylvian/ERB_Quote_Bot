import json
import string


class Constants():
    """wraps all constant data"""

    def __init__(self, constantJSON='data/constants.json'):
        with open(constantJSON, 'r', encoding='utf8') as file:
            constants = json.load(file)

        # alternative names
        self.__translations = {}
        for actual_name, alt_names in constants['alternative_names'].items():

            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    self.__translations[alt_name] = actual_name
            else:
                self.__translations[alt_names] = actual_name

        self.alternativeNames = self.__translations.keys()

        ##
        self.__wikis = {}
        for wiki_name, subreddit_names in constants['sub_to_wiki'].items():

            if isinstance(subreddit_names, list):
                for subreddit_name in subreddit_names:
                    self.__wikis[subreddit_name] = wiki_name
            else:
                self.__wikis[subreddit_names] = wiki_name