import spacy
import random

# create blank Language class
nlp = spacy.blank("en")

# create the built-in pipeline components and add them to the pipeline
ner = nlp.create_pipe("ner")
nlp.add_pipe(ner, last=True)

# add labels
LABELS = ['PRODUCT_TYPE', 'PRICE', 'COLOR', 'BRAND', 'GENDER', 'MATERIAL', 'FIT']
for label in LABELS:
    ner.add_label(label)

# training data
TRAIN_DATA = [
    ("Glossy-finish python-print calfskin loafers featuring gold-plated logo lettering", {"entities": [(0, 33, "PRODUCT_TYPE"), (53, 71, "MATERIAL")]}),
    ("Blue Moschino dress for women, price 515", {"entities": [(0, 4, "COLOR"), (5, 13, "BRAND"), (20, 25, "GENDER"), (33, 36, "PRICE")]}),
    # ... add more examples
]

# get names of other pipes to disable them during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

# only train NER
with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
    # show warnings for misaligned entity spans once
    warnings.filterwarnings("once", category=UserWarning, module='spacy')

    # reset and initialize the weights randomly
    nlp.begin_training()
    for itn in range(10):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            nlp.update(
                [text],  # batch of texts
                [annotations],  # batch of annotations
                drop=0.5,  # dropout - make it harder to memorise data
                losses=losses,
            )
        print("Losses", losses)

# test the trained model
for text, _ in TRAIN_DATA:
    doc = nlp(text)
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

# save model to output directory
nlp.to_disk('/path/to/your/model')
