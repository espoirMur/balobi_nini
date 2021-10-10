[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

## Table of Contents

- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## About The Project

_What did they say? or What are they talking about in Lingala_

Finally this project is taking shape , I finally found what I am building....

Among multiple concepts I am testing on this project!

Here are some feature that are working in this repository:

- This project use Tweepy alongside with Apache Airflow to collect all tweets containing the words RDC and DRC on a hourly basis.

- Once those tweets are collected I apply some cleaning on them and generate a WordCloud to display the most used word by Congolese on Social Media on a given day.

- Again I use Airflow and Celery as scheduler to tweet that WordCloud generated on a daily basis...

- I used StreamIt to display that WordCloud as an image on a web page.

The other feature I will be implementing next time are :

- Using Topic Modeling to identify the different topic used in those tweets.
- Using Sentiment analysis and display the sentiment in the congolese tweets.

- Once I got those results I will be updating the StreamLit dashboard...

<!-- Build with -->

## Built With

- [Python](https://www.python.org/)
- [Tweepy](https://github.com/tweepy/tweepy)
- [Airflow](https://github.com/apache/airflow)
- [NLTK](https://www.nltk.org/)
- [Github Actions](https://github.com/features/actions)
- [streamlit](https://streamlit.io/)

<!-- GETTING STARTED -->

## Getting started

Clone the project to have a local copy in your machine.

We have decided to use docker to build and have the project running...

### Install Redis

The project use redis as broker, install it and get it running using this [link](https://www.ubuntupit.com/how-to-install-and-configure-redis-on-linux-system/)

### Install Postgres

The project also use postgres as database , install it and create a database for the project. Keep it's name somewhere for future use.

Follow this [URL](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e) to create a user and a database

### Generate the .env file

`cp .env.sample .env`

### Run Docker

Make sure you have docker installed and running and docker-compose and then go inside the project directory and run :

`docker-compose up -d --build`

Then chill until I get motivation to finish this readme

Update the database using this command :

`docker-compose exec streamlit-instance python manage.py db upgrade`

<!-- road map -->

## Roadmap

Anytime I learn something new I would like to apply it on this project.

I made a Todo list about item I will work on on this project.

It depend on my motivation and my mood and how I feel when working on this project ...

But the Todo can be found [here](./TODOS.md)...

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under my personal open source licence. See [`LICENSE`](./LICENSE.md) for more information.

<!-- CONTACT -->

## Contact

Espoir Murhabazi - [@olobi_nini](https://twitter.com/olobi_nini) - espoir.mur on gmail

Project Link: [https://github.com/espoirMur/balobi_nini](https://github.com/espoirMur/balobi_nini)

<!-- ACKNOWLEDGEMENTS -->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/espoirMur/balobi_nini/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/espoirMur/balobi_nini/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/espoirMur/balobi_nini/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/espoirMur/balobi_nini/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/espoirMur/balobi_nini/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/murhabazi-buzina-espoir-7849b1b1/
[product-screenshot]: images/screenshot.png
