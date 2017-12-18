from __future__ import division

from Levenshtein import distance
from numpy import mean
from zutils.merge_util import merge_map


def isnumber(x):
    """isnumber : Checks whether the object is an instance of
    int long float or complex

    :param x: object to be checked
    """
    return isinstance(x, (int, long, float, complex))


def isstring(x):
    """isstring : Checks whether the object is an instance of
    string

    :param x: object to be checked
    """
    return isinstance(x, (str, unicode))


class CompareUtil:
    '''
        Utility Class for comparing two jsons and assigning a score
    '''

    @staticmethod
    def compare(obj1, obj2, detailed=False, min_match_score=0.1):
        '''
        Compares two objects and scores them from 0-1.
        1 indicating a perfect match and 0 for mismatch

        :param obj1: Expected Object
        :type obj1: Object to be matched
        :param obj2: object
        :type obj2: object
        '''
        if isinstance(obj1, list) and isinstance(obj2, list):
            return CompareUtil.compare_list(obj1, obj2, detailed, min_match_score)
        if isinstance(obj1, dict) and isinstance(obj2, dict):
            return CompareUtil.compare_dict(obj1, obj2, detailed)
        else:
            return CompareUtil.compare_type(obj1, obj2, detailed)

    @staticmethod
    def compare_list(obj1, obj2, detailed=False, min_match_score=0.1):
        '''
        Compares two lists and scores them

        The order of elements in the 2 list need not be the same.
        It tries to score an element in the list against every other to
        get the best match

        :param obj1: Expected List
        :type obj1: List to be matched

        :param obj2: list
        :type obj2: list
        '''
        output = {}
        selected_indices = []
        index_map = {}
        for i in xrange(0, len(obj1)):
            max_score = min_match_score
            max_index = -1
            # find out the most appropriate match from the list
            for j in xrange(0, len(obj2)):
                if j not in selected_indices:
                    score = CompareUtil.compare(obj1[i],
                                                obj2[j],
                                                False).get("score", 0.0)

                    if score > max_score:
                        max_score = score
                        max_index = j

            # Check if there is a better rev match for the max_score element
            if max_index != -1:
                reverse_max_score = min_match_score
                for j in xrange(i, len(obj1)):
                    if j not in selected_indices:
                        score = CompareUtil.compare(
                            obj1[j], obj2[max_index], False).get("score", 0.0)
                        if score > reverse_max_score:
                            reverse_max_score = score
                if reverse_max_score > max_score:
                    max_index = -1

            if max_index != -1:
                index_map[i] = [max_index]
                output = merge_map(output,
                                   CompareUtil.compare(obj1[i],
                                                       obj2[max_index], detailed))
                selected_indices.append(max_index)
            else:
                output_obj = {"score": 0.0,
                              "count": 1,

                             }
                if detailed:
                    output_obj["details"] = {"unmatch": [obj1[i]]}
                output = merge_map(output, output_obj)

        if detailed:
            extra_objs = []
            for j in xrange(0, len(obj2)):
                if j not in selected_indices:
                    extra_objs.append(obj2[j])
            if "details" not in output:
                output["details"] = {"extra": []}
            output["details"]["extra"] = extra_objs

        score = output.get("score", 0) / output.get("count", 1)
        average_score = 1.0
        if output.get("count", 0) > 0:
            average_score = score
        compare_output = {
                "score": average_score,
                "details": output,
                "count": 1
        }
        if detailed:
            compare_output["mapping"] = index_map
        return compare_output

    @staticmethod
    def compare_type(obj1, obj2, detailed=False):
        '''
        Compares two primitive types (numbers and strings)

        :param obj1: Expected Object
        :type obj1: Object to be compared

        :param obj2: Number or String
        :type obj2: Number or String

        :param detailed: Boolean indicating whether details should be returned
        :type detailed: boolean
        '''
        score = 0.0
        if isnumber(obj1) and isnumber(obj2):
            score = 0.0
            if (obj1 == obj2):
                score = 1.0
        if isstring(obj1) and isstring(obj2):
            max_len = max(len(obj1), len(obj2))
            score = 1.0
            if max_len > 0:
                score = (max_len - distance(obj1.lower(), obj2.lower())) / max_len
            score = max(0.0, score)
        details = {}
        if detailed:
            if score == 1.0:
                details["exact"] = [obj1]
            elif score != 0.0:
                details["partial_match"] = [{
                                             "expected": obj1,
                                             "found": obj2,
                                             "score": score
                                            }]
            else:
                details["mismatch"] = [{
                                             "expected": obj1,
                                             "found": obj2
                                            }]
        output = {"score": score, "count": 1}
        if detailed:
            output["detailed"] = details
        return output

    @staticmethod
    def compare_dict(obj1, obj2, detailed=False):
        '''
        Compares two dicts and scores them

        :param obj1: Expected Dict
        :type obj1: Dict to be matched

        :param obj2: dict
        :type obj2: dict
        '''
        output = {}
        for key in obj1:
            if key in obj2:
                val1 = obj1[key]
                val2 = obj2[key]
                output[key] = CompareUtil.compare(val1, val2, detailed)
            else:
                output[key] = {
                               "score": 0.0,
                               "count": 1,
                               "details": {
                                           "unmatch": {key: [obj1[key]]}
                                           }
                               }

        scores = [output[k]["score"] for k in output]
        average_score = 1.0
        if len(scores) > 0:
            average_score = mean(scores)
        return {
                "score": average_score,
                "count": 1,
                "details": output
        }


def test():
    dict_a = {"a": 2,
              "b": 2,
              "c": [1, 2, 3]
              }
    dict_b = {"a": 2,
              "b": 2,
              "c": [2, 4]
              }

    list_a = [{"AttendanceEndDate": "2011-01-01",
               "AttendanceStartDate": "",
               "DegreeLevel": "phd",
               "MajorProgramName": [
                   "Computer Science"
               ],
               "School": "University of California, Berkeley"
               }]
    list_b = [{"AttendanceEndDate": "",
               "AttendanceStartDate": "2011-01-01",
               "DegreeLevel": "phd",
               "MajorProgramName": [
                   "Computer Science"
               ],
               "School": "University of California, Berkeley"
               }]

    from zutils.string_util import StringUtil
    print StringUtil.pretty_print(CompareUtil.compare(dict_a, dict_b, True))
    print StringUtil.pretty_print(CompareUtil.compare(list_a, list_b, True))


if __name__ == "__main__":
    test()
