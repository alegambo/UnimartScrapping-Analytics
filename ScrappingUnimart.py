from openpyxl.reader.excel import load_workbook
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs
import pandas as pd
import os
import time
import boto3
from datetime import datetime
from urllib.robotparser import RobotFileParser
from openpyxl import load_workbook


class UnimartScraper:
    """
        A scraper class designed to extract data from the Unimart website.
        """

    # For ease of development, folder paths were added statically.
    # Adjustments are needed to make the code portable across different operating systems.
    ROOT_URL = 'https://www.unimart.com/'
    ROBOTS_URL = 'https://www.unimart.com/robots.txt'
    ROOT_NAV_ID = 'AccessibleNav'  # ID for the main navigation element on the website
    XPATH_DATA_LINK = './/*[@data-link]'  # XPath to locate elements with a data-link attribute
    MAIN_CATEGORIES_TITLE = 'Main Categories'  # Title or label for main categories
    #For pratical Purposes that folders was added statically
    OUTPUT_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\'  # Directory to store output files
    OUTPUT_DIRECTORY_URLS = 'URLs\\'  # Sub-directory specifically for URLs
    READ_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\Urls\\'  # Directory to read input files
    MAIN_CATEGORIES_SUBFOLDER='MainCategories\\'
    MAIN_CATEGORIES_URLS_SUBCATEGORIES=OUTPUT_DIRECTORY+MAIN_CATEGORIES_SUBFOLDER+ 'MainCategories_urls_subcategories\\'
    ARTICLES_BY_SUBCATEGORY_FOLDER=OUTPUT_DIRECTORY+'Articles_by_subcategory\\'
    BUCKET = 'unimartbucket'  # Name of the S3 bucket for cloud storage
    FILE_WITH_MAIN_URLS = 'MAIN_URLS.xlsx'  # Excel file containing main URLs
    # XPath for the main content div containing article details on the website
    DIV_WITH_ARTICLES = (
        "//*[contains(@class, 'boost-pfs-filter-products') and "
        "contains(@class, 'boost-pfs-filter-product-item-layout-no-border') and "
        "contains(@class, 'boost-pfs-filter-product-item-label-top_left') and "
        "contains(@class, 'boost-pfs-filter-product-item-swatch_color_display_type_image_product') and "
        "contains(@class, 'boost-pfs-filter-swatch-shape-circle') and "
        "contains(@class, 'boost-pfs-filter-product-item-text-alignment-left')]"
    )
    # XPath to locate the bottom pagination div on the website
    BOTTOM_DIV = '//div[contains(@class, "boost-pfs-filter-bottom-pagination") and contains(@class, "boost-pfs-filter-bottom-pagination-default") and @style="display: block;"]'
    # XPath for the link to navigate to the next page
    NEXT_PAGE_LINK = './ul/li[not(contains(@class, "boost-pfs-filter-pagination-disabled"))]/a[normalize-space(.)="→"]'

    def __init__(self):
        """
               Initializes the scraper with a headless Chrome browser session.
               Sets up the WebDriver wait for explicit waits and initializes the S3 client for AWS operations.
         """

        # Set Chrome to run in headless mode for scraping without visual browser interface
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

        # Setup explicit wait with a maximum of 10 seconds for elements to become available
        self.wait = WebDriverWait(self.driver, 10)
        # Initialize the S3 client for Amazon Web Services
        self.s3 = boto3.client('s3')

    def scrape_product_details_from_url(self, subcategory, label, url):
        """
            Navigates to the given URL, scrapes, and stores article details like brand, name, price, and offer price.

            :param subcategory: Name of the subcategory.
            :param label: Label of the article.
            :param url: Web page URL to scrape article details from.
            """
        df = pd.DataFrame(columns=['Brand', 'Articule_Name', 'Price', 'Offer_Price'])
        # Navigate to the primary URL
        self.driver.get(url)
        time.sleep(15)
        file_path = self.ARTICLES_BY_SUBCATEGORY_FOLDER + subcategory + '.xlsx'

        while True:
            time.sleep(10)

            div_with_articles = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.DIV_WITH_ARTICLES)))

            elements_with_class1 = div_with_articles.find_elements(By.XPATH,
                                                                   './/div[contains(@class, "boost-pfs-filter-product-bottom-inner")]')
            elements_with_class2 = div_with_articles.find_elements(By.XPATH,
                                                                   './/div[contains(@class, "boost-pfs-filter-product-bottom")]')

            if elements_with_class1:
                elements_to_process = elements_with_class1
            else:
                elements_to_process = elements_with_class2

            self.iterate_by_articule(elements_to_process, df)
            self.save_to_excel(df, file_path, label)

            try:
                element_bottom = self.driver.find_element(By.XPATH, self.BOTTOM_DIV)
                next_page = element_bottom.find_element(By.XPATH, self.NEXT_PAGE_LINK)
                next_page_url = next_page.get_attribute('href')

                if not next_page_url or not isinstance(next_page_url, str):
                    print("Invalid URL or Not Founded:", next_page_url)
                    break

                # Navigate to the next page
                self.driver.get(next_page_url)
                print(self.driver.current_url)  # print the current next page

            except NoSuchElementException:
                # break the loop
                break

    def save_to_excel(self, df, file_path, sheet_name):
        """
        Save the dataframe to an Excel file. If the file already exists, append the new dataframe to the end.
        If the specified sheet doesn't exist in an existing file, then create a new sheet with headers.

        :param df: DataFrame with the data.
        :param file_path: Full path to the file.
        :param sheet_name: Name of the sheet to save the data.
        """

        # Check if the file already exists
        if os.path.exists(file_path):
            try:
                # Determine the last row using pandas
                existing_df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                startrow = existing_df.shape[0]
                header = False  # Do not add headers since the sheet already exists
            except ValueError:  # If the sheet doesn't exist in the file
                startrow = 0
                header = True  # Add headers since the sheet will be new

            # Write to the existing file
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow, header=header)

        else:  # If the file doesn't exist
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def can_fetch(self, url, user_agent="*"):
        """
        Determines if a given user agent is allowed to fetch the specified URL based on the rules
        in the robots.txt file of the website.

        :param url: The URL that needs to be fetched.
        :param user_agent: The name of the user-agent (default is "*").
        :return: True if the user agent is allowed to fetch the URL, otherwise False.
        """

        # Initialize the RobotFileParser to interpret the robots.txt file
        rp = RobotFileParser()

        # Set the URL for the robots.txt file
        rp.set_url(self.ROBOTS_URL)

        # Read and parse the robots.txt file
        rp.read()

        # Check if the specified user agent can fetch the given URL
        return rp.can_fetch(user_agent, url)

    def get_articule_info(self):
        """
        Extracts article information from all Excel files in the output directory.
        It goes through each file, extracts the categories and subcategories, and then scrapes article details from the given URL.

        :param self: Instance of the class.
        """

        # List all files in the output directory
        files = os.listdir(self.MAIN_CATEGORIES_URLS_SUBCATEGORIES)

        # Filter and get only Excel files
        excelFiles = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]

        for file in excelFiles:
            print(file)
            file_without_extension = file.replace(".xlsx", "")
            complete_path = os.path.join(self.MAIN_CATEGORIES_URLS_SUBCATEGORIES, file)
            print(complete_path)

            # Read the Excel file
            excel_df = pd.read_excel(complete_path, engine='openpyxl')

            # Iterate through the dataframe columns in steps of 2 (since every pair is a value and a URL)
            for i in range(0, excel_df.columns.size, 2):
                value_header = excel_df.columns[i]
                url_header = excel_df.columns[i + 1]
                if value_header == "Marcas Populares":
                    continue

                # Iterate through the dataframe rows
                for _, row in excel_df.iterrows():
                    label = row[value_header]
                    url = row[url_header]
                    if pd.notna(label) and pd.notna(url) and not label.startswith("Ver Todo"):
                        # Process each URL and extract article details
                        subcategory = value_header.replace("¿", "").replace("?", "").replace(" ", "_")
                        print(f"Processing: {subcategory} - {label} - {url}")
                        self.scrape_product_details_from_url(subcategory, label, url)

    def iterate_by_articule(self, elements_with_class, dataframe):

        """
            Iterates over given elements, extracts, and stores article details.

            :param elements_with_class: Web page elements containing article details.
            :param dataframe: DataFrame to store article details.
            """

        for element in elements_with_class:
            a_class_list = element.find_elements(By.TAG_NAME, "a")
            span_money = element.find_elements(By.CSS_SELECTOR, "span.money")
            offer = None
            brand = a_class_list[0].text
            articule_name = a_class_list[1].text
            if len(span_money) > 1:
                price = span_money[0].text
                offer = span_money[1].text
            else:
                price = span_money[0].text

            print("brand: " + brand)
            print("article_name: " + articule_name)
            print("price: " + price)
            dataframe.loc[len(dataframe)] = [brand, articule_name, price, offer]
            print("+++++++++++++++++++++++++++++++")

    def get_access_to_root_page(self):
        """
           Navigates to the root page and waits until the main navigation element becomes visible.
        """
        # Wait until the main navigation element is visible
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, self.ROOT_NAV_ID))
        )

    def get_categories_from_nav(self, nav):
        """
            Extracts the main categories listed in the given navigation element.

            :param nav: Web element representing the navigation section.
            :return: List of main category names.
        """
        # Split the text of the navigation element by new lines to get individual categories
        return nav.text.split("\n")

    def create_excel_with_main_categories(self, main_categories):
        """
        Saves the provided list of main categories to an Excel file. Filters out specific categories before saving.

        :param main_categories: List of main category names.
        """
        # Exclude "Regalos" and "Ofertas" from the list of main categories because they are categories with temporary
        # articles
        filtered_main_categories = [cat for cat in main_categories if cat not in ["Regalos", "Ofertas"]]

        # Create a dataframe and save it to an Excel file
        df = pd.DataFrame({self.MAIN_CATEGORIES_TITLE: filtered_main_categories})
        df.to_excel(self.OUTPUT_DIRECTORY + self.MAIN_CATEGORIES_SUBFOLDER + self.MAIN_CATEGORIES_TITLE + '.xlsx', index=False)

    def get_data_links(self, nav):
        """
        Extracts the 'data-link' attributes from the provided navigation element.

        :param nav: Web element representing the navigation section.
        :return: List of 'data-link' attribute values.
        """
        # Find all elements in the navigation with the specified XPath
        elements = nav.find_elements(By.XPATH, self.XPATH_DATA_LINK)
        # Extract data-link attributes from the navigation element Exclude the last two elements,
        # corresponding to "Regalos" and "Ofertas" categories because they are categories with temporary articles
        elements = elements[:-2]

        # Retrieve the 'data-link' attribute from each element and return the list
        return [el.get_attribute('data-link') for el in elements]

    def extract_subcategories_and_urls(self, element_divs, dataframe):

        """
           Extracts the names and URLs of subcategories from the provided web elements.
           Populates the given dataframe with the extracted data, using subcategory names as column headers.

           :param element_divs: List of web elements representing the subcategories.
           :param dataframe: DataFrame to populate with extracted subcategory data.
           """

        # Attempt to read an Excel file with URLs. If not found, initialize a new dataframe
        # Note: This segment is commented out, so it's not currently being used.
        # try:
        #     excel_df = pd.read_excel(self.OUTPUT_DIRECTORY + self.OUTPUT_DIRECTORY_URLS + self.FILE_WITH_MAIN_URLS)
        # except FileNotFoundError:
        #     excel_df = pd.DataFrame(columns=['Label', 'URL', 'Subcategory'])

        # Iterate through each provided web element to extract subcategory details
        for div in element_divs:
            list_items = []
            list_url = []
            # Extract the name of the subcategory
            subcategory = div.find_element(By.XPATH, './/a').text

            # Find all links within the subcategory
            ul_elements = div.find_element(By.TAG_NAME, 'ul')
            a_elements = ul_elements.find_elements(By.TAG_NAME, 'a')

            for a in a_elements:
                label = a.text
                list_items.append(label)
                link = a.get_attribute('href')
                list_url.append(link)
                # Commented-out condition seems to check the start of the label and if it's unique in excel_df.
                # if label.startswith("Ver Todo") and not label.startswith("Ver Todo Ofertas") and not label.startswith("Ver Todos"):
                #     if not excel_df['URL'].str.contains(link).any():
                #         excel_df.loc[len(excel_df)] = [label, link, subcategory]

            # Populate the dataframe with the extracted subcategory names and URLs
            dataframe[subcategory] = pd.Series(list_items)
            dataframe[subcategory + '_url'] = pd.Series(list_url)
        # Commented out saving of the excel_df, which was initially intended to hold unique URLs.
        # excel_df.to_excel(self.OUTPUT_DIRECTORY + self.OUTPUT_DIRECTORY_URLS + self.FILE_WITH_MAIN_URLS, index=False)

    def get_elements_by_data_links(self, list_li_categories, data_links, main_categories):
        """
           For each main category, the function clicks on its respective UI element, extracts subcategory details
           and saves the results to an Excel file.

           :param list_li_categories: List of web elements representing the main categories.
           :param data_links: Data link IDs associated with each main category.
           :param main_categories: List of main category names.
           """
        # Loop through each main category, its web element, and associated data link
        for li, data_link, category in zip(list_li_categories, data_links, main_categories):
            df = pd.DataFrame()  # Create an empty dataframe to store extracted data
            li.click()  # Click on the main category to display its subcategories

            # Find the associated content by ID after the click
            elementID = self.driver.find_element(By.ID, data_link)
            time.sleep(5)  # Allow some time for the content to load/display

            # Extract all the subcategory elements under the main category
            element_divs = elementID.find_elements(By.XPATH,
                                                   './/div[contains(@class, "grid__item large--one-fifth medium--one-whole no_middle_align mt30")]')

            # Extract details (like URLs) from the subcategories and save to the dataframe
            self.extract_subcategories_and_urls(element_divs, df)

            time.sleep(3)  # Pause for a moment before proceeding
            li.click()  # Click again to collapse the category (or navigate back)

            # Save the dataframe to an Excel file named after the main category
            df.to_excel(self.MAIN_CATEGORIES_URLS_SUBCATEGORIES + category + '.xlsx', sheet_name=category, index=False)

    def uploadtoS3(self, directory=None):
        """
        Uploads files from the specified directory (or the default output directory if none is specified)
        to an Amazon S3 bucket, preserving the directory structure.

        :param directory: The directory path to look for files. If not provided, uses the default OUTPUT_DIRECTORY.
        """

        # If no directory is provided, use the default OUTPUT_DIRECTORY
        if directory is None:
            directory = self.OUTPUT_DIRECTORY

        # Iterate over files and directories in the given directory
        for archivo in os.listdir(directory):
            complete_path = os.path.join(directory, archivo)

            # If it's a file, upload it to S3
            if os.path.isfile(complete_path):
                # Calculate the relative path to keep the directory structure in S3
                s3_path = os.path.relpath(complete_path, self.OUTPUT_DIRECTORY)

                # Replace backslashes with slashes for S3 paths and upload
                self.s3.upload_file(complete_path, self.BUCKET, s3_path.replace("\\", "/"))

                # Print a confirmation message
                print(f'{complete_path} has been successfully uploaded to {self.BUCKET}/{s3_path}')

            # If it's a directory, call the function recursively to process its contents
            elif os.path.isdir(complete_path):
                self.uploadtoS3(directory=complete_path)

    def scrape_unimart(self):
        """
        Orchestrates the scraping process for the Unimart website. It follows these steps:
        1. Navigate to the Unimart root URL.
        2. Wait for the main navigation to be accessible.
        3. Extract main category names from the navigation.
        4. Save main category names to an Excel file.
        5. Extract data-links associated with main categories.
        6. Extract individual list items corresponding to main categories.
        7. Execute scraping for the list items using their data-links.
        """

        # Navigate to the Unimart root URL
        self.driver.get(self.ROOT_URL)

        # Wait until the main navigation section is accessible
        self.get_access_to_root_page()

        # Find and extract the main navigation element by its ID
        nav = self.driver.find_element(By.ID, self.ROOT_NAV_ID)

        # Extract main category names from the navigation
        main_categories = self.get_categories_from_nav(nav)

        # Save the extracted main category names to an Excel file
        self.create_excel_with_main_categories(main_categories)

        # Extract data-links associated with main categories
        data_links = self.get_data_links(nav)

        # Extract individual list items from the navigation that correspond to main categories
        list_li_categories = nav.find_elements(By.TAG_NAME, 'li')

        # Exclude the list items corresponding to "Regalos" and "Ofertas" categories
        list_li_categories = list_li_categories[:-2]

        # Initiate the scraping process for the list items using their associated data-links
        self.get_elements_by_data_links(list_li_categories, data_links, main_categories)

        # Start the main scraping method of the scraper
        self.get_articule_info()

        # Commented line: Closes the browser session after scraping
        self.driver.quit()


if __name__ == "__main__":
    # Ensure the script is being run as the main program (not imported elsewhere)

    # Record the current datetime before starting the scraping process for performance measurement
    before = datetime.now()

    # Instantiate the UnimartScraper class
    scraper = UnimartScraper()

    # Start scrapping
    scraper.scrape_unimart()


    # Record the current datetime after finishing the scraping process
    after = datetime.now()

    # Print the duration it took for the scraping process to complete
    print(after - before)

    # Commented lines: additional methods that could be called on the scraper instance
    # scraper.readFirstUrls()  # Potentially read and process URLs from an initial set
    # scraper.uploadtoS3()     # Upload scraped data or files to Amazon S3