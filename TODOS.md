TO DO LIST :

- [] COLLECT MORE TWEET FOR MORE ANALYSIS
- [x] REFRACTOR PREPROCESSING STEP
- [x] WORK ON TOPIC MODELING
- [x] EMBEDED IT REAL TIME PROCESS WITH A DATABASE (check apache airflow)
- [x] Learn about topic modeling and write the first draft of that blog post
- [x] Refractor the twitter to collect geograhpical data about the blog
- [] refractor the blog post and put in a publishable state.
- [x] find a way to run the streaming code at midnight and collect tweets for one date
- [x] ask question on SO about how to retrieve data about the country
- [x] other step for cleaning
- [x] Remove one word or 2 words strings and charcteres
- [x] Remove kinshasa
- [x] [for each word in a topic plot the distribution]
- [x] Read Aspitel project and check how she implemented it
- [x] create the django or flask project and plan the deployment
- [] write unittest for project
- [] refractor the project and make it maintainable
- [] get geocode location for all cities in DRC
- [x] fix the issue of retrieving tweets by date
- [x] use apache airflow to run cron jobs and data retrieval task at a specific time in a day
- [] Deploy everything to DO
- [] Improve the processing by removing Congolese names from stematization
- [x] Add a job that tweet the word count everyday after getting it
- [] Create a job that goes to every tweet and collect all the replies about it
- [] Get all the data for year 2020 and save it in a raw json file without cleaning
- [] Save the data to json file without cleaning
- [] https://dagshub.com/ investigate the usage of this
- [] Move the project from Airflow to Prefect or Any other workflow manager
- [] get all the tweets from my timeline
- [] Add a script to intialize the database migration

### DRC Coordinates

The whole country
[11.94,-13.64,30.54,5.19]

## PostModern Feb 2023

I finally get time to touch on this project after around 6 month of it being down.
It took me around a day to setup a new server and to get the project running again.
The github action are back working but there have been a lot of learning since the last time I worked on this project.

I would like to improve it by adding new tools.

HEre is the next road map.

Before adding new features to the project I would like to replace Airflow with Perfect as workflow manager.
Replace Docker with Kubernetes as container manager.
Then add more feature and improve the modelling aspect of the project.

## Update November 2023

A lot happens since I touch on this project, the DRC election are approaching and I was thinking to use it again, but unfortunately the twitter api is no longer free and they are requesting to 100 USD. Should I pay 100 USD for a research project, nannnnnnn! Elon will not take my money.

I searched and I found this cool tool: https://github.com/vladkens/twscrape/?tab=readme-ov-file and one of those days I would like to try it to scrape twiter data without using the API.
