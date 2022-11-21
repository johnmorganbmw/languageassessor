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
import plotly.graph_objects as go

nlp=en_core_web_sm.load()

###Logo###
from PIL import Image
url = 'https://raw.githubusercontent.com/johnmorganbmw/languageassessor/main/IandDLogo_Shrunk.png'
response = requests.get(url)
image = Image.open(BytesIO(response.content))
st.image(image)

###Title###
st.title("Gendered Language Assessor")

###Data Import and preprocessing###
url2 = 'https://raw.githubusercontent.com/johnmorganbmw/languageassessor/main/Gendered_Word_Key.csv'
key = pd.read_csv(url2)

male_words = key["Male-Coded"].tolist()

female_words = key["Female-Coded"].tolist()
del female_words[118:123] #removes the blanks at the end of the column

male_nlp = [nlp(x) for x in male_words] #applies the spacy processing
female_nlp = [nlp(x) for x in female_words]

matcher = PhraseMatcher(nlp.vocab) #performs named entity recognition

matcher.add("MASCULINE",male_nlp) #adds the male terms for the NER
matcher.add("FEMININE",female_nlp) #adds the female terms for the NER

###Applying the gender recognition to our text###
job = st.text_area("Copy and paste your text here.") 

job_string = "".join(chain.from_iterable(job)) #converts the copy and pasted text into something understandable

job_string = job_string.translate(str.maketrans('','', string.punctuation)).lower() #removes punctuation and lowercasifies

job_nlp = nlp(job_string) #applies spacy processing to the pasted text

matches = matcher(job_nlp) #Applies the NER with our gendered terms

for match_id, start, end in matches:
    # create a new Span for each match and use the match_id as the label
    span = Span(job_nlp, start, end, label=match_id)
    job_nlp.ents = list(job_nlp.ents) + [span]  # add span 

#Creates the overall evaluation (just adding the totals and comparing)
female_count = len([x for x in job_nlp.ents if x.label_ == "FEMININE"])
male_count = len([x for x in job_nlp.ents if x.label_ == "MASCULINE"])

if female_count - male_count == 0:
    result = "Neutral"
elif female_count > male_count and female_count - male_count < 3:
    result = "Leans Feminine"
elif female_count > male_count and female_count - male_count >= 3:
    result = "Strongly Leans Feminine"
elif female_count < male_count and male_count - female_count < 3:
    result = "Leans Masculine"
elif female_count < male_count and male_count - female_count >= 3:
    result = "Strongly Leans Masculine"
else: result = "Error!"

st.header("Gendered Language Result")
result_metric = st.metric(label="",value=result) #the result from the if statement

###Summary Pie Chart###
colors = ["#fce27a","#66c2c0"]

fig = go.Figure(data=[go.Pie(labels=['Masculine','Feminine'],
                             values=[male_count,female_count])])
fig.update_traces(hoverinfo='label', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors))

st.plotly_chart(fig, use_container_width=True)


#male_metric = st.metric(label="Male Count",value=male_count)
#female_metric = st.metric(label="Female Count",value=female_count) #used these for debugging, currently they do not appear in the final app

st.text("") #blank line to make the app look nicer

###Renders the text with the gendered text flagged###
colors = {"FEMININE" : "#66c2c0", "MASCULINE" : "#fce27a"}
st.header("Flagged Language")
visualize_ner(job_nlp, labels= ["MASCULINE","FEMININE"] , displacy_options = {"colors" : colors},title = "",show_table = False)

st.text("") #blank line to make the app look nicer

###Word Replacement Recommendation###
st.header("Recommended Word Replacements")

entities = [(e.label_,e.text) for e in job_nlp.ents] #pulls out all entities
df_matches = pd.DataFrame(entities, columns=['Language','Word']).query("Language=='MASCULINE'").drop("Language",axis=1) #saves them as a dataframe and just keeps the masculine words

key2 = key.drop("Female-Coded",axis=1) #creates a key of just the recommendations for masculine words
df_merged = df_matches.merge(key2.rename({'Male-Coded': 'Word'}, axis = 1), on = "Word", how = "left").drop_duplicates() #joins the matches and recoommended replacements

#sneaking some CSS in to hide the row index in the below table
hide_table_row_index = """ 
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(df_merged) #the recommendations table
