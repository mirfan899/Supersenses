import time

import spacy
from streusle_tagger.models import streusle_tagger
# import jsonlines
from allennlp.predictors import Predictor
nlp = spacy.load("en_core_web_sm")
predictor = Predictor.from_path("models/streusle_linear/model.tar.gz", predictor_name="streusle-tagger")


start = time.time()
doc = nlp("John went to the pool")
tokens = []
lemmas = []
upos_tags = []

for span in doc:
    tokens.append(span.text)
    lemmas.append(span.lemma_)
    upos_tags.append(span.pos_)

data = [{"tokens": tokens, "upos_tags":upos_tags, "lemmas": lemmas}]

# with jsonlines.open('test.jsonl', 'w') as writer:
#     writer.write_all(data)

# predict


print(predictor.predict_json({"tokens": tokens, "upos_tags": upos_tags, "lemmas": lemmas}))

end = time.time()
print((end-start)*1000)
