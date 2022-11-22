import json
from faker import Faker


def keyword_callback(word):
    return word.upper()


def parse_json(json_str: str,
               keyword_callback,
               required_fields=None,
               keywords=None):
    if required_fields is None or keywords is None:
        return json_str
    json_doc = json.loads(json_str)
    keywords_dct = dict.fromkeys(keywords, 0)
    for field in required_fields:
        if field in json_doc:
            words_list = json_doc[field].split(" ")
        else:
            words_list = []
        for i in range(len(words_list)):
            if words_list[i] in keywords_dct:
                words_list[i] = keyword_callback(words_list[i])
        if len(words_list) > 0:
            json_doc[field] = " ".join(words_list)
    return json.dumps(json_doc)


if __name__ == "__main__":
    fake = Faker()
    keywords = [
        fake.numerify(text="word%#")
        for _ in range(fake.random_int(max=100))
    ]
    required_fields = [
        fake.numerify(text="key%#")
        for _ in range(fake.random_int(max=100))
    ]
    json_str = json.dumps(
        {
            fake.numerify(text="key%#"): " ".join(
                [
                    fake.numerify(text="word%#")
                    for _ in range(fake.random_int(min=1, max=10))
                ]
            )
            for _ in range(fake.random_int(max=20))
        }
    )
    print(parse_json(json_str, keyword_callback, required_fields, keywords))
