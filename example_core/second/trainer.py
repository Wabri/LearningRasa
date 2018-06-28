from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
training_data = load_data('data/trainingData/base_data_set.json')
trainer = Trainer(config.load('data/nlu_model_config.yml'))
trainer.train(training_data)
model_directory = trainer.persist('models/nlu/', fixed_model_name="current")
