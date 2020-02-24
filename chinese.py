#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import jieba
from gensim import models, similarities, corpora
from collections import defaultdict

def Chinese(txt_name):
    # Log
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # Reference text file processing
    # jieba participle
    data = []
    for t in txt_name[1:]:
        txt = open(t, encoding='utf-8').read()
        data.append(jieba.cut(txt))
    data_new = []
    doc1 = []
    for t in data:
        data_temp = ''
        for i in t:
            data_temp += i + " "
        data_new.append(data_temp)
    for t in data_new:
        doc1.append(t)
    texts = [[word for word in doc.split()]
          for doc in doc1]

    # Statistically restricted word frequency
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts1 = [[token for token in k if frequency[token] > 2]
          for k in texts]
    print(texts1)

    # Build a corpus
    dictionary = corpora.Dictionary(texts1)
    dictionary.save("/Users/ck/Documents/学习资料/毕业设计/代码/示例文本/yuliaoku.txt")

    # Object text file processing
    f = txt_name[0]
    c = open(f, encoding='utf-8').read()

    # jieba participle
    data0 = jieba.cut(c)
    data00 = ""
    for i in data0:
        data00 += i + " "
    new_doc = data00
    print(new_doc)

    # doc2bow builds a bag of words model, turning the file into a sparse vector
    new_vec = dictionary.doc2bow(new_doc.split())

    # Further processing the sparse vector to obtain a new corpus
    new_corpor = [dictionary.doc2bow(t3) for t3 in texts1]

    # Building a TF-IDF model
    tfidf = models.TfidfModel(new_corpor)

    # Calculate the number of features
    featurenum = len(dictionary.token2id.keys())

    # Calculate sparse matrix similarity
    index = similarities.SparseMatrixSimilarity(tfidf[new_corpor], num_features=featurenum)

    # Calculate cosine similarity
    sims = index[tfidf[new_vec]]
    sims = str(sims).replace('[', '').replace(']', '').split(' ')
    if '' in sims:
        sims.remove('')
    return sims
