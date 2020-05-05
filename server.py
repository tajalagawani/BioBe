"""
Simple flask server for the interface
"""

import os
import json

from flask import Flask, request, redirect, url_for, Response
from flask import render_template

# -----------------------------------------------------------------------------

app = Flask(__name__)

seo_settings = {
	'default_page_title' : "COVID-19 Research AI Registry",
	'default_page_description': "This project is part of an initiative Supporting each other through COVID-19, following https://www.biorxiv.org/ to help with influx of papers on COVID-19, Built by Taj Noah."
}

# load raw paper data
with open('jall.json', 'r') as f:
    jall = json.load(f)
# this is crazy, I think they just recently changed this API
# for now converting to "legacy format" as just a string as a quick fix
for j in jall['rels']:
    if isinstance(j['rel_authors'], list):
        j['rel_authors'] = '; '.join(a['author_name'] for a in j['rel_authors'])

# load computed paper similarities
with open('sim_tfidf_svm.json', 'r') as f:
    sim_dict = json.load(f)

# load search dictionary for each paper
with open('search.json', 'r') as f:
    search_dict = json.load(f)

# OPTIONAL: load tweet dictionary, if twitter_daemon has run
tweets_dict = {}
if os.path.isfile('tweets.json'):
    with open('tweets.json', 'r') as f:
        tweets_dict = json.load(f)
# decorate each paper with tweets
for j in jall['rels']:
    j['tweets'] = tweets_dict.get(j['rel_doi'], [])
    j['tweets'].sort(key=lambda t: t['followers'], reverse=True)

# do some precomputation since we're going to be doing lookups of doi -> doc index
doi_to_ix = {}
for i, j in enumerate(jall['rels']):
    doi_to_ix[j['rel_doi']] = i

# -----------------------------------------------------------------------------
# few helper functions for routes

def default_context(papers, **kwargs):
    """ build a default context for the frontend """
    gvars = {'num_papers': len(jall['rels'])}
    gvars.update(kwargs) # insert anything else from kwargs into global context
    context = {'papers': papers, 'gvars': gvars}
    return context

# -----------------------------------------------------------------------------
# routes below

@app.route("/search", methods=['GET'])
def search():
    q = request.args.get('q', '') # get the search request
    if not q:
        return redirect(url_for('main')) # if someone just hits enter with empty field

    qparts = q.lower().strip().split() # split by spaces

    # accumulate scores
    n = len(jall['rels'])
    scores = []
    for i, sd in enumerate(search_dict):
        score = sum(sd.get(q, 0) for q in qparts)
        if score == 0:
            continue # no match whatsoever, dont include
        score += 1.0 * (n - i)/n # give a small boost to more recent papers (low index)
        scores.append((score, jall['rels'][i]))
    scores.sort(reverse=True, key=lambda x: x[0]) # descending
    papers = [x[1] for x in scores if x[0] > 0]
    if len(papers) > 40:
        papers = papers[:40]
    context = default_context(papers, sort_order='search', search_query=q)
    return render_template('index.html', **context, page_title="Search at " + seo_settings['default_page_title'], page_description=seo_settings['default_page_description'])

@app.route('/sim/<doi_prefix>/<doi_suffix>')
def sim(doi_prefix=None, doi_suffix=None):
    doi = f"{doi_prefix}/{doi_suffix}" # reconstruct the full doi
    pix = doi_to_ix.get(doi)
    if pix is None:
        papers = []
    else:
        sim_ix = sim_dict[pix]
        papers = [jall['rels'][cix] for cix in sim_ix]
    context = default_context(papers, sort_order='sim')
    return render_template('index.html', **context, page_title="COVID-19 Research AI Registry | Similar Papers", page_description="Similar Papers to " + papers[0][rel_title])


@app.route('/sitemap.xml')
def sitemap():
    pages = [{
        'url': 'http://biobe.betech.ai/',
        'lastmod' : jall['rels'][0]['rel_date'],
        'changefreq' : 'daily',
        'priority' : '1.0'
    },{
        'url': 'http://biobe.betech.ai/search',
        'lastmod' : jall['rels'][0]['rel_date'],
        'changefreq' : 'daily',
        'priority' : '1.0'
    }]

    for jal in jall['rels']:
        pages.append({
            'url' : 'http://biobe.betech.ai/sim/' + jal['rel_doi'],
            'lastmod' : jal['rel_date'],
            'changefreq': 'daily',
            'priority' : '0.8'
        })

    xml_from_sitemap = render_template('sitemap.xml', len=len(pages),pages=pages)
    xml_response = Response(response=xml_from_sitemap, status=200, mimetype="application/xml")
    xml_response.headers["Content-Type"] = "text/xml; charset=utf-8"
    return xml_response

@app.route('/')
def main():
    papers = jall['rels'][:40]
    context = default_context(papers, sort_order='latest')
    return render_template('index.html', **context, page_title= seo_settings['default_page_title'], page_description=seo_settings['default_page_description'])

