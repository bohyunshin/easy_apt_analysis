# H&M Personalized Fashion Recommendation Dataset from Kaggle

## Competition description
H&M Group is a family of brands and businesses with 53 online markets and approximately 4,850 stores. Our online store offers shoppers an extensive selection of products to browse through. But with too many choices, customers might not quickly find what interests them or what they are looking for, and ultimately, they might not make a purchase. To enhance the shopping experience, product recommendations are key. More importantly, helping customers make the right choices also has a positive implications for sustainability, as it reduces returns, and thereby minimizes emissions from transportation.

In this competition, H&M Group invites you to develop product recommendations based on data from previous transactions, as well as from customer and product meta data. The available meta data spans from simple data, such as garment type and customer age, to text data from product descriptions, to image data from garment images.

There are no preconceptions on what information that may be useful – that is for you to find out. If you want to investigate a categorical data type algorithm, or dive into NLP and image processing deep learning, that is up to you.

More information about competition can be found in [this kaggle page](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/overview)
## Data description

```angular2html
├── images
│   ├── 010
│   │   ├── 0108775015.jpg
│   │   ├── 0108775044.jpg
│   │   ├── 0108775051.jpg
│   ├── 011
│   ├── 012
│   ├── ...
├── articles.csv
├── customers.csv 
└── transactions_train.csv
```
### images/
* a folder of images corresponding to each article_id
* images are placed in subfolders starting with the first three digits of the article_id 
* note, not all article_id values have a corresponding image

### articles.csv
* detailed metadata for each article_id available for purchase

Below is an example of meta for product code `0108775`

| article_id | product_code | prod_name | product_type_no | product_type_name | product_group_name  | graphical_appearance_no | graphical_appearance_name | colour_group_code | colour_group_name | perceived_colour_value_id | perceived_colour_value_name | perceived_colour_master_id | perceived_colour_master_name | department_no | department_name | index_code | index_name | index_group_no | index_group_name | section_no | section_name            | garment_group_no | garment_group_name | detail_desc                              |
|------------|--------------|-----------|-----------------|-------------------|---------------------|-------------------------|---------------------------|-------------------|-------------------|---------------------------|-----------------------------|----------------------------|------------------------------|---------------|-----------------|------------|------------|----------------|------------------|------------|-------------------------|------------------|--------------------|------------------------------------------|
| 0108775015 | 0108775      | Strap top | 253             | Vest top          | Garment Upper body  | 1010016                 | Solid                     | 10                | White             | 3                         | Light                       | 9                          | White                        | 1676          | Jeresy Basic    | A          | Ladieswear | 1              | Ladieswear       | 16         | Womens Everyday Basics  | 1002             | Jeresy Basic       | Jersey top with narrow shoulder straps.  |
### customers.csv 
* metadata for each customer_id in dataset

Below is an example of meta for customer id `00000dba`

| customer_id | FN  | Active | club_member_status | fashion_news_frequency | age | postal_code |
|-------------|-----|--------|--------------------|------------------------|-----|-------------|
| 00000dba    |     |        | ACTIVE             | NONE                   | 49  | ...         |

### transactions_train.csv
* the training data, consisting of the purchases each customer for each date, as well as additional information. 
* Duplicate rows correspond to multiple purchases of the same item. 
* Your task is to predict the article_ids each customer will purchase during the 7-day period immediately after the training data period.

Below is an example of a transaction data

| t_data     | customer_id | article_id  | price   | sales_channel_id |
|------------|-------------|-------------|---------|------------------|
| 2018-09-10 | 00000dba    | 0108775015  | 0.05083 | 2                |