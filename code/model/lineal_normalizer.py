#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:39:51 2021

@author: cbadenes
"""

class Lineal_Normalizer():
    
    def __init__(self, multiplier=50):
        self.multiplier = multiplier
        
    def get_text(self, dictionary):
        text = ""         
        for key in dictionary:
            try:
                relevance = 0
                if (dictionary[key] > 0):
                    relevance = round(dictionary[key],3)
                if (relevance > self.multiplier):
                    relevance = self.multiplier
                frequency = int(self.multiplier * relevance)
                token = key.replace(" ","_")
                if (frequency < 1):
                    frequency = 1
                text += (" " + token)*frequency
            except OverflowError:
                print("OverflowError on frequency:" + str(dictionary[key]))
            except ValueError:
                print("ValueError on frequency:" + str(dictionary[key]))
        return text