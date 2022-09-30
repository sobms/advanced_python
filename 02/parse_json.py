import json

def keyword_callback(word):
    return word.upper()

def parse_json(json_str: str, keyword_callback, required_fields=None, keywords=None):
    keywords_dct = dict.fromkeys(keywords, 0)
    json_doc = json.loads(json_str)
    for field in required_fields:
        if field in json_doc:
            words_list = json_doc[field].split(' ')
        else:
            words_list = []
        for i in range(len(words_list)):
            if words_list[i] in keywords_dct:
                words_list[i] = keyword_callback(words_list[i])
        if len(words_list) > 0:
            json_doc[field] = ' '.join(words_list)
    return json.dumps(json_doc)

if __name__ == '__main__':
    print(parse_json('{"key2" : "word1 word2", "key3" : "word1 word3 word4"}', keyword_callback, required_fields=["key1"], keywords=["word2"]))