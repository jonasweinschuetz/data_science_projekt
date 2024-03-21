# Feeding the Academic Appetite: Price Dynamics and Dietary Trends of German Canteens

## About this Project

This project aims to collect, analyze, and evaluate data from german educational canteens and cafeterias. The project primarily focuses on prices and the distribution of vegan, vegetarian, and meat/omnivorous dishes that are offered in the canteens. 



## Repository Structure 

### Directories

- [data](https://github.com/jonasweinschuetz/data_science_projekt/tree/main/data): contains the cleaned and transformed datasets used during data analysis as well as the raw data collected at the begining of our journey
- [data_acquisition](https://github.com/jonasweinschuetz/data_science_projekt/tree/main/data_acquisition): a collection of scripts used to collect the raw data
- [data_cleaning](https://github.com/jonasweinschuetz/data_science_projekt/tree/main/data_cleaning): a collection of scripts used to clean and transform the raw data, the main work is done by the *open-mensa-json-to-pandas-csv.py* script
- [app.py](https://github.com/jonasweinschuetz/data_science_projekt/blob/main/app.py) and [pages](https://github.com/jonasweinschuetz/data_science_projekt/tree/main/pages): files that belong to the dash application call this directory their home, *app.py* is the main script that launches the dash web app
- [presentation+poster](https://github.com/jonasweinschuetz/data_science_projekt/tree/main/presentation_and_poster): files related to the visualization of our findings, this includes the presentation slides and the poster




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


## Dependencies

This project uses Python 3.x and the following libraries:

- Pandas for data manipulation and analysis
- NumPy for numerical computations
- Matplotlib and Seaborn for data visualization
- Scikit-learn for machine learning and outlier detection

To install the dependencies, run the following command in your terminal or command prompt:




## Chalenges 

### Data Collection

#### Webscraping

The web-scraped dataset was obtained from one of our classmates, [Lia Lenckowski](https://github.com/llenck). Her web scraper queries the subpages of the Studentenwerk SH responsible for the meal plan of each university. Each of these subpages can be passed an argument representing one of the canteens that the university has. Then, only the container containing the meal table needs to be extracted from the received HTML, and the dishes are loaded into a JSON-lines file. Since the canteens always provide their weekly schedule, a request is made for each canteen of each university of the Studentenwerk once a week.

### Data Cleaning

The data cleaning process was relatively straightforward. To work with dish names and tags more effectively, we converted them to lowercase and filtered out line breaks and other special characters. The biggest issue we encountered was with prices. Unfortunately, there are canteens where one, two, or sometimes even all price tiers were missing. We suspect that this is due to some canteens, for example, having a single price for all their customers, which was then only recorded in the guest price line. We considered how to fill these gaps but ultimately decided not to consider missing prices for the respective price class calculation. It is particularly unfortunate that in the OpenMensa database, there were no data entries for Berlin and Bremen, which is why these two states cannot be found in our price statistics. The last point, which unfortunately came to our attention too late, is that in many canteens in Lower Saxony, almost 10 times as many dishes are found in the database on Fridays compared to the other weekdays. Unfortunately, we did not have the time to investigate potential causes of this phenomenon, but please keep this fact in mind when reviewing weekday-specific data from Lower Saxony.

### Data Transformation 

The main issue lay in categorizing the data into vegan, vegetarian and omnivorous dishes (vvo categories). TODO
