### Political news classifier

#### Data

I have used [Webhose.io](http://webhose.io) to download thousands of news in different categories.

#### Training

You can follow the training process in this [Jupyter Notebook file](http://github.com/unbiased/models/PoliticalNewsClassifier.ipynb).

#### Saving the model

After finish training our model, we store our model data in three files:

1. **political_classifier.pth**

	Contains the model weights, saved using `torch.save()`

2. **political_classifier.cfg**

	Contains a serialized config file of the model, so we don't need to hardcode the model params.

```
config = {
    'vocab_size': VOCAB_SIZE,
    'labels':  {
         0 : "Non-political",
         1 : "Political"
    },
    'ngrams': 2,
    'embeddings_dim': EMBED_DIM    
}
```

3.	**political_classifier.vocab**

 	Contains the model words vocabulary.



### Political Stance classifier

#### Data

I have used [Webhose.io](http://webhose.io) to download thousands of news from a list of 67 newspapers.

Each newspaper was manually classified into EXTREME_LEFT, LEFT, LEFT_CENTER, LEAST_BIASED, RIGHT_CENTER, RIGHT, EXTREME_RIGHT, and the journal stance was used as a proxy for each news stance.

#### Training

You can follow the training process in this [Jupyter Notebook file](http://github.com/unbiased/models/PoliticalNewsStanceClassifier.ipynb).

#### Saving the model

Similar to the previous model, we have also stored our model in three files.