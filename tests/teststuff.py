import spacy
import re


def custom_pipeline(nlp):
    return (merge_html_tags, )


def insert_spaces_around_tags(html):
    return re.sub(r'(.)(<.*?>)(.)', r' \1 ', html).strip()


def merge_html_tags(doc):
    print(doc.text)
    indexes = [m.span() for m in re.finditer(r'(?<!\\)(<.*?>)', doc.text)]
    for start, end in indexes:
        doc.merge(start, end)

nlp = spacy.load('en', create_pipeline=custom_pipeline)

html = insert_spaces_around_tags(r"<p class='something' id='test'> something</br> </p>")
print(html)
doc = nlp(html)

print(doc.is_tagged)
print(doc.is_parsed)

for word in doc:
    print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)

