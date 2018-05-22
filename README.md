# LearningRasaNLU

installation:
$ pip3 install rasa_nlu
$ pip3 install rasa_nlu[spacy]
$ python3 -m spacy download en_core_web_md
$ python3 -m spacy link en_core_web_md en

run:
$ python3 -m rasa_nlu.train -c nlu_model_config.json --fixed_model_name current
$ python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue --epochs 300
$ python -m rasa_core.run -d models/dialogue -u models/nlu/default/current
