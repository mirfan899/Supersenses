import spacy
from allennlp.predictors import Predictor
from streusle_tagger.models import streusle_tagger

ENGLISH = spacy.load("en_core_web_sm")
predictor = Predictor.from_path("models/streusle_linear/model.tar.gz", predictor_name="streusle-tagger")

MODELS = {
    "en": ENGLISH,
}

AR_ENTITIES = {"B-LOC": "LOCATION",
               "I-LOC": "LOCATION",
               "B-ORG": "ORG",
               "I-ORG": "ORG",
               "I-PER": "PERSON",
               "B-PER": "PERSON",
               "B-MIS": "MIS",
               "I-MIS": "MIS",
               "PER": "PERSON",
               "LOC": "LOCATION",
               "B-FAC": "FACILITY",
               "I-FAC": "FACILITY",
               "B-PRO": "PRODUCT",
               "I-PRO": "PRODUCT",
               "B-EVE": "EVENT",
               "I-EVE": "EVENT",
               "DAT-B": "DATE",
               "DAT-I": "DATE",
               "PER-B": "PERSON",
               "PER-I": "PERSON",
               "EVT-B": "EVENT",
               "EVT-I": "EVENT",
               "CVL-B": "CIVILIZATION",
               "CVL-I": "CIVILIZATION",
               "ORG-B": "ORG",
               "ORG-I": "ORG",
               "NUM-B": "NUMBER",
               "NUM-I": "NUMBER",
               "LOC-B": "LOCATION",
               "LOC-I": "LOCATION",
               "FLD-B": "FIELD",
               "FLD-I": "FIELD",
               "TIM-B": "TIME",
               "TIM-I": "TIME",
               "ANM-B": "ANIMAL",
               "ANM-I": "ANIMAL",
               "PLT-B": "PLANT",
               "PLT-I": "PLANT",
               "MAT-B": "MATERIAL",
               "MAT-I": "MATERIAL",
               "TRM-B": "TERM",
               "TRM-I": "TERM",
               "AFW-B": "ARTIFACTS_WORKS",
               "AFW-I": "ARTIFACTS_WORKS",
               }

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
