### BioBe 
OMAC COVID-19 HACKATHON

How can AI help us to understand everything about CoronaVirus ?
In machine learning, support-vector machines (SVMs, also support-vector networks) are supervised learning models with associated learning algorithms that analyze data used for classification and regression analysis. Given a set of training examples, each marked as belonging to one or the other of two categories, an SVM training algorithm builds a model that assigns new examples to one category or the other, making it a non-probabilistic binary linear classifier (although methods such as Platt scaling exist to use SVM in a probabilistic classification setting). An SVM model is a representation of the examples as points in space, mapped so that the examples of the separate categories are divided by a clear gap that is as wide as possible. New examples are then mapped into that same space and predicted to belong to a category based on the side of the gap on which they fall.
In addition to performing linear classification, SVMs can efficiently perform a non-linear classification using what is called the kernel trick, implicitly mapping their inputs into high-dimensional feature spaces.
When data is unlabelled, supervised learning is not possible, and an unsupervised learning approach is required, which attempts to find natural clustering of the data to groups, and then map new data to these formed groups. The support-vector clustering algorithm, created by Hava Siegelmann and Vladimir Vapnik, applies the statistics of support vectors, developed in the support vector machines algorithm, to categorize unlabeled data, and is one of the most widely used clustering algorithms in industrial applications.


I have trained  SVN Model_covid19 , with exemplar trained on TFIDF .
TFIDF, is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus. It is often used as a weighting factor in searches of information retrieval, text mining, and user modeling. The tf–idf value increases proportionally to the number of times a word appears in the document and is offset by the number of documents in the corpus that contain the word, which helps to adjust for the fact that some words appear more frequently in general. 
This project organizes COVID-19 SARS-CoV-2 preprints from medRxiv and bioRxiv, and it is able to add all the source for covid 19 when we can make it legal ,The raw data comes from the bioRxiv , and this project makes the data searchable, sortable, etc. 








## Hosts : 
I got free hosting from DigitalOcean as part of an initiative Supporting each other through COVID-19

8 GB Memory / 160 GB Disk / FRA1 Ubuntu  

Code layout
There are two large parts of the code:

Indexing code. Uses Arxiv API to download the most recent papers in any categories you like, and then downloads all papers, extracts all text, creates tfidf vectors based on the content of each paper. This code is therefore concerned with the backend scraping and computation: building up a database of bioxiv  papers, calculating content vectors, creating thumbnails, computing SVMs for people, etc.

User interface. Then there is a web server (based on Flask/Tornado/sqlite) that allows searching through the database and filtering papers by similarity, etc.
numpy, feedparser (to process xml files), scikit learn (for tfidf vectorizer, training of SVM), ImageMagick ,pdftotext, flask (for serving the results), flask_limiter, and tornado
Also dateutil, and scipy. And sqlite3 for database (accounts, library support, etc.) 



## Demo 
http://biobe.betech.ai/
 
 
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



## License


MIT
