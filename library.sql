-- SQL Script for Library Management System

-- 1. Table: Books
CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    AuthorID INT NOT NULL,
    CategoryID INT NOT NULL,
    ISBN VARCHAR(20) UNIQUE NOT NULL,
    Availability BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- 2. Table: Members
CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Contact VARCHAR(15) UNIQUE NOT NULL,
    MembershipDate DATE NOT NULL
);

-- 3. Table: Librarians
CREATE TABLE Librarians (
    LibrarianID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Contact VARCHAR(15) UNIQUE NOT NULL
);

-- 4. Table: Transactions
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT NOT NULL,
    MemberID INT NOT NULL,
    IssueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- 5. Table: Fines
CREATE TABLE Fines (
    FineID INT PRIMARY KEY AUTO_INCREMENT,
    TransactionID INT NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

-- 6. Table: Categories
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100) NOT NULL UNIQUE
);

-- 7. Table: Authors
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    AuthorName VARCHAR(255) NOT NULL UNIQUE
);
