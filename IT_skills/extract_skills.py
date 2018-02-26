# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:06:04 2018

@author: sylwia
"""
import numpy as np
import re
import pandas as pd


bulldog_skills = open('Scrappers/Skills/buldog_skills.txt').read().split('\n')
skills_hanscraped = open('Scrappers/Skills/additional_skills.txt').read().split(',')
#languages_wiki = open('Scrappers/Skills/IT_technologies_list.txt').read().split('\n')


#### skills list preprocessing
# words with '/' will be separated to two elements
additional_list = [s.split('/') for s in (bulldog_skills + skills_hanscraped) if '/' in s]
additional_list = [item.strip() for sublist in additional_list for item in sublist] # flaten it
# characters in '()' brackets will be treated as separated word
additional_list_2 = [s.replace(')', '').split('(') for s in (bulldog_skills + skills_hanscraped) if ('(' in s)]
additional_list_2 = [item.strip() for sublist in additional_list_2 for item in sublist]

skills_list = bulldog_skills +additional_list + additional_list_2 + skills_hanscraped
skills_list = [s.replace('.', ' ').strip() for s in skills_list]
skills_list = list(set(skills_list)) # to remove empty string which wast the first one



#### preprocess offers
offers =  open('Scrappers/Offers/offers_pracuj_pl.txt').read().split('\n')
for ch in ['/', ',', '.', '(', ')']:
    offers = [o.replace(ch,' ') for o in offers]    
# don't remove stopwords, as it may affect keywords (ruby ON rails, )



def find_skills(skl_list):
    skills_pattern = "[\s]" + "[\s]|[\s]".join(re.escape(skill) for skill in skl_list) +"[\s]"
    r = re.compile(r''+skills_pattern)
    skills_from_offers = [r.findall(o) for o in offers]
    return (skills_from_offers)

#################################################
# 1. Filter all technologies which have only one letter (R, C, ...?)
skills_one_letter = list(set([s.upper() for s in skills_list if (len(s)==1 and not s.isdigit())]))
skills_one_letter = ['C', 'R']
skills_list_one_letter = find_skills(skills_one_letter)

#################################################
# 2. Filter the rest of technologies (lower letter)
offers = [o.lower() for o in offers]
rest_skills = [s.lower() for s in skills_list]
excluded = ['i', 'it', '', ' ', 'developer', 'code', 'processing', 'plus', 'pl', 'sp', 'al', 'software'] + [s.lower() for s in skills_one_letter]
rest_skills = [s for s in rest_skills if (s not in excluded and not s.isdigit())]
rest_skills_list = find_skills(rest_skills)

#################################################
# 3. Merge two skills lists
merged_skills_list = [skills_list_one_letter[n] + rest_skills_list[n] for n in range(0,len(rest_skills_list))]
merged_skills_list = [list(set(s)) for s in merged_skills_list]

#################################################
# 4. Create sparse matrix of values
merged_skills_list = [s_list for s_list in merged_skills_list if len(s_list) > 1]
skills_to_blob = [item.strip() for sublist in merged_skills_list for item in sublist]
unique_merged_skills = list(set(skills_to_blob))

merged_skills_df = pd.DataFrame(0, index=np.arange(len(merged_skills_list)), columns = list(set(unique_merged_skills)))
for n in range(len(merged_skills_list)):
    for skl in merged_skills_list[n]:
        merged_skills_df.loc[n , skl.strip()] = 1


thefile = open('Scrappers/Skills/unique_skills.txt', 'w')
for skill in unique_merged_skills:
    thefile.write("%s\n" % skill)
thefile.close()

thefile = open('skills_to_blob.txt', 'w')
for skill in skills_to_blob:
    thefile.write("%s\n" % skill)
thefile.close()


thefile = open('Scrappers/Offers/offers_preprocessed.txt', 'w')
for skill in merged_skills_list:
    thefile.write("%s\n" % skill)
thefile.close()


merged_skills_array = np.array('')
for lst in merged_skills_list:
    np.append(merged_skills_array, " ".join(lst))