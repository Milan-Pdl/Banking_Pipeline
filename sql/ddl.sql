-- 1. Create CUSTOMER Table
CREATE TABLE CUSTOMER (
    cust_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    postal_code VARCHAR(10),
    country VARCHAR(50),
    email VARCHAR(100),
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    occupation VARCHAR(80),
    education VARCHAR(50),
    nationality VARCHAR(50)
);

-- 2. Create PRODUCT Table
CREATE TABLE PRODUCT (
    product_id VARCHAR(10) PRIMARY KEY,
    schm_type VARCHAR(5),
    schm_code VARCHAR(10),
    product_desc VARCHAR(100)
);

-- 3. Create BRANCH Table
CREATE TABLE BRANCH (
    branch_id VARCHAR(10) PRIMARY KEY,
    province VARCHAR(50),
    cluster_name VARCHAR(50),
    city_name VARCHAR(50),
    branch_name VARCHAR(100) NOT NULL
);

-- 4. Create ACCOUNT HUB TABLE
CREATE TABLE ACCOUNT (
    account_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10) REFERENCES CUSTOMER(cust_id),
    branch_id VARCHAR(10) REFERENCES BRANCH(branch_id),
    product_id VARCHAR(10) REFERENCES PRODUCT(product_id),
    account_balance NUMERIC(15,2) DEFAULT 0.00,
    lien_amt NUMERIC(15,2) DEFAULT 0.00,
    acct_cls_flg CHAR(1) CHECK (acct_cls_flg IN ('Y', 'N')),
    schm_type VARCHAR(5),
    schm_code VARCHAR(10),
    acct_crncy_code VARCHAR(5)
);

-- 5. Create CARD Table
CREATE TABLE CARD (
    card_number VARCHAR(25) PRIMARY KEY,
    account_id VARCHAR(10) REFERENCES ACCOUNT(account_id),
    balance NUMERIC(15,2) DEFAULT 0.00,
    card_type VARCHAR(10) CHECK (card_type IN ('DEBIT', 'CREDIT')),
    closing_balance NUMERIC(15,2) DEFAULT 0.00,
    card_expiry_date DATE
);

-- Create TRANSACTION Table
CREATE TABLE TRANSACTION (
    transaction_id VARCHAR(20) PRIMARY KEY,
    account_id VARCHAR(10) NOT NULL REFERENCES ACCOUNT(account_id),
    card_number VARCHAR(25) REFERENCES CARD(card_number), -- Optional: populated if a card was used
    transaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    transaction_type VARCHAR(15) CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER_IN', 'TRANSFER_OUT', 'FEE', 'INTEREST')),
    amount NUMERIC(15,2) NOT NULL CHECK (amount > 0),
    currency_code VARCHAR(5) DEFAULT 'USD',
    channel VARCHAR(20) CHECK (channel IN ('ATM', 'BRANCH', 'MOBILE_BANKING', 'INTERNET_BANKING', 'POS')),
    reference_number VARCHAR(50) UNIQUE, -- Unique tracking number from the payment gateway/switch
    transaction_status VARCHAR(15) DEFAULT 'PENDING' CHECK (transaction_status IN ('PENDING', 'SUCCESS', 'FAILED', 'REVERSED')),
    description TEXT
);

-- Index for optimized lookup performance on accounts (highly recommended for transactional tables)
CREATE INDEX idx_transaction_account ON TRANSACTION(account_id);
CREATE INDEX idx_transaction_date ON TRANSACTION(transaction_date);