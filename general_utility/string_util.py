import json
import re

import unidecode


class StringUtil:
    """StringUtil: Utility file for operations related to a String

    """
    OPERATORS = ['(', ')', ';', ',', ':', '-', '[', ']', '!']
    REMOVABLE_STRINGS = ["\\", "*", "!", "_"]
    ALL_REMOVABLE_STRINGS = ['(', ')', ":", "-", "#", "!", "."]
    REPLACE_MAP = {"&#39;": "'",
                   "&amp;": "&",
                   "&#x2019;": "'",
                   "\u2013": "-",
                   "\u00a0": "",
                   "\xa0": " ",
                   "\xc2": " ",
                   "\u00ae": "",
                   "\u00e2": "",
                   "\u20ac": "",
                   "\u2122": "",
                   "B. Tech": "B.Tech",
                   "M. Tech": "M.Tech",
                   "B. S.": "BS",
                   "B.S.": "BS",
                   "M. S.": "MS",
                   "M.S.": "MS",
                   "B. E.": "BE",
                   "B.E.": "BE",
                   "M. E.": "ME",
                   "M.E.": "ME",
                   "e.g.": "e.g",
                   "eg.": "e.g",
                   "E.g.": "e.g",
                   "E.G.": "e.g",
                   "a.k.a.": "a.k.a"
                   }

    @staticmethod
    def get_dot_noises():
        """get_dot_noises

        Due to data scraping, sometimes sentences are not properly separated by
        period '.' i.e without space after a period. This function returns the
        frequently occuring noises

        """
        noises = {}
        if noises == {}:
            dot_noise_list = []
            dot_noise_map = {}
            for noise in dot_noise_list:
                dot_noise_map[noise] = noise.replace(".", ". ")
            return dot_noise_map
        return noises

    @staticmethod
    def string_convertor(value):
        if isinstance(value, unicode):
            value = unidecode.unidecode(value)
        else:
            value = str(value)
        return value

    @staticmethod
    def clean_weak(string):
        if not string:
            return ""
        result = StringUtil.string_convertor(string)

        replace_map = StringUtil.REPLACE_MAP
        for word, rep in replace_map.iteritems():
            result = result.replace(word, rep)
        re.sub(r"(\d)\.\s", r"\1 ", result)
        return result

    @staticmethod
    def clean(string, line_separator=" . "):
        """clean

        Removes junk characters from a string and returns a clean string
        that can be used for extracting information

        :param string: String to be cleaned
        """
        result = StringUtil.clean_weak(string)

        for removable_string in StringUtil.REMOVABLE_STRINGS:
            result = result.replace(removable_string, " ")

        separators = ["\n"]
        for separator in separators:
            result = result.replace(separator, line_separator)

        noises = StringUtil.get_dot_noises()

        for noise in noises:
            result = result.replace(noise, noises[noise])

        result = re.sub('[.]+', ".", result)
        result = re.sub('\.\s+\.', ".", result)
        return re.sub("\s+", " ", result).strip()

    @staticmethod
    def clean_strong(string):
        """clean

        Removes junk characters from a string and returns a clean string
        that can be used for extracting information

        :param string: String to be cleaned
        """
        result = StringUtil.clean(string, line_separator=" ")
        for removable_string in StringUtil.ALL_REMOVABLE_STRINGS:
            result = result.replace(removable_string, " ")
        return re.sub("\s+", " ", result).strip()

    @staticmethod
    def clean_list(strings, line_separator=" . "):
        """clean_list : Cleans all the strings in the list

        :param strings: Strings to be cleaned
        :param line_separator: Line Separator to be replaced with

        :type strings: List<String>
        :type line_separator: string
        """
        return [StringUtil.clean(string, line_separator) for string in strings]

    @staticmethod
    def contains(string, array):
        """contains : Checks whether string is present in array of not

        :param string: String to be checked
        :param array: List of strings

        :type string: string
        :type array: List<String>
        """
        return string in array

    @staticmethod
    def contains_any(string, array):
        """contains_any : checks whether string contains any
        element of the list

        :param string: String from where to be checked
        :param array: List of strings to be checked

        :type string: string
        :type array: List<String>
        """
        for key in array:
            if key in string:
                return True
        return False

    @staticmethod
    def pretty_print(json_object):
        """pretty_print : Prints a human readable string representation of the
        json object

        :param json_object: Json Object for which the string has to be returned

        :type json_object: Json
        """
        pretty_string = json.dumps(json_object, sort_keys=True, indent=4)
        print pretty_string
        # Returning for legacy reasons
        return pretty_string

    @staticmethod
    def pretty_string(json_object):
        """pretty_print : Returns a human readable string representation of the
        json object

        :param json_object: Json Object for which the string has to be returned

        :type json_object: Json
        """
        pretty_string = json.dumps(json_object, sort_keys=True, indent=4)
        return pretty_string

    @staticmethod
    def put_spaces_around_operators(text):
        for op in StringUtil.OPERATORS:
            text = text.replace(op, ' ' + op + ' ')
        return text

    # TODO :implement the concept of matching strength -
    # northwestern shouldnt match northeastern
    @staticmethod
    def editdistance(a, b):
        "Calculates the Levenshtein distance between a and b."
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a, b = b, a
            n, m = m, n

        current = range(n + 1)
        for i in range(1, m + 1):
            previous, current = current, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete = previous[j] + 1, current[j - 1] + 1
                change = previous[j - 1]
                if a[j - 1] != b[i - 1]:
                    change = change + 1
                current[j] = min(add, delete, change)

        return current[n]
