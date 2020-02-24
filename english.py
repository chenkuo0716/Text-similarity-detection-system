#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from gensim import models, similarities, corpora

def English(documents):
    # Log
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # Reference text file processing
    texts = [[word for word in document.lower().split()] for document in documents[1:]]
    print(texts)

    # Statistically restricted word frequency
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts1 = [[token for token in text if frequency[token] > 1] for text in texts]
    print(texts1)

    # Build a corpus
    dictionary = corpora.Dictionary(texts1)
    print(dictionary.token2id)

    # Doc2bow the dictionary to get a new corpus
    corpus = [dictionary.doc2bow(text) for text in texts1]

    # Building a TF-IDF model
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print(doc)

    # Depth-first search
    print(tfidf.dfs)
    print(tfidf.idfs)

    # Training the Lsi model
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
    lsi.print_topics(2)

    # Map documents into two-dimensional topic space with Lsi model
    corpus_lsi = lsi[corpus_tfidf]
    for doc in corpus_lsi:
        print(doc)

    # Calculate sparse matrix similarity
    index = similarities.MatrixSimilarity(lsi[corpus])

    # Object text file processing
    query = documents[0]
    print(query)

    # doc2bow builds a bag of words model, turning the file into a sparse vector
    query_bow = dictionary.doc2bow(query.lower().split())
    print(query_bow)

    # Map documents into 2D topic space with Lsi model
    query_lsi = lsi[query_bow]
    print(query_lsi)

    # Calculate cosine similarity
    sims = index[query_lsi]
    sims = list(sims)
    return sims
