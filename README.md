# Twitter-Analysis-For-DRC

I really don't know how to name this project , I just want to work on something related to social media data analysis for DRCongo.

Basically, In this project the ideas is to collect tweet related to DRC analyze and check what we can do with them.

Some interesting topics we could do are :

- Sentiment analysis of comment to a particular topic.
- Content analysis , with this I mean trying to understand what Congelese are talking about on social media.
- Disease prevention using social media analysis. (Basically using time series analysis to predict ebola outbreak in a region.)
- Another interesting will be to use the streaming api to fetch data daily and retrieve what people are talking about.
- We can use twitter data to find what are the most popular Influencer (persons or businesses) on twitter
- Using twitter data to visualize the most hashtags used by Congoleses

I will be sharing more topics with time.

Some resources I'm using are :

- [This One](https://www.researchgate.net/publication/303127692_SOCIAL_MEDIA_MINING_FOR_PUBLIC_HEALTH_MONITORING_AND_SURVEILLANCE)
- [And this One](https://www.ncbi.nlm.nih.gov/pubmed/26042846)
- [chap 1 and Chap 2 of This Book](https://www.amazon.com/Mastering-Social-Media-Mining-Python-ebook/dp/B01BFD2Z2Q)

#### How to run the project

We have decided to use docker to build and have the project running...

Make sure you have docker installed and running and docker-compose and then go inside the project directory and run :

`docker-compose up -d --build`

Then chill until I get motivation to finish this readme

Update the database using this command :

`docker-compose exec streamlit-instance python manage.py db upgrade`
