# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:56:59 2018

@author: sylwia
"""
import numpy as np 
from os import path
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = open('skills_to_blob.txt').read()

mask = np.array(Image.open(path.join("cloud.png")))

# graphisc source: https://pixabay.com/pl/chmura-pogoda-s%C5%82abe-glif-symbolu-1672676/
wc = WordCloud(background_color="white", colormap = 'magma', max_words=300, mask=mask,  relative_scaling=1, font_path= '/home/sylwia/Downloads/alpha_echo.ttf')
# generate word cloud
wc.generate(text)

wc.to_file(path.join("word_cloud.png"))

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()