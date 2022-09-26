import streamlit as st
import pandas as pd
import numpy as np
import spacy as sp
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from spacy_streamlit import visualize_ner
from PIL import Image
from itertools import chain
import string
from io import BytesIO
import requests
import en_core_web_sm

nlp=en_core_web_sm.load()

#Logo
url = 'https://raw.githubusercontent.com/johnmorganbmw/languageassessor/main/IandDLogo_Shrunk.png'
response = requests.get(url)
image = Image.open(BytesIO(response.content))
st.image(image)

#Title
st.title("Gendered Language Assessment Tool")

#Data Import and preprocessing
url2 = 'https://raw.githubusercontent.com/johnmorganbmw/languageassessor/main/Gendered_Word_Key.csv'
key = pd.read_csv(url2)

male_words = key["Male-Coded"].tolist()

female_words = key["Female-Coded"].tolist()
del female_words[118:123]

male_nlp = [nlp(x) for x in male_words]
female_nlp = [nlp(x) for x in female_words]

matcher = PhraseMatcher(nlp.vocab)

matcher.add("MASCULINE",male_nlp)
matcher.add("FEMININE",female_nlp)

#Applying the gender recognition to our text
job = st.text_area("Copy and paste your text here.")

job_string = "".join(chain.from_iterable(job))

job_string = job_string.translate(str.maketrans('','', string.punctuation))

job_nlp = nlp(job_string)

matches = matcher(job_nlp)

for match_id, start, end in matches:
    # create a new Span for each match and use the match_id as the label
    span = Span(job_nlp, start, end, label=match_id)
    job_nlp.ents = list(job_nlp.ents) + [span]  # add span 

#Creates the final valuation
female_count = len([x for x in job_nlp.ents if x.label_ == "FEMININE"])
male_count = len([x for x in job_nlp.ents if x.label_ == "MASCULINE"])

if female_count - male_count == 0:
    result = "Neutral"
elif female_count > male_count and female_count - male_count < 3:
    result = "Leans Feminine"
elif female_count > male_count and female_count - male_count > 3:
    result = "Strongly Leans Feminine"
elif female_count < male_count and male_count - female_count < 3:
    result = "Leans Masculine"
elif female_count < male_count and male_count - female_count > 3:
    result = "Strongly Leans Masculine"
else: result = "Error!"

st.header("Gendered Language Result")
result_metric = st.metric(value=result)

#Renders the text with the gendered text flagged
colors = {"FEMININE" : "#66c2c0", "MASCULINE" : "#fce27a"}
st.header("Flagged Language")
visualize_ner(job_nlp, labels= ["MASCULINE","FEMININE"] , displacy_options = {"colors" : colors},show_table = False)
