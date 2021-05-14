#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 23:18:04 2021

@author: cbadenes
"""

import statistics
import json

def get_report(name,results):
    report = { 'name':name, 'sample': len(results)}
    print("Sample:",len(results))
    
    avg_precision = statistics.mean([result['precision'] for result in results])
    report['avg_precision'] = avg_precision
    print("Average Precision:", avg_precision)
    
    avg_recall = statistics.mean([result['recall'] for result in results])
    report['avg_recall'] = avg_recall
    print("Average Recall:", avg_recall)
    
    avg_fmeasure = statistics.mean([result['fmeasure'] for result in results])
    report['avg_fmeasure'] = avg_fmeasure
    print("Average F-Measure:", avg_fmeasure)
    


if __name__ == '__main__':  

    
    # print report
    input_file = open('../results/dev-results.jsonl', mode='r')
    output_file = open('../results/dev-report.jsonl', mode='w')    
    
    results = {}
    
    for line in input_file:
        eval_result = json.loads(line)
        strategy = eval_result['strategy']
        if (strategy not in results):
            results[strategy] = []
        results[strategy].append(eval_result)
    
    for strategy in results.keys():
        print("> Strategy:",strategy)
        report = get_report(strategy,results[strategy])
        output_file.write(json.dumps(report))
        output_file.write("\n")
    

    input_file.close()
    output_file.close()
    
    