from helpers import MODELS, AR_ENTITIES
import re
from helpers import predictor

def get_cores(doc, tokens):
    result = []

    for index, w in enumerate(doc):
        for cluster in w._.coref_clusters:
            for mention in cluster.mentions[-1]:
                if w.text in mention.text:
                    mnts = cluster.mentions[:-1]
                    matches = []
                    for span in mnts:
                        for token in span:
                            if token.tag_ in ["NN", "NNP"]:
                                found = tokens.index(token.text)
                                matches.append((found, token.text))
                    result.append({mention.text: matches})
    return result
