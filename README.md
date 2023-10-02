# UnimartScrapping-Analytics

A specialized tool suite designed for the entire data journey of the [Unimart](https://www.unimart.com/) website - from scraping to analytical visualization.

## About Unimart

[Unimart](https://www.unimart.com/) is a leading online store in Costa Rica, boasting an extensive offering of over 40,000 products at competitive prices. Authorized to retail products from renowned brands such as Nexxt Solutions, Argom, Xiaomi, Google, Amazon, and more, Unimart has carved its niche primarily in the electronic, computing, home, sports, perfumes sectors, among others. With its expansive product range and commitment to quality, it has established itself as a premier online shopping destination in the region.

## Description

This project is divided into two main phases:

### 1. Data Extraction
This phase involves a web scraper built to navigate the Unimart website [Unimart](https://www.unimart.com/), identify and extract product categories, subcategories, and specific product details such as brand, name, price, and offer price. Extracted data is stored in Excel files, with functionality to upload these files to an Amazon S3 bucket.

- Automated browsing using `selenium`.
- Data extraction structured into categories and subcategories.
- Data storage in Excel files using `openpyxl` and `pandas`.
- Functionality to interact with AWS S3 using `boto3`.

### 2. Data Analysis & Visualization
Taking the extracted data from the Excel files, this phase populates a PostgreSQL database designed for structured storage and efficient querying. Various analytical techniques are employed to visualize data and provide meaningful insights into the Unimart products' landscape. Features include:

- Seamless database integration using `psycopg2`.
- Comprehensive database management with insertion, query, and other CRUD operations.

## Key Features

### Data Extraction
- **Web Browsing Automation:** Uses `selenium` for efficient website navigation.
- **Structured Data Extraction:** Categorizes data into main categories and subcategories.
- **Excel Integration:** Uses `openpyxl` and `pandas` for structured Excel file storage.
- **Amazon S3 Integration:** Comes with `boto3` functionality for storing data in the cloud.

### Data Analysis & Visualization
- **PostgreSQL Integration:** Seamless data management using `psycopg2`.
- **Database Operations:** Comprehensive CRUD functionalities for efficient data handling.
- **Graphical Insights:** Uses `matplotlib` for visual data representation and analysis.

## Installation

1. Ensure you have Python installed on your machine.
2. Clone this repository:

git clone https://github.com/alegambo/UnimartScrapping-Analytics.git


3. Navigate to the project directory:

cd UnimartScrapping-Analytics


4. Install the necessary dependencies using the `requirements.txt` file:

pip install -r requirements.txt


5. Set up your environment for Selenium and the respective WebDriver (e.g., ChromeDriver if you're using Chrome).

6. Configure your AWS credentials if planning to use the S3 functionality.


## Usage

To start the scraper, simply navigate to the project folder and run(Phase 1):

python Scrapping_Unimart.py

