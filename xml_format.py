from utils import MODELS, AR_ENTITIES
import re
from utils import predictor


governor = "<governor idx='{}' {} {} {} {}>{}</governor>"
dependent = "<dependent idx='{}' {} {} {} {}>{}</dependent>"


def get_dependencies(doc):
    output = ""
    for index, token in enumerate(doc):
        output += "<dep type='{}'>".format(token.dep_.lower())
        governer = get_governor(token)
        dependent = get_dependent(token, index + 1)
        output += governer
        output += dependent
        output += "</dep>"
    return output


def get_dependencies_with_streusle(doc, tokens_tags):
    output = ""
    for index, token in enumerate(doc):
        output += "<dep type='{}'>".format(token.dep_.lower())

        governer = get_governor(token)
        dependent = get_dependent(token, index + 1)
        dword = re.findall(r'>(.+?)<', dependent)[0]
        gword = re.findall(r'>(.+?)<', governer)[0]

        d = ''
        g = ''
        if dword in tokens_tags["tokens"]:
            dfound = tokens_tags["tokens"].index(dword)
            d = tokens_tags["tags"][dfound]

        if gword in tokens_tags["tokens"]:
            gfound = tokens_tags["tokens"].index(gword)
            g = tokens_tags["tags"][gfound]

        governer = governer.replace("<governor", "<governor streusle='{}'".format(g))
        dependent = dependent.replace("<dependent", "<dependent streusle='{}'".format(d))

        output += governer
        output += dependent
        output += "</dep>"
    return output


def get_dependencies_with_streusle_synset_cores(span, tokens_tags):
    tokens = [w.text for w in span.doc]
    mentions = get_cores(span, tokens)
    output = ""
    for index, token in enumerate(span):
        output += "<dep type='{}'>".format(token.dep_.lower())

        governer = get_governor(token)
        dependent = get_dependent(token, index + 1)
        dword = re.findall(r'>(.+?)<', dependent)[0]
        gword = re.findall(r'>(.+?)<', governer)[0]
        # if dword in mentions.keys():
        corefd = ""
        corefg = ""
        for obj in mentions:
            if dword in obj.keys():
                sentence_id = "0"
                for id, sent in enumerate(span.doc.sents):
                    if obj[dword][0][1] in sent.text:
                        sentence_id = id
                for found in obj[dword]:
                    corefd += str(sentence_id) + ":" + str(found[0]) + ","
        for obj in mentions:
            if gword in obj.keys():
                sentence_id = "0"
                for id, sent in enumerate(span.doc.sents):
                    if obj[dword][0][1] in sent.text:
                        sentence_id = id
                for found in obj[gword]:
                    corefg += str(sentence_id) + ":" + str(found[0]) + ","
        d = ''
        g = ''
        if dword in tokens_tags["tokens"]:
            dfound = tokens_tags["tokens"].index(dword)
            d = tokens_tags["tags"][dfound]

        if gword in tokens_tags["tokens"]:
            gfound = tokens_tags["tokens"].index(gword)
            g = tokens_tags["tags"][gfound]
        if corefd:
            dependent = dependent.replace("<dependent", "<dependent streusle='{}' coref='{}'".format(d, corefd))
        else:
            dependent = dependent.replace("<dependent", "<dependent streusle='{}'".format(d))
        if corefg:
            governer = governer.replace("<governor", "<governor streusle='{}' coref='{}'".format(g, corefg))
        else:
            governer = governer.replace("<governor", "<governor streusle='{}'".format(g))
        # governer = governer.replace("<governor", "<governor streusle='{}' coref='{}'".format(g, corefg))
        # dependent = dependent.replace("<dependent", "<dependent streusle='{}' coref='{}'".format(d, corefd))

        output += governer
        output += dependent
        output += "</dep>"
    return output


def get_lemma(token):
    lemma = ''
    if token.text != token.lemma_:
        lemma = "lemma='{}'".format(token.lemma_)
    return lemma


def get_governor_tag(token):
    gtag = token.head.tag_
    tag = token.head.pos_
    if token.sent.root.text == token.text:
        gtag = ""
    return gtag, tag


def get_governor_lemma(token):
    lemma = ''
    if token.head.text != token.head.lemma_:
        lemma = "lemma='{}'".format(token.head.lemma_)
    if token.sent.root.text == token.text:
        lemma = ""

    return lemma


def get_governor_ent_type(token):
    gnee = ""
    if token.head.ent_type_ and token.head.ent_type_ in AR_ENTITIES.keys():
        gnee = "nee='{}'".format(AR_ENTITIES[token.head.ent_type_])
    elif token.head.ent_type_:
        gnee = "nee='{}'".format(token.head.ent_type_)
    return gnee


def get_ent_type(token):
    nee = ""
    if token.ent_type_ and token.ent_type_ in AR_ENTITIES.keys():
        nee = "nee='{}'".format(AR_ENTITIES[token.ent_type_])
    elif token.ent_type_:
        nee = "nee='{}'".format(token.ent_type_)
    return nee


def get_governor(token):
    head = token.head
    gtag, pos = get_governor_tag(token)
    lemma = get_governor_lemma(token)
    nee = get_governor_ent_type(token)

    if head.text == token.text and token.dep_ == "ROOT":
        head = "root"
    if token.sent.root.text == token.text:
        lemma = ""
    # check head if its a string then we dont have any synset
    synset = "synsetid='{}'".format(head._.offset) if type(head) != str else ""
    if gtag:
        return governor.format(token.head.i + 1, "pennbank='{}' pos='{}'".format(gtag, pos), nee, lemma, synset, head)
    else:
        return governor.format(token.head.i + 1, gtag, nee, lemma, synset, head)


def get_dependent(token, index):
    lemma = get_lemma(token)
    nee = get_ent_type(token)
    synset = "synsetid='{}'".format(token._.offset) if token._.offset else ""
    return dependent.format(index, "pennbank='{}' pos='{}'".format(token.tag_, token.pos_), nee, lemma, synset, token.text)


def get_streusle_json(doc):
    tokens = []
    lemmas = []
    upos_tags = []
    for span in doc:
        tokens.append(span.text)
        lemmas.append(span.lemma_)
        upos_tags.append(span.pos_)
    return {"tokens": tokens, "upos_tags":upos_tags, "lemmas": lemmas}


def get_doc(text, lang):
    model = MODELS[lang]
    output = ""
    text = text.replace('\n', ' ')

    if lang == "en":
        doc = model(text.strip())
        # sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", text.strip())
        output += "<parser>"
        for sentence_id, sentence in enumerate(doc.sents):
            tokens_tags = predictor.predict_json(get_streusle_json(sentence))
            dep_start = "<dependencies type='collapsed-dependencies'>"
            dependencies = get_dependencies_with_streusle_synset_cores(sentence, tokens_tags)
            dependencies += "<original-sentence>{}".format(sentence.text) + "</original-sentence>"
            dep_end = "</dependencies>"
            output += dep_start + dependencies + dep_end
    else:
        return {"<{}>".format(lang) + "Not supported" + "</{}>".format(lang)}
    return output + "</parser>"


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
