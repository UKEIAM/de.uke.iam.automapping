Actual code 

```
|- src
    |- automapping/    (source code)
        |- concept.py       (object to keep concepts)
        |- detections.py     (object to create dataframe with predictions)
        |- language.py
        |- m5_pipeline.py   (integration with internal application)
        |- loader.py        (file with data loading)
        |- prediction.py    (object with keep predictions)
        |- preprocessor.py   (abbreviation replacement and nlp preprocessin)
        |- translator.py    (translation with Hugging Face model from German to English)
        |- mapper.py        (objject with TF-idf model)
```