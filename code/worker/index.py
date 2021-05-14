#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:36:24 2021

@author: cbadenes
"""
import model.text_rank as tr
import model.lineal_normalizer as lnormalizer
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import es_core_news_lg
import requests
from itertools import groupby
import re
import collections


nlp = es_core_news_lg.load()


textrank = tr.TextRank()
normalizer = lnormalizer.Lineal_Normalizer()

pos_list = ['NOUN', 'PROPN', 'ADJ', 'VERB','INTJ']
stopword_list=["ANTECEDENTES","ANTECEDENTE","Antecedentes","Antecedente",
                   "OBJETIVOS","OBJETIVO","Objetivo","Objetivos",
                   "RESULTADOS","RESULTADO","Resultado","Resultados",
                   "MÉTODOS","METODO","Método","Métodos",
                   "CONCLUSIONES","CONCLUSION","Conclusiones","Conclusion",
                   "EVALUACIÓN","evaluación"
                   "ANTECEDENTES/OBJETIVO",
                   "INTRODUCCIÓN","Introduccion",
                   "RESUMEN","Resumen",
                   "estudio",
                   "año"]

"""Set stop words"""
for word in STOP_WORDS.union(set(stopword_list)):
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True

    
def get_tokens(text,entity_map={},lower=False):
    doc = nlp(text)
    sentences = []
    current_offset = 0
    
    #general entities
    for entity in doc.ents:
        if (":" in entity.text):
            continue            
        entity_map[entity.start_char]=entity.text.replace(" ","_")
    
    
    for sent in doc.sents:
        selected_words = []
        for token in sent:
            # Store words only with cadidate POS tag
            if (token.idx in entity_map):
                entity = entity_map[token.idx]
                current_offset = token.idx + len(entity)
                selected_words.append(entity.replace(" ","_"))              
            elif token.idx > current_offset and token.pos_ in pos_list and token.is_stop is False:
                current_offset = token.idx + len(token.lemma_)
                if lower is True:
                    selected_words.append(token.lemma_.lower())
                else:
                    selected_words.append(token.lemma_)                            
        sentences.append(selected_words)
    return sentences


def create_document(article,track,entities,scope='default',lower=False):
    document = {}
    document['id'] = article['id']
    document['track_s'] = track
    document['title_s'] = article['title']
    document['abstract_t'] = article['abstractText']
    document['journal_s'] = article['journal']
    document['size_i'] = len(article['abstractText'])
    year = article['year']
    if ( year == 'Not Available'):
        year = -1
    document['year_i'] = year
    document['db_s'] = article['db']
    if ('decsCodes' in article):
        document['codes'] = article['decsCodes']
    document['scope_s'] = scope
    document['diseases'] = [entity['span'].replace(" ","_") for entity in entities['diseases']]
    document['medications'] = [entity['span'].replace(" ","_") for entity in entities['medications']]
    document['procedures'] = [entity['span'].replace(" ","_") for entity in entities['procedures']]
    document['symptoms'] = [entity['span'].replace(" ","_") for entity in entities['symptoms']]
    
    #medical entities
    entity_map = {}
    for entity in entities['diseases']:
        entity_map[int(entity['start'])]=entity['span']
    for entity in entities['medications']:
        entity_map[int(entity['start'])]=entity['span']
    for entity in entities['procedures']:
        entity_map[int(entity['start'])]=entity['span']
    for entity in entities['symptoms']:
        entity_map[int(entity['start'])]=entity['span']
    
    #tokens
    text = ""
    #if (len(document['title_s']) > 1):
    #    text +=  document['title_s'] + "."
    if (len(document['abstract_t']) > 1):
        text += document['abstract_t']
    tokens = get_tokens(text,entity_map,lower)
    document['tokens'] = tokens
    bow = get_bow(tokens)
    article['bow_t']=bow
    return document    

def evaluate_result(reference,data):
    tp = 0
    fp = 0
    fn = 0
    for result in data:
        if (result in reference):
            tp += 1
        else:
            fp += 1
    for value in reference:
        if (value not in data):
            fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fmeasure = 2 * ( (precision * recall) / (precision + recall)  )
    return { 'tp': tp, 'fp': fp, 'fn': fn, 'precision': precision, 'recall': recall, 'fmeasure':fmeasure}


def evaluate(text,codes):
    print("getting topic distribution for codes",codes)
    response = requests.post("http://localhost:8080/classes", json = { 'text':text})
    
    data = response.json()
    
    labels0 = []
    labels1 = []
    labels2 = []
    for topic in data:
        if (topic['id']== 0):
            labels0.append(topic['name'])
        elif (topic['id']== 1):
            labels1.append(topic['name'])    
        else:     
            labels2.append(topic['name'])
    
    result0 = evaluate_result(codes, labels0)
    labels0.extends(labels1)
    result01 = evaluate_result(codes, labels0)
    labels0.extends(labels2)
    result012 = evaluate_result(codes, labels0)
    return { 'result0': result0, 'result01': result01, 'result012':result012}
    
def inference(id,text):
    print("getting topic distribution for",id)
    response = requests.post("http://localhost:8080/classes", json = { 'text':text})
    
    data = response.json()
    
    labels0 = []
    labels1 = []
    labels2 = []
    for topic in data:
        if (topic['id']== 0):
            labels0.append(topic['name'])
        elif (topic['id']== 1):
            labels1.append(topic['name'])    
        else:     
            labels2.append(topic['name'])
    
    label0_res = { 'id':id, 'labels': labels0}
    labels0.extend(labels1)
    label1_res = { 'id':id, 'labels': labels0}
    labels0.extend(labels2)
    label2_res = { 'id':id, 'labels': labels0}
    
    return { 'result0': label0_res, 'result1': label1_res, 'result2':label0_res}    
    
    
def categorize(article, hierarchy):
    for code in article['codes']:
        hierarchy_code = hierarchy[code]
        deep = hierarchy_code['deep']
        code_label = 'codes'+str(deep)
        if (code_label not in article):
            article[code_label]=[code]
        else:
            article[code_label].append(code)
    return article
    
def get_bow(tokens):
    string_check= re.compile('[@!#$%^&*()<>,=?/\|}{~:]')
    num_words = 4
    count = 0
    for list_tokens in tokens:
        count += len(list_tokens)
    keywords = textrank.get_keywords(tokens,num_words,count)
    #normalized_text = normalizer.get_text(keywords)
    bow = ""
    for key in keywords:        
        try:
            token = key.replace(" ","_")
            if (len(token)>1) and (string_check.search(token) == None):
                relevance = 0
                multiplier = 50
                if (keywords[key] > 0):
                    relevance = round(keywords[key],3)
                if (relevance > multiplier):
                    relevance = multiplier
                frequency = int(multiplier * relevance)                
                if (frequency < 1):
                    frequency = 1
                bow += key+"="+str(frequency)+"#NOUN# "
        except OverflowError:
            print("OverflowError on frequency:" + str(keywords[key]))
        except ValueError:
            print("ValueError on frequency:" + str(keywords[key]))
    return bow

def create_bow(article):
    tokens = []
    if ('tokens' in article):
        tokens = article['tokens']
    if ('sentences' in article):
        tokens = article['sentences']
        article.pop('sentences')
        article['tokens'] = tokens
    if ('tokens_t' in article):
        article.pop('tokens_t')
    bow = get_bow([tokens])
    article['bow_t']=bow
       
    return article
    
    
    