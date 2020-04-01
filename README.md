
# BIOBE 

This project organizes COVID-19 SARS-CoV-2 preprints from medRxiv and bioRxiv. The raw data comes from the [bioRxiv](https://connect.biorxiv.org/relate/content/181) page, but this project makes the data searchable, sortable, etc. The "most similar" search uses an exemplar SVM trained on tfidf feature vectors from the abstracts of these papers. The project is running live on [biomed-sanity.com](http://biomed-sanity.com/). (I could not register covid-sanity.com because the term is "protected")



Since I can't assess the quality of the similarity search I welcome any opinions on some of the hyperparameters. For instance, the parameter `C` in the SVM training and the size of the feature vector `max_features` (currently set at 2,000) dramatically impact the results.

This project follows a previous one of mine in spirit, [arxiv-sanity](https://github.com/karpathy/arxiv-sanity-preserver).
## Demo 
http://104.248.239.251:5000/sim/10.1101/2020.03.28.013508

## run

As this is a flask app running it locally is straight forward. First compute the database with `run.py` and then serve:

```
$ python run.py
$ flask run
```

To deploy in production I recommend NGINX and Gunicorn. After configuring NGINX in your environment something like

```
$ gunicorn3 --workers=3 serve:app --access-logfile -
```

will do the trick.


## License

MIT
