## Unbiased API

The API was built using Python 3 and Flask. 

#### GET /suggestions?headline={headline}
The main endpoint called by the browser extension is the `/suggestions` endpoint. 

It receives a query param `headline` and returns a list of alternative views: one that is `central` and other that is oppositve from the headline sent.

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

There are two other endpoints availables `/is_political` and `/political_stance`.

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