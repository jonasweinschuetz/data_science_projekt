# How has the average price for a meal in Schleswig-Holstein changed since 2021? 

## Exploring Meal Price Changes in Schleswig-Holstein Since 2021

To investigate the question of how meal prices of canteens have evolved in Schleswig-Holstein since 2021, we compiled a dataset from all canteens in the region. This dataset, which dates back to 2021, combines information from the OpenMensa API with data obtained through web scraping (see [Data Collection](#data-collection)). Over this period, the dynamics of meal pricing within Schleswig-Holstein's canteens have experienced noticeable shifts. In our analysis, we consider various factors: geographical (by city), status-based (student, employee, guest), and dietary categories (vegan, vegetarian, omnivorous). We aim to unravel the intricacies of these pricing adjustments.

### Impact of Location on Price Change

Analysis of the average canteen meal pricing data across cities reveals that each city within Schleswig-Holstein has experienced significant price changes. Kiel, Flensburg, and Heide have seen a steady rise in meal prices. Lübeck, meanwhile, exhibits the smallest increase in prices in EUR terms, with only a marginally smaller percentage increase compared to the other cities. This suggests that, in general, local pricing in Lübeck has been more affordable.

![rq1_city_1](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/1bc7cb1d-f8db-49bc-9240-cc0e7d682dc6)

![rq1_city_2](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/adbc7d75-cb3f-4c90-9511-ab8e65464fbc)

**Average Price Change (Per Year Since 2021)**

| Location             | Price Increase (€/Year) | Percentage Increase (\%/Year) |
|----------------------|-------------------------|-------------------------------|
| Kiel:                | 0.41 €                  | 10.41 \%                      |
| Flensburg:           | 0.42 €                  | 11.05 \%                      |
| Lübeck:              | 0.16 €                  | 8.67 \%                       |
| Heide:               | 0.47 €                  | 9.36 \%                       |
| **Schleswig-Holstein:** | 0.36 €              | 9.87 \%                       |

In 2022 and 2023, canteen meal prices in Schleswig-Holstein (SH) rose noticeably, yet remained below the national food inflation rate. Despite the significant differences observed between cities across these years, an overarching trend of increasing prices is evident.

**Annual Price Changes (2022 and 2023)**
| Location          | 2022   | 2023  |
|-------------------|-------|-------|
| Kiel:             | 8.7 %  | 12.4 % |
| Flensburg:        | 1.7 %  | 9.8 %  |
| Lübeck:           | 15.8 % | 6.8 %  |
| Heide:            | 11.8 % | 12.2 % |
| **SH:**           | 9.5 %  | 10.3 % |
| **Food Inflation:** | 13.4 % | 12.4 % |

_Food Inflation = Germany-wide food inflation rate ([destatis.de](https://destatis.de))_

## Impact of Visitor Status on Price Change

An in-depth examination of meal price changes in canteens based on visitor status (student, employee, guest) reveals differentiated impacts. Guests experienced an annual increase of 10.92 % (0.47 €), employees saw a 10.47 % rise (0.42 €), and students encountered the steepest increase at 10.94 % (0.31 €). This tiered pricing model demonstrates the canteens' attempts to maintain affordability amidst inflation, tailored for students, employees, and guests.

![rq1_visirors_1](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/ff53bbbf-0f61-470a-8e90-d4f04b52bd34)

## Impact of Dietary Categories on Price Change

Further analysis delves into price variations across dietary categories: vegan, vegetarian, and meat-based meals. Surprisingly, vegan meals underwent the highest price adjustments, followed by meat-based and then vegetarian options. Specifically, vegan dishes experienced an average annual price increase of 18.33 % (0.54 €), with meat-based (16.84 %, 0.67 €) and vegetarian (15.41 %, 0.48 €) meals seeing more modest rises. The graph below illustrates the substantial price volatility of vegan meals compared to meat-based options, potentially reflecting the increasing costs of vegan food production and a growing demand for plant-based diets among students.

![rq1_category_1](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/098cc59f-f387-4521-8b11-e48dde3c1c4a)

![rq1_category_2](https://github.com/jonasweinschuetz/data_science_projekt/assets/59099913/64441c51-b427-4268-8f15-cb89754f7d5e)

## Conclusion

Our comprehensive analysis of meal price changes in Schleswig-Holstein's canteens since 2021 highlights several key trends. Geographical location, visitor status, and dietary choices significantly influence price adjustments, with vegan meals experiencing the highest increases. Despite the inflationary pressures, canteen meal prices in the region have generally remained below the national food inflation rate, suggesting efforts by canteen operators to keep meals accessible to their primary clientele. As dietary habits continue to evolve and economic conditions change, these trends offer valuable insights for diverse and economically sensitive people such as students, employees, and guests in educational institutions.


**Annual Price Changes (2022 and 2023)**
|                     | 2022   | 2023  |
|---------------------|-------|-------|
| **SH:**             | 9.5 %  | 10.3 % |
| **Food Inflation:** | 13.4 % | 12.4 % |
