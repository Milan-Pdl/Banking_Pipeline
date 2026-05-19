-- 1. Insert into CUSTOMER
INSERT INTO CUSTOMER (cust_id, name, address, phone_number, postal_code, country, email, father_name, mother_name, occupation, education, nationality) VALUES
('CUST001', 'Aayush Shrestha', 'New Baneshwor, Kathmandu', '+977-9851012345', '44600', 'Nepal', 'aayush.shrestha@email.com', 'Ram Shrestha', 'Sita Shrestha', 'Software Engineer', 'Bachelors', 'Nepali'),
('CUST002', 'Pooja Thapa', 'Lakeside, Pokhara', '+977-9841098765', '33700', 'Nepal', 'pooja.thapa@email.com', 'Hari Thapa', 'Gita Thapa', 'Banker', 'Masters', 'Nepali'),
('CUST003', 'Rajesh Hamal', 'Siddharthanagar, Bhairahawa', '+977-9801234567', '32900', 'Nepal', 'rajesh.hamal@email.com', 'Krishna Hamal', 'Radha Hamal', 'Business Owner', 'High School', 'Nepali');

-- 2. Insert into PRODUCT
INSERT INTO PRODUCT (product_id, schm_type, schm_code, product_desc) VALUES
('PROD001', 'SAV', 'GEN_SAV', 'General Savings Account'),
('PROD002', 'SAV', 'SMR_SAV', 'Samriddhi Premium Savings Account'),
('PROD003', 'CUR', 'BUS_CUR', 'Business Current Account');

-- 3. Insert into BRANCH
INSERT INTO BRANCH (branch_id, province, cluster_name, city_name, branch_name) VALUES
('BR001', 'Bagmati', 'Kathmandu Valley', 'Kathmandu', 'Kantipath Main Branch'),
('BR002', 'Gandaki', 'Western Cluster', 'Pokhara', 'Lakeside Branch'),
('BR003', 'Lumbini', 'Terai Region', 'Bhairahawa', 'Siddharthanagar Branch');

-- 4. Insert into ACCOUNT
INSERT INTO ACCOUNT (account_id, customer_id, branch_id, product_id, account_balance, lien_amt, acct_cls_flg, schm_type, schm_code, acct_crncy_code) VALUES
('ACC1000001', 'CUST001', 'BR001', 'PROD001', 150000.00, 0.00, 'N', 'SAV', 'GEN_SAV', 'NPR'),
('ACC1000002', 'CUST002', 'BR002', 'PROD002', 750500.50, 10000.00, 'N', 'SAV', 'SMR_SAV', 'NPR'),
('ACC1000003', 'CUST003', 'BR003', 'PROD003', 2500000.00, 0.00, 'N', 'CUR', 'BUS_CUR', 'NPR');

-- 5. Insert into CARD
INSERT INTO CARD (card_number, account_id, balance, card_type, closing_balance, card_expiry_date) VALUES
('4000123456789010', 'ACC1000001', 150000.00, 'DEBIT', 0.00, '2030-12-31'),
('5100987654321020', 'ACC1000002', 50000.00, 'CREDIT', 12500.00, '2029-05-15');

-- 6. Insert into TRANSACTION
INSERT INTO TRANSACTION (transaction_id, account_id, card_number, transaction_date, transaction_type, amount, currency_code, channel, reference_number, transaction_status, description) VALUES
('TXN20260519001', 'ACC1000001', '4000123456789010', CURRENT_TIMESTAMP, 'WITHDRAWAL', 5000.00, 'NPR', 'ATM', 'REF987654321', 'SUCCESS', 'ATM Cash Withdrawal - Kantipath'),
('TXN20260519002', 'ACC1000002', NULL, CURRENT_TIMESTAMP, 'TRANSFER_IN', 25000.00, 'NPR', 'MOBILE_BANKING', 'REF112233445', 'SUCCESS', 'Fonepay transfer received from Nabil Bank'),
('TXN20260519003', 'ACC1000003', NULL, CURRENT_TIMESTAMP, 'TRANSFER_OUT', 120000.00, 'NPR', 'INTERNET_BANKING', 'REF556677889', 'PENDING', 'Vendor payment via ConnectIPS');