# How has the average price for a meal in Schleswig-Holstein changed since 2021? 

## Exploring Meal Price Changes in Schleswig-Holstein Since 2021

To explore this research question we build a data set for all canteens in Schleswig-Holstein. This data set dates back to 2021 and is merged from the OpenMensa API and web scraped data. Since 2021, the dynamics of meal pricing within Schleswig-Holstein's canteens have undergone noticeable changes. Here we analyse different aspects: geographical (by city), status-based (student, employee, guest), and dietary categories (vegan, vegetarian, omnivorous). We aim to unravel the intricacies of these pricing adjustments.

### Impact of location on price change

Looking at the average meal pricing data of the cities it reveals that each city within Schleswig-Holstein exhibited significant price changes. Kiel, Flensburg, and Heide have shown a steady increase in meal prices. Lübeck presents an interesting case with the smallest price increase by EUR, but only an slightly smaller percentage increase than the rest, indicating that the local pricing in general seems to be cheaper. 

![rq1_city_1](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/1bc7cb1d-f8db-49bc-9240-cc0e7d682dc6)

![rq1_city_2](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/adbc7d75-cb3f-4c90-9511-ab8e65464fbc)

**Average price change (per year since 2021)**

| Location             | Price Increase (€/Year) | Percentage Increase (\%/Year) |
|----------------------|-------------------------|-------------------------------|
| Kiel:                | 0.41 €                  | 10.41 \%                      |
| Flensburg:           | 0.42 €                  | 11.05 \%                      |
| Lübeck:              | 0.16 €                  | 8.67 \%                       |
| Heide:               | 0.47 €                  | 9.36 \%                       |
| **Schleswig-Holstein:** | 0.36 €              | 9.87 \%                       |

In 2022 and 2023, meal prices in Schleswig-Holstein (SH) rose significantly, yet remained below the German food inflation rate. There are some interesting aspects about each city, such as the big differences of both years in Flensburg and Lübeck. However, we can see an overall increasing trend in both years.

| Location          | 2022   | 2023  |
|-------------------|-------|-------|
| Kiel:             | 8.7 %  | 12.4 % |
| Flensburg:        | 1.7 %  | 9.8 %  |
| Lübeck:           | 15.8 % | 6.8 %  |
| Heide:            | 11.8 % | 12.2 % |
| **SH:**           | 9.5 %  | 10.3 % |
| **Food Inflation:** | 13.4 % | 12.4 % |

_Food Inflation = Germany-wide food inflation rate ([destatis.de](https://destatis.de))_

## Impact of visitor status on price change

A closer examination of the meal price changes based on the visitors status (student, employee, guest) reveals a nuanced impact. Guests saw an yearly increase of 10.92 % (0.47 €), employees experienced a 10.47 % rise (0.42 €), and students faced the highest jump at 10.94 % (0.31 €). This tiered pricing model reflects the canteens' efforts to balance affordability during inflation for students, employees, and guests.

![rq1_visirors_1](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/ff53bbbf-0f61-470a-8e90-d4f04b52bd34)

## Impact of dietary categories on price change

The analysis extends to the variations in meal prices across different dietary categories: vegan, vegetarian, and meat-based meals. The data highlights a surprising trend towards higher price adjustments for vegan meals, followed by meat-based and lastly vegetarian options. Specifically, vegan dishes saw an average yearly price change of 18.33 % (0.54 €), contrasting with the more modest increases for meat-based (16.84 %, 0.67 €) and vegetarian (15.41 %, 0.48 €) meals. This pattern could reflect the rising costs of vegan food production, alongside growing demand for plant-based diets among the student population. However, the average prices could be slightly missleading because of some outliers as can be seen in the graph. Looking at the trend lines and their slope, we can deduct, that 

![rq1_category_1](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/098cc59f-f387-4521-8b11-e48dde3c1c4a)

![rq1_category_2](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/64441c51-b427-4268-8f15-cb89754f7d5e)
