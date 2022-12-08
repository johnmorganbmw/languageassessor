# Gendered Language Assessor

## Purpose
This app was the Bias Busters' winning submission to the BMW Group/ekipa's Joyful Diversity with AI Challenge in Sep-Dec 2022. The purpose is primarily to improve the appeal of job postings for women to ensure qualified applicants feel confident in applying while serving as an example of how we can automatically assess the language we use to maximise outcomes we want to see.

## Functional Details
The functional app can be viewed here: https://bit.ly/3fol8Aw. It is coded in Python using Streamlit and runs on Streamlit cloud. The named entity recognition uses spaCy and a dictionary of gendered terms adapted from "Evidence That Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality" by Gaucher, Friesen, & Kay (2011).

## Usage
To use the tool, copy and paste in the text from a job posting and the app will highlight masculine/feminine language and provide an overall score for the posting. According to the underlying research, women will find postings with more masculine language to be less appealing and be less likely to apply (men are undeterred by feminine language). If your result shows that the language leans masculine, consider changing the language to be more collaborative rather than individualistic. The app will issue a list of recommended replacement words at the bottom to help you make these changes.

## Future Development
The app in its current form is planned to stay publicly available. Future development internal to BMW will incorporate an algorithmic backend as specified in "Balancing Gender Bias in Job Advertisements With Text-Level Bias Mitigation" by Hu et al. (2022) and translate the app to other languages by training various word embedding models. This expansion will most likely not be publicly available.
