### Install packages
run
```shell
pip install -r requirements.txt
```

## Spacy and stanfordnlp models
Now install `spacy` model
```shell
python -m spacy download en_core_web_sm
```

Install `stanfordnlp` model, Run in Python Console
```python
import stanza
stanza.download("en")
```
