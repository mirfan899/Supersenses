import spacy
from streusle_tagger.models import streusle_tagger
from allennlp.predictors import Predictor
nlp = spacy.load("en_core_web_sm")
predictor = Predictor.from_path("models/streusle_linear/model.tar.gz", predictor_name="streusle-tagger")


def get_supersenses(text):
    doc = nlp(text)
    tokens = []
    lemmas = []
    upos_tags = []
    for span in doc:
        tokens.append(span.text)
        lemmas.append(span.lemma_)
        upos_tags.append(span.pos_)
    result = predictor.predict_json({"tokens": tokens, "upos_tags": upos_tags, "lemmas": lemmas})
    output = []
    for index, (to, ta) in enumerate(zip(result["tokens"], result["tags"])):
        output.append({"index": index, "token": to, "tag": ta})

    return output


# result = []
# tokens = [w.text for w in doc]
# for index, w in enumerate(doc):
#     for cluster in doc._.coref_clusters:
#         for mention in cluster.mentions[-1]:
#             if w.text in mention.text:
#                 # find shit here
#                 print(index, w)
#                 mnts = cluster.mentions[:-1]
#                 matches = []
#                 for span in mnts:
#                     for token in span:
#                         if token.tag_ in ["NN", "NNP"]:
#                             found = tokens.index(token.text)
#                             matches.append((found, token.text))
#                 result.append({mention.text: matches})
