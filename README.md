# Client Project: Mapping Coronavirus Sentiment
Jonathan Cheung, Rahul Kaw, Wesley Miller, Roxana Ruvalcaba


### Problem Statement
Can we predict the severity of the COVID outbreak in a region using Twitter data? Specifically, can we accurately label and predict a tweet's sentiment, and is that information related to the COVID-19 outbreak severity?

The original problem statement stated that the data released regarding instances of the COVID-19 pandemic is aggregated before it is released to (legally and ethically) protect the privacy of those involved. Unfortunately, this takes away some of the utility of the data. The question we were to answer was; can we use social media to narrow the location of cases while still protecting individual privacy rights?  We initially attempted to utilize reddit information as well, but decided to stick with twitter scraper as early data analysis with reddit information was inconclusive.

### Executive Summary
Twitter sentiment data from California cities is currently not a good predictor of the extent of the Covid outbreak. To analyze the problem, we leveraged NLTK, sPacy, TextBlob, and Folium libraries to analyze tweet sentiment on a regional level, and then to compare it to regional coronavirus cases data. For the first model, we used sPacy and nltk.opinion lexicon to label and predict tweet sentiment. For the second model, we used NLTK and TextBlob to label tweet sentiments then pipeline GridSearched a Logistic Regression to predict tweet sentiment. The tweets used as input for the models were pulled from seven California cities. The results of the first model were then plotted on a map with actual LA Times coronavirus data. The models did a good job predicting sentiment, however we did not find a strong relationship between tweet sentiment status and Covid-19 outbreak cases. For next steps, we recommend gathering more location data and to further refine the sentiment labels.

### Contents
- [Twitter and Reddit APIs](./code)
- [Final Notebooks and Maps](./notebook)
- [Presentation Slides](./Mapping%20Coronavirus%20Sentiment.pdf)

### Conclusion
The models performed well in predicting the sentiment of a tweet once tweets were labeled as being negative, neutral or, positive. However, we were unable to find any clear relationships between twitter sentiment and the severity of an outbreak in a region when the data was mapped and compared, and thus couldn’t predict the severity of an outbreak through tweets. While labeling sentiment, there were many conflating factors getting in the way of making any assertions regarding twitter sentiment’s relationship with coronavirus outcomes. As next steps, we recommend refining the tweet sentiment labels either by further cleaning the data, or manually labelling if resources are available. In particular utilizing additional computing power for modelling via an external resource, and gathering data with more tweet locations, seem like clear next steps. As additional tools, please also view the map prototypes the team created using actual coronavirus data from the LA Times.
