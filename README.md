# Feeding the Academic Appetite: Price Dynamics and Dietary Trends of German Canteens

## About this Project

This project aims to collect, analyze, and evaluate data from german educational canteens and cafeterias. The project primarily focuses on prices and the distribution of vegan, vegetarian, and meat/omnivorous dishes that are offered in the canteens. 


------

## Repository Structure 

### Directories

- __data__: contains the cleaned and transformed datasets used during data analysis as well as the raw data collected at the begining of our journey
- __data_acquisition__: a collection of scripts used to collect the raw data
- __data_cleaning__: a collection of scripts used to clean and transform the raw data, the main work is done by the *open-mensa-json-to-pandas-csv.py* script
- __app.py__ and __pages__: files that belong to the dash application call this directory their home, *app.py* is the main script that launches the dash web app
- __presentation+poster__: files related to the visualization of our findings, this includes the presentation slides and the poster



------

## The Dataset

The data primarily consist of two datasets: a smaller web-scraped dataset from universities in Schleswig-Holstein, which we scraped from the  [official website](https://studentenwerk.sh/de/mensen-in-kiel) of the state's student service, and a nationwide dataset collected using the [OpenMensa API](https://docs.openmensa.org/). The scraping began in mid-2022 and continued until early March 2024. The second dataset mostly extends only until the beginning of the year 2023; however, for the locations also represented in the first set, we collected retrospective data up to the year 2021 to gain a better understanding of long-term price trends. We would have liked to gather extensive data for the remaining canteens in Germany as well, but we decided against it, as the data collection process would otherwise have taken up too much time.


Each data point represents a dish that was offered on a particular day. Each entry includes the following details: 
- the unique ID of the canteen where the dish was sold
- the city where the canteen is located
- the unique ID of the dish within the location
- the name of the dish
- the date the dish was sold
- the price at which the dish was offered (for students, employees, and guests respectively)
- a list of tags providing additional information about the dish

Additionally, we also determined the corresponding federal state for each dish using Wikipedia's list of the German cities.

------

## Dependencies

This project uses Python 3.x and the following libraries:

- Pandas for data manipulation and analysis
- NumPy for numerical computations
- Matplotlib and Seaborn for data visualization
- Scikit-learn for machine learning and outlier detection

To install the dependencies, run the following command in your terminal or command prompt:


------


## Chalanges 

### Data Collection
### Data Cleaning
### Data Transformation 

The main issue lay in categorizing the data into vegan, vegetarian and omnivorous dishes (vvo categories). TODO
