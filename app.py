# -*- coding: utf-8 -*-
from flask import Flask, request, Response

from xml_format import get_doc

app = Flask(__name__, template_folder="static")


@app.route('/', methods=["GET"])
def text_to_xml():
    request.encoding = 'utf-8'

    text = request.args.get('text')
    lang = request.args.get('lang')
    if lang == None or text == None:
        return Response("<missing>lang or text missing</missing>", mimetype='application/xml')
    xml = get_doc(text, lang)
    return Response(xml, mimetype='application/xml')


if __name__ == '__main__':
    app.run(threaded=False, processes=1)
