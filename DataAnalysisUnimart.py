import pandas as pd
import psycopg2
import os
import locale
import matplotlib.pyplot as plt
import matplotlib.colors as mcm
import numpy as np


class DatabaseManager:
    def __init__(self, host, dbname, user, password, port):
        """
        Initialize the DatabaseManager with necessary connection details.

        :param host: The hostname or IP address of the database server.
        :param dbname: Name of the database to connect to.
        :param user: Username to connect to the database.
        :param password: Password for the given username.
        :param port: Port number where the database server is listening.
        """
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = None  # This will hold the actual database connection object once connected.

    def connect(self):
        """
        Establish a connection to the database and return the connection object.

        :return: The database connection object.
        """
        self.conn = psycopg2.connect(
            host=self.host,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            port=self.port
        )
        return self.conn

    def disconnect(self):
        """Close connection to Database."""
        if self.conn:
            self.conn.close()

    def insert_category(self, category_name):
        """
        Insert a new category into the database and retrieve the generated ID.

        :param category_name: The name of the category to be inserted.
        :return: None
        """
        data = (category_name,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query
            query = "INSERT INTO Category (category_name) VALUES (%s) RETURNING ID_Category;"

            # Execute the query with the provided data
            cur.execute(query, data)

            # Fetch the ID generated by the insertion
            generated_id = cur.fetchone()[0]

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def fetch_all(self, query, params=None):
        """
        Execute the given query and return all results.

        :param query: The SQL query to be executed.
        :param params: Optional parameters to use with the query.
        :return: List of tuples containing query results.
        """
        self.connect()
        cur = self.conn.cursor()
        cur.execute(query, params or ())
        results = cur.fetchall()
        return results

    def insert_price(self, price):
        """
        Insert a new price into the database.

        :param price: The price value to be inserted.
        :return: None
        """
        data = (price,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query
            query = "INSERT INTO Price (price) VALUES (%s);"

            # Execute the query with the provided data
            cur.execute(query, data)

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def insert_brand1(self, brand):
        """
        Insert a new brand into the database.

        :param brand: The name of the brand to be inserted.
        :return: None
        """
        data = (brand,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query
            query = "INSERT INTO brand (brand_name) VALUES (%s);"

            # Execute the query with the provided data
            cur.execute(query, data)

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def insert_brand(self, brand):
        """
        Insert a new brand into the database.

        :param brand: The name of the brand to be inserted.
        :return: None
        """
        data = (brand,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query
            query = "INSERT INTO brand (brand_name) VALUES (%s);"

            # Execute the query with the provided data
            cur.execute(query, data)

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def insert_article(self, id_type, id_brand, id_price, article_name):
        """
        Insert a new article with its related information into the database.

        :param id_type: The ID of the article type.
        :param id_brand: The ID of the article brand.
        :param id_price: The ID of the article price.
        :param article_name: The name of the article to be inserted.
        :return: None
        """
        data = (id_type, id_brand, id_price, article_name,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query
            query = "INSERT INTO article (id_type, id_brand,id_price,article_name) VALUES (%s, %s, %s, %s);"

            # Execute the query with the provided data
            cur.execute(query, data)

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def insert_brands(self, brands):
        """
        Insert multiple brands into the database at once.

        :param brands: List of brand names to be inserted.
        :return: None
        """
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query for multiple records
            query = "INSERT INTO brand (brand_name) VALUES (%s);"

            # Prepare data for insertion
            data = [(brand,) for brand in brands]

            # Execute the query with the provided data
            cur.executemany(query, data)

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def insert_type(self, subcategory_id, type_name):
        """
        Insert a new type with its related subcategory ID into the database.

        :param subcategory_id: The ID of the related subcategory.
        :param type_name: The name of the type to be inserted.
        :return: None
        """
        data = (subcategory_id, type_name,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query
            query = "INSERT INTO type (id_subcategory, type_name) VALUES (%s, %s);"

            # Execute the query with the provided data
            cur.execute(query, data)

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def insert_subcategory(self, category_id, subcategoryname):
        """
        Insert a new subcategory with its related category ID into the database.

        :param category_id: The ID of the related category.
        :param subcategoryname: The name of the subcategory to be inserted.
        :return: None
        """
        data = (category_id, subcategoryname,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL INSERT query
            query = "INSERT INTO Subcategory (ID_Category, subcategory_name) VALUES (%s, %s);"

            # Execute the query with the provided data
            cur.execute(query, data)

            # Commit the transaction to the database
            self.conn.commit()

        except Exception as e:
            # In case of an error, rollback the transaction
            self.conn.rollback()
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def select_id_price(self, price):
        """
        Fetch the ID associated with a specific price from the database.

        :param price: The price value to look up.
        :return: The ID associated with the given price, or None if not found.
        """
        data = (price,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL SELECT query
            query = "SELECT id_price FROM price WHERE price = %s;"

            # Execute the query with the provided data
            cur.execute(query, data)

            results = cur.fetchall()

            if results:
                id_price = results[0][0]
                return id_price

        except Exception as e:
            # In case of an error, report it
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def select_id_brand(self, brand_name):
        """
        Fetch the ID associated with a specific brand name from the database.

        :param brand_name: The brand name to look up.
        :return: The ID associated with the given brand name, or None if not found.
        """
        data = (brand_name,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL SELECT query
            query = "SELECT id_brand FROM brand WHERE brand_name = %s;"

            # Execute the query with the provided data
            cur.execute(query, data)

            results = cur.fetchall()

            if results:
                id_brand = results[0][0]
                return id_brand

        except Exception as e:
            # In case of an error, report it
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def select_id_type(self, type_name):
        """
        Fetch the ID associated with a specific type name from the database.

        :param type_name: The type name to look up.
        :return: The ID associated with the given type name, or None if not found.
        """
        data = (type_name,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL SELECT query
            query = "SELECT id_type FROM type WHERE type_name = %s;"

            # Execute the query with the provided data
            cur.execute(query, data)

            results = cur.fetchall()

            if results:
                id_type = results[0][0]
                return id_type

        except Exception as e:
            # In case of an error, report it
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def select_id_subcategory(self, subcategory_name):
        """
        Fetch the ID associated with a specific subcategory name from the database.

        :param subcategory_name: The subcategory name to look up.
        :return: The ID associated with the given subcategory name, or None if not found.
        """
        data = (subcategory_name,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL SELECT query
            query = "SELECT id_subcategory FROM subcategory WHERE subcategory_name = %s;"

            # Execute the query with the provided data
            cur.execute(query, data)

            results = cur.fetchall()

            if results:
                id_subcategory = results[0][0]
                return id_subcategory

        except Exception as e:
            # In case of an error, report it
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()

    def select_id_category(self, category_name):
        """
        Fetch the ID associated with a specific category name from the database.

        :param category_name: The category name to look up.
        :return: The ID associated with the given category name, or None if not found.
        """
        data = (category_name,)
        try:
            # Create a cursor for database operations
            cur = self.conn.cursor()

            # SQL SELECT query
            query = "SELECT id_category FROM Category WHERE category_name = %s;"

            # Execute the query with the provided data
            cur.execute(query, data)

            results = cur.fetchall()

            if results:
                id_category = results[0][0]
                return id_category

        except Exception as e:
            # In case of an error, report it
            print(f"Error: {e}")

        finally:
            # Close the cursor
            cur.close()


def get_article_count_by_brand(db_manager):
    """
    Fetch the count of articles grouped by brand from the database, returning the top 10 brands with the highest article count.

    :param db_manager: An instance of the database manager or the object that provides the `fetch_all` method.
    :return: List of tuples containing brand names and their associated article counts.
    """
    query = """
    SELECT B.brand_name, COUNT(A.ID_Article) AS NumberOfArticles
    FROM Brand B
    LEFT JOIN Article A ON B.ID_Brand = A.ID_Brand
    GROUP BY B.brand_name
    ORDER BY NumberOfArticles DESC
    limit 10;
    """
    data= db_manager.fetch_all(query)
    plot_brand_article_count(data)


def get_article_count_by_subcategory(db_manager):
    """
    Fetch the count of articles grouped by subcategory from the database, returning the top 10 subcategories with the highest article count.

    :param db_manager: An instance of the database manager or the object that provides the `fetch_all` method.
    :return: List of tuples containing subcategory IDs, subcategory names, and their associated article counts.
    """
    query = """
    SELECT 
        s.ID_Subcategory,
        s.subcategory_name,
        COUNT(a.ID_Article) AS article_count
    FROM 
        Subcategory s
    LEFT JOIN 
        Type t ON s.ID_Subcategory = t.ID_Subcategory
    LEFT JOIN 
        Article a ON t.ID_Type = a.ID_Type
    GROUP BY 
        s.ID_Subcategory, s.subcategory_name
    ORDER BY 
        article_count DESC
    limit 10;
    """
    data= db_manager.fetch_all(query)
    plot_article_count_by_subcategory(data)


def insert_category_from_excel(db_manager):
    """
    Read categories from an Excel file and insert them into the database.

    :param db_manager: An instance of the database manager or the object that provides the `insert_category` method.
    :return: None
    """
    # Load data from the Excel file into a pandas DataFrame
    excel_df = pd.read_excel('C:\\Users\\alega\\Documents\\Excels\\MainCategories\\Main Categories.xlsx',
                             engine='openpyxl')

    # Iterate through each row of the DataFrame
    for index, row in excel_df.iterrows():
        # Use the database manager to insert each category into the database
        db_manager.insert_category(row['Main Categories'])


def insert_price_from_excel(db_manager):
    """
    Read prices from multiple Excel files within a directory and insert unique prices into the database.

    :param db_manager: An instance of the database manager or the object that provides the `insert_price` method.
    :return: None
    """
    # Set locale for number formatting
    # READ_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\Ver Todo URL\\'  # An alternative path, currently commented out
    READ_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\Articles_by_subcategory\\'

    # List all files in the directory
    files = os.listdir(READ_DIRECTORY)
    print(files)

    # Filter out only Excel files from the list
    excelFiles = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]
    collected_rows = []

    # Iterate over each Excel file
    for file in excelFiles:
        file_without_extension = file.replace(".xlsx", "")
        print(file_without_extension)
        full_path = os.path.join(READ_DIRECTORY, file)
        print(full_path)

        # Load the Excel file
        xl = pd.ExcelFile(full_path)

        # Iterate over each sheet in the Excel file
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name, engine='openpyxl')

            # Check if the sheet has a 'Price' column
            if 'Price' in df.columns:
                values = df['Price'].tolist()
                collected_rows.extend(values)
            else:
                print(f"The file {file} does not have a 'Price' column.")

    # Remove duplicates from the collected prices and format them
    unique_values = list(set(collected_rows))
    for price in unique_values:
        cleaned_price = price.replace("₡", "").replace(",", "")
        decimal_number = locale.atof(cleaned_price)
        formatted_number = "{:.2f}".format(decimal_number)

        # Use the database manager to insert each cleaned price into the database
        db_manager.insert_price(formatted_number)


def insert_subcategory_from_excel(db_manager):
    """
    Read subcategories from Excel files within a directory and insert them into the database,
    associating them with their main category based on the file name.

    :param db_manager: An instance of the database manager.
    :return: None
    """
    READ_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\MainCategories\\MainCategories_urls_subcategories\\'
    files = os.listdir(READ_DIRECTORY)
    print(files)
    excelFiles = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]
    collected_rows = []

    for file in excelFiles:
        full_path = os.path.join(READ_DIRECTORY, file)
        file_without_extension = file.replace(".xlsx", "")
        df = pd.read_excel(full_path, engine='openpyxl')
        print(file_without_extension)

        try:
            # Get the category ID based on the file name (file name is assumed to be the category name)
            id_category = db_manager.select_id_category(file_without_extension)

            for col in df.columns:
                if '_url' not in col and "Marcas Populares" not in col:
                    db_manager.insert_subcategory(id_category, col)
                    print(f"Subcategory {col} inserted with ID_Category {id_category}")
                else:
                    print(f"No category found for {col}")

        except Exception as e:
            print(f"Error: {e}")


def insert_brands_from_excel(db_manager):
    """
    Read brands from multiple Excel files within a directory and insert unique brands into the database.

    :param db_manager: An instance of the database manager.
    :return: None
    """
    READ_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\Articles_by_subcategory\\'
    files = os.listdir(READ_DIRECTORY)
    excelFiles = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]
    collected_rows = []

    for file in excelFiles:
        file_without_extension = file.replace(".xlsx", "")
        print(file_without_extension)
        full_path = os.path.join(READ_DIRECTORY, file)
        print(full_path)
        xl = pd.ExcelFile(full_path)

        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name, engine='openpyxl')

            if 'Brand' in df.columns:
                values = df['Brand'].tolist()
                collected_rows.extend(values)
            else:
                print(f"The file {file} does not have a 'Brand' column.")

    # Remove duplicates from the collected brands
    unique_values = list(set(collected_rows))

    # Use the database manager to insert all the unique brands into the database
    db_manager.insert_brands(unique_values)


def insert_type_from_excel(db_manager):
    """
    Read types from Excel files within a directory and insert them into the database,
    associating them with their subcategory based on the file name.

    :param db_manager: An instance of the database manager.
    :return: None
    """
    READ_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\Articles_by_subcategory\\'
    files = os.listdir(READ_DIRECTORY)
    excelFiles = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]

    for file in excelFiles:
        file_without_extension = file.replace(".xlsx", "")
        print(file_without_extension)
        full_path = os.path.join(READ_DIRECTORY, file)
        print(full_path)
        xl = pd.ExcelFile(full_path)

        # Convert file name to subcategory name and fetch its ID
        subcategory = file_without_extension.replace("_", " ")
        id_subcategory = db_manager.select_id_subcategory(subcategory)

        for sheet_name in xl.sheet_names:
            # Insert type into the database, associating it with its subcategory
            db_manager.insert_type(id_subcategory, sheet_name)


def insert_articule_from_excel(db_manager):
    """
    Read articles from Excel files and insert them into the database.

    :param db_manager: An instance of the database manager.
    :return: None
    """
    READ_DIRECTORY = 'C:\\Users\\alega\\Documents\\Excels\\Articles_by_subcategory\\'
    files = os.listdir(READ_DIRECTORY)
    excelFiles = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]

    for file in excelFiles:
        file_without_extension = file.replace(".xlsx", "").replace("_", " ")
        print(f"file is  {file_without_extension}")
        full_path = os.path.join(READ_DIRECTORY, file)

        xl = pd.ExcelFile(full_path)

        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name, engine='openpyxl')
            id_type = db_manager.select_id_type(sheet_name)

            for index, row in df.iterrows():
                # Get brand ID from the database
                id_brand = db_manager.select_id_brand(row['Brand'])
                print(f"id_brand id is  {id_brand}")

                # Clean and format the price
                cleaned_price = row['Price'].replace("₡", "").replace(",", "")
                decimal_number = locale.atof(cleaned_price)
                formatted_number = "{:.2f}".format(decimal_number)

                # Get price ID from the database
                id_price = db_manager.select_id_price(formatted_number)
                print(f"id_price id is  {id_price}")

                article_name = row['Articule_Name']
                print(f"article_name is {article_name}")

                # Insert the article into the database
                db_manager.insert_article(id_type, id_brand, id_price, article_name)


def get_price_stats_by_subcategory(db_manager):
    """
    Fetch average, minimum, and maximum prices of articles grouped by their subcategories.

    :param db_manager: An instance of the database manager.
    :return: A list of tuples where each tuple contains statistics for a specific subcategory.
    """
    query = """
    SELECT 
        S.subcategory_name, 
        AVG(P.Price) AS AvgPrice, 
        MIN(P.Price) AS MinPrice, 
        MAX(P.Price) AS MaxPrice
    FROM Subcategory S
    LEFT JOIN Article A ON S.ID_Subcategory = A.ID_Subcategory
    LEFT JOIN Price P ON A.ID_Price = P.ID_Price
    GROUP BY S.subcategory_name
    ORDER BY AvgPrice DESC;
    """
    return db_manager.fetch_all(query)


# --------------------------
# Queries for Statistics
# --------------------------
def get_price_stats_by_category(db_manager):
    """
    Fetch average, minimum, and maximum prices of articles grouped by their main categories.

    :param db_manager: An instance of the database manager.
    :return: A list of tuples where each tuple contains statistics for a specific main category.
    """
    query = """
    SELECT 
    C.category_name, 
    AVG(P.Price) AS AvgPrice, 
    MIN(P.Price) AS MinPrice, 
    MAX(P.Price) AS MaxPrice
FROM Category C
LEFT JOIN Subcategory S ON C.ID_Category = S.ID_Category
LEFT JOIN Type T ON S.ID_Subcategory = T.ID_Subcategory
LEFT JOIN Article A ON T.ID_Type = A.ID_Type
LEFT JOIN Price P ON A.ID_Price = P.ID_Price
GROUP BY C.category_name
ORDER BY AvgPrice DESC;
    """
    data= db_manager.fetch_all(query)
    filtered_data = [row for row in data if not (row[1] is None and row[2] is None and row[3] is None)]
    # # print(data)
    plot_price_stats_by_category(filtered_data)


def most_expensive_articles(db_manager):
    """
    Fetch the top 10 most expensive articles along with their prices.

    :param db_manager: An instance of the database manager.
    :return: A list of tuples where each tuple contains the name and price of an article.
    """
    query = """
    SELECT 
    A.article_name,
    P.Price AS price
FROM 
    Article A
JOIN 
    Price P ON A.ID_Price = P.ID_Price
ORDER BY 
    P.Price DESC
LIMIT 10;
    """
    data= db_manager.fetch_all(query)
    plot_most_expensive_articles(data)


def plot_brand_article_count(data):
    """
    Plot the number of articles for each brand.

    :param data: List of tuples, where each tuple contains the brand name and the respective article count.
    """
    brands = [row[0] for row in data]
    counts = [row[1] for row in data]

    #MatplotlibDeprecationWarning: The get_cmap function was deprecated in Matplotlib 3.7 and will be removed two minor releases later. Use ``matplotlib.colormaps[name]`` or ``matplotlib.colormaps.get_cmap(obj)`` instead.cmap = plt.cm.get_cmap("tab10", len(brands))
    cmap = plt.cm.get_cmap("tab10", len(brands))
    colors = [cmap(i) for i in range(len(brands))]
    plt.figure(figsize=(10, 8))
    bars = plt.bar(brands, counts,color=colors)

    # Display the exact counts on top of the bars
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2,  # X position, centered on the bar
                 bar.get_height() + 0.5,  # Y position, slightly above the top of the bar
                 '%d' % int(bar.get_height()),  # Text
                 ha='center', va='bottom',
                 color='black')

    plt.title('Number of items Per brand')
    plt.ylabel('Article Count')
    plt.xlabel('Brand')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def plot_price_stats_by_category(data):
    """
    Plot the average, minimum, and maximum prices of articles for each main category.

    :param data: List of tuples, where each tuple contains the category name, average, minimum, and maximum prices.
    """
    # Get the category names
    categories = [row[0] for row in data]
    # Get average, min, and max prices
    avg_prices = [row[1] for row in data]
    min_prices = [row[2] for row in data]
    max_prices = [row[3] for row in data]

    x = np.arange(len(categories))  # label locations
    width = 0.25  # width of the bars

    fig, ax = plt.subplots(figsize=(15, 10))

    # Create bars
    rects1 = ax.bar(x - width, min_prices, width, label='Min Price', color='lightblue')
    rects2 = ax.bar(x, avg_prices, width, label='Avg Price', color='red')
    rects3 = ax.bar(x + width, max_prices, width, label='Max Price', color='steelblue')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Category')
    ax.set_ylabel('Price')
    ax.set_title('Price statistics by Category')
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()

    # Helper function to label bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(round(height, 2)),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=6)

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    plt.show()


def plot_most_expensive_articles(data):
    """
    Plot the prices of the top 10 most expensive articles.

    :param data: List of tuples, where each tuple contains the article name and its price.
    """

    # Get the article names and their prices
    articles = [row[0] for row in data]
    print(articles)
    prices = [row[1] for row in data]
    print(prices)

    # Create the plot
    plt.figure(figsize=(15, 10))
    bars = plt.barh(articles, prices, color='purple', edgecolor='black')

    # Display the exact prices on the bars
    for bar in bars:
        plt.text(bar.get_width() - (0.02 * float(max(prices))),
                 bar.get_y() + bar.get_height() / 2,
                 '₡%.2f' % bar.get_width(),  # Display the price with 2 decimal places
                 ha='right', va='center',
                 color='white', fontsize=10)

    # Set the title and labels
    plt.title('Top 10 Most Expensive Articles')
    plt.xlabel('Price')
    plt.ylabel('Article Name')
    plt.tight_layout()
    # Reverse the y-axis to have the most expensive article at the top
    plt.gca().invert_yaxis()
    plt.ticklabel_format(style='plain', axis='x')
    plt.show()


def plot_article_count_by_subcategory(data):
    """
    Plot the number of articles for each subcategory.

    :param data: List of tuples, where each tuple contains the subcategory ID, subcategory name, and article count.
    """
    # Get the subcategory names
    subcategories = [row[1] for row in data]
    # Get the article counts
    counts = [row[2] for row in data]

    plt.figure(figsize=(15, 10))
    bars = plt.barh(subcategories, counts, color='skyblue', edgecolor='black')

    # Display the exact counts on the bars
    for bar in bars:
        plt.text(bar.get_width() - (0.02 * max(counts)),
                 bar.get_y() + bar.get_height() / 2,
                 '%d' % int(bar.get_width()),  # Text
                 ha='center', va='center',
                 color='black')

    # Set the title and labels
    plt.title('Number of Articles by Subcategory')
    plt.xlabel('Number of Articles')
    plt.ylabel('Subcategory')
    plt.tight_layout()
    # Reverse the order on the y-axis to have the subcategory with the most articles at the top
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    # Connection credentials
    HOST = 'localhost'
    DBNAME = 'unimart'
    USER = 'postgres'
    PASSWORD = 'root'
    PORT = '5432'

    db_manager = DatabaseManager(HOST, DBNAME, USER, PASSWORD, PORT)
    db_manager.connect()
    insert_category_from_excel(db_manager)
    insert_price_from_excel(db_manager)
    insert_subcategory_from_excel(db_manager)
    insert_brands_from_excel(db_manager)
    insert_type_from_excel(db_manager)
    insert_articule_from_excel(db_manager)
    #get_article_count_by_brand(db_manager)
    #get_article_count_by_subcategory(db_manager)
    #get_price_stats_by_category(db_manager)
    #most_expensive_articles(db_manager)
    db_manager.disconnect()
