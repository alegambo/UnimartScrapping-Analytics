CREATE TABLE Category (
    ID_Category SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE Subcategory (
    ID_Subcategory SERIAL PRIMARY KEY,
    ID_Category INTEGER REFERENCES Category(ID_Category) ON DELETE CASCADE,
    subcategory_name VARCHAR(255) NOT NULL
);
CREATE TABLE Type (
    ID_Type SERIAL PRIMARY KEY,
    ID_Subcategory INTEGER REFERENCES Subcategory(ID_Subcategory) ON DELETE CASCADE,
    type_name VARCHAR(255) NOT NULL
);
CREATE TABLE Brand (
    ID_Brand SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL
);

CREATE TABLE Price (
    ID_Price SERIAL PRIMARY KEY,
    Price DECIMAL(10, 2) NOT NULL,
    Notes TEXT
);

CREATE TABLE Article (
    ID_Article SERIAL PRIMARY KEY,
    ID_Brand INTEGER REFERENCES Brand(ID_Brand) ON DELETE SET NULL,
	ID_Price INTEGER REFERENCES Price(ID_Price) ON DELETE SET NULL,
	ID_Type INTEGER REFERENCES Type(ID_Type) ON DELETE SET NULL,
    article_name VARCHAR(255) NOT NULL	
);

CREATE TABLE PriceHistory (
    ID_History SERIAL PRIMARY KEY,
    ID_Article INTEGER REFERENCES Article(ID_Article) ON DELETE CASCADE,
    ID_Price INTEGER REFERENCES Price(ID_Price) ON DELETE SET NULL,
    DateChanged DATE NOT NULL,
    Notes TEXT
);
CREATE TABLE OfferPrice (
    ID_OfferPrice SERIAL PRIMARY KEY,
    ID_Article INTEGER REFERENCES Article(ID_Article) ON DELETE CASCADE,
    Price DECIMAL(10, 2) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    Notes TEXT
);

CREATE INDEX idx_category_name ON Category(category_name);


CREATE INDEX idx_subcategory_name ON Subcategory(subcategory_name);


CREATE INDEX idx_brand_name ON Brand(brand_name);


CREATE INDEX idx_price ON Price(Price);

CREATE INDEX idx_article_name ON Article(article_name);

CREATE INDEX idx_type_name ON Type(type_name);


