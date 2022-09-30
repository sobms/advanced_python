import unittest
import unittest.mock
from parse_json import parse_json

@unittest.mock.patch("parse_json.keyword_callback")
class ParseJsonTest(unittest.TestCase):
    def test_parse_json(self, keyword_callback_mock):
        #case1
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]
        keyword_callback_mock.return_value = 'str1'
        self.assertEqual(parse_json(json_str, keyword_callback_mock, required_fields, keywords),
                         '{"key1": "Word1 str1", "key2": "word2 word3"}')
        self.assertEqual(keyword_callback_mock.call_count, 1)
        #case2
        json_str = '{"key1": "Word1 word2 word3", "key2": "word2 word3", "key3": "word1 word4 word5"}'
        required_fields = ["key2", "key3"]
        keywords = ["word2", "word3", "word4"]
        keyword_callback_mock.return_value = 'str1'
        self.assertEqual(parse_json(json_str, keyword_callback_mock, required_fields, keywords),
                         '{"key1": "Word1 word2 word3", "key2": "str1 str1", "key3": "word1 str1 word5"}')
        self.assertEqual(keyword_callback_mock.call_count, 4)
        #case3
        json_str = '{}'
        required_fields = ["key2", "key3"]
        keywords = ["word2", "word3", "word4"]
        keyword_callback_mock.return_value = 'str1'
        self.assertEqual(parse_json(json_str, keyword_callback_mock, required_fields, keywords),
                         '{}')
        self.assertEqual(keyword_callback_mock.call_count, 4)
        #case4
        json_str = '{"key2": "word1 word2", "key3": "word1 word3 word4"}'
        required_fields = ["key2", "key3"]
        keywords = ["word5"]
        keyword_callback_mock.return_value = 'str1'
        self.assertEqual(parse_json(json_str, keyword_callback_mock, required_fields, keywords),
                         '{"key2": "word1 word2", "key3": "word1 word3 word4"}')
        self.assertEqual(keyword_callback_mock.call_count, 4)
        #case5
        json_str = '{"key1": "Word1 word2 word3", "key2": "word2 word3", "key3": "word1 word4 word5"}'
        required_fields = []
        keywords = ["word2", "word3", "word4"]
        keyword_callback_mock.return_value = 'str1'
        self.assertEqual(parse_json(json_str, keyword_callback_mock, required_fields, keywords),
                         '{"key1": "Word1 word2 word3", "key2": "word2 word3", "key3": "word1 word4 word5"}')
        self.assertEqual(keyword_callback_mock.call_count, 4)
        #case6
        json_str = '{"key1": "Word1 word2 word3", "key2": "word2 word3", "key3": "word1 word4 word5"}'
        required_fields = ["key2", "key3"]
        keywords = []
        keyword_callback_mock.return_value = 'str1'
        self.assertEqual(parse_json(json_str, keyword_callback_mock, required_fields, keywords),
                         '{"key1": "Word1 word2 word3", "key2": "word2 word3", "key3": "word1 word4 word5"}')
        self.assertEqual(keyword_callback_mock.call_count, 4)




