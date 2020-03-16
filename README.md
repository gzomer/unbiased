## What it is?

Unbiased is a web browser extension that detects political bias in your Facebook news feed and automatically suggests alternative views.

[![Unbiased](https://img.youtube.com/vi/j9CDgkuy5aw/0.jpg)](https://www.youtube.com/watch?v=j9CDgkuy5aw)

## How to test it?

[Unbiased Chrome Extension](https://chrome.google.com/webstore/detail/jmmjoijiobljkppffbfcajelfihgllem/)

## How I built it

Unbiased has five main components:

-	Browser extension
-	API
-	Political news classifier
-	Political news stance classifier
-	Recommendation system

### 1. Browser extension

The browser extension was developed using `Javascript` and `Chrome Extensions API`.

It has two main files: `script.js` and `background.js`.

#### script.js

This script is responsible for monitoring changes in your news feed, and detecting which of the items are news.
I did this by selecting all news feed items that have a link, which of course, may contain non-political content. 

This is why we need to send the headline to the `suggestions` API, which will detect if the headline is related to politics or not.

As this is script doesn't have permission to run CORS requests, we need to send a message to the `background.js` script, which will then call the API.

#### background.js

After receiving a message with a headline, the `background.js` script calls the `/suggestions` endpoint. Finally, after receiving the response, it sends the response back to the main script, which will then render the templates with the alternative news returned from the API.

### 2. API

The API was built using Python 3 and Flask. 

#### GET /suggestions?headline={headline}
The main endpoint called by the browser extension is the `/suggestions` endpoint. 

It receives a query param `headline` and returns a list of alternative views: one that is `central` and other that is opposite from the headline sent.

An example request and response can be seen below.

#### Request

```
curl https://unbiased.us/suggestions?headline=Coronavirus+Is+Officially+A+Pandemic,+But+What+Does+That+Mean?
```

#### Response
```
{
  "headline": "Coronavirus Is Officially A Pandemic, But What Does That Mean?", 
  "suggestions": [
    {
      "domain": "economist.com", 
      "id": "6bce3f764437a8997a732b2a731db514dd3dea36", 
      "image": "https://www.economist.com/sites/default/files/20200208_IRD001.jpg", 
      "link": "https://www.economist.com/international/2020/02/05/scientists-are-racing-to-produce-a-vaccine-for-the-latest-coronavirus", 
      "similarity": 0.8283491563149442, 
      "stance": "central", 
      "title": "Run, don\u2019t walk - Scientists are racing to produce a vaccine for the latest coronavirus | International | The Economist"
    }, 
    {
      "domain": "slate.com", 
      "id": "466acd332a765c9df5a56c91faf6d9eeae34b4ca", 
      "image": "https://compote.slate.com/images/cbf40c69-4949-4638-b7a5-7ba81880bd39.jpeg?width=780&height=520&rect=1560x1040&offset=0x0", 
      "link": "https://slate.com/technology/2020/02/coronavirus-vaccine-possibility-sars-wuhan-research.html", 
      "similarity": 0.9121501602756262, 
      "stance": "left", 
      "title": "How close are we to a coronavirus vaccine?"
    }
  ]
}
```

There are two other endpoints available: `/is_political` and `/political_stance`.

#### GET /is_political?headline={headline}
Detect if the headline is related to politics or not.

```
{
  "political": true
}

```

#### GET /political_stance?headline={headline}
Return the headline political stance (left, center or right)

```
{
  "stance": "right"
}
```

### 3. Political news classifier

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



### 4. Political Stance classifier

#### Data

I have used [Webhose.io](http://webhose.io) to download thousands of news from a list of 67 newspapers.

Each newspaper was manually classified into EXTREME_LEFT, LEFT, LEFT_CENTER, LEAST_BIASED, RIGHT_CENTER, RIGHT, EXTREME_RIGHT, and the journal stance was used as a proxy for each news stance.

#### Training

You can follow the training process in this [Jupyter Notebook file](http://github.com/unbiased/models/PoliticalNewsStanceClassifier.ipynb).

#### Saving the model

Similar to the previous model, we have also stored our model in three files.

### 5. Recommendation system

The recommendation system module is responsible for suggesting alternative news based on a headline and a stance.

It works by comparing the embeddings (GloVE) of the headline with the embeddings of all the other news given a specific stance. 

To compare, we use cosine similarity and we return the most similar news.

As computing the embeddings every time for all news would be slow, we built an in-memory cache of the embeddings so that the comparison can run faster.

## Challenges I ran into

Initially, the idea was to have a more fine-grained classification of political stance (EXTREME_LEFT, LEFT, LEFT_CENTER, LEAST_BIASED, RIGHT_CENTER, RIGHT, EXTREME_RIGHT).

However, this proved to be difficult, especially due to the lack of enough training data.

Also, only using the headline isn't always enough to classify the stance correctly, as we don't have enough context.

Another challenge was the fact the extremes (both right and left), sometimes got mixed up. From my analysis, this was due to the fact that both sides tend to use strong and emotional words, and this was challenging for the classifier to detect.

## What's next for Unbiased

- Expand to other social networks
- Get more data to improve the classifiers
- Improve the models by also passing part of the news content as a context
- Improve the political stance classifier for the extreme views
- Add more domains other than politics (fake news, hate speech, sexism, racism)