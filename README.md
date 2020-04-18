

# BIOBE 

This project organizes COVID-19 SARS-CoV-2 preprints from medRxiv and bioRxiv. The raw data comes from the BioBe , but this project makes the data searchable, sortable, etc. The "most similar" search uses an exemplar SVM trained on tfidf feature vectors from the abstracts of these papers. The project is running live on [BioBe. ip ](http://104.248.239.251:5000). (I could not register covid-sanity.com because the term is "protected")

bioRxiv (pronounced "bio-archive") is a free online archive and distribution service for unpublished preprints in the life sciences. It is operated by Cold Spring Harbor Laboratory, a not-for-profit research and educational institution. By posting preprints on bioRxiv, authors are able to make their findings immediately available to the scientific community and receive feedback on draft manuscripts before they are submitted to journals.

currently indexing 885 papers.




## Demo 
http://104.248.239.251:5000/
 
 
## Requirements

. Flask
. requests
. numpy
. sklearn

## Run

As this is a flask app running it locally is straight forward. First compute the database with `run.py` and then serve:

```
$ python run.py
$ flask run
```

To deploy in production I recommend NGINX and Gunicorn. After configuring NGINX in your environment something like

```
$ gunicorn3 --workers=3 serve:app --access-logfile -
```



This project follows ,@karpathy
[arxiv-sanity](https://github.com/karpathy/arxiv-sanity-preserver).


## License


MIT
