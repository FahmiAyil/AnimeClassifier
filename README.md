# AnimeClassifier
1. Anime Classifier used to classify synopsis of anime, so we can know, what is the appropriate genre for the anime.
2. Using Naive Bayes to classifying synopsis.
3. Using Porter Stemmer
4. Using lxml webscrape to scrape website [MyAnimeList](https://myanimelist.net/anime.php)

# How to run program
* Make sure you have import the database '''animelist.sql'''
* Run Conn.py to check the database has been connected
* Run Scrape.py to start scrape site [MyAnimeList](https://myanimelist.net/anime.php)
* Run Filestem.py to start the text preprocessing techniques (Casefolding, Tokenizing, Stopword Removal, Stemming)
* Run Classifier.py to identify a new synopsis and classify genre by a new synopsis using Naive Bayes algorithm
