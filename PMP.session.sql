
--@block
SELECT * FROM pg_catalog.pg_tables where SCHEMANAME = 'public';

--@block
SELECT * from asset;

--@block
INSERT INTO asset(ticker,category,name,description) values('REL','MULTI','Reliance','This is Reliance Industry ');

--@block 
ALTER TABLE asset 
ADD PRIMARY KEY (ID);

--@block 
-- SET  FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE asset CASCADE;

--@block
INSERT INTO asset_pricing1(ticket,market_traded,timestamp1,market_value,currency) values('REL','BSE','2023-11-08 09:23:15',69,'INR');

--@block
SELECT * from pmp2.asset_pricing1;


--@block
Create DATABASE pmp;
Create DATABASE pmp2;


--@block
CREATE TABLE asset_pricing1 (
    Ticket text NOT NULL,
    Market_Traded text NOT NULL,
    market_value decimal NOT NULL,
    timestamp1 timestamptz NOT NULL,
    currency text NOT NULL,
    PRIMARY KEY (Ticket, Market_Traded,timestamp1)
);
--@block
ALTER TABLE asset_pricing1
ADD CONSTRAINT fk_asset_ticker
FOREIGN KEY (ticket)
REFERENCES Asset (Ticker);
SELECT create_hypertable('asset_pricing1', 'timestamp1');


--@block
-- Create the portfolio table
CREATE TABLE portfolio (
    UUID INT NOT NULL REFERENCES Users(UUID),
    transaction_id INT NOT NULL REFERENCES transaction(transaction_id),
    Ticker TEXT NOT NULL REFERENCES Asset(Ticker),
    current_ticker_value DECIMAL NOT NULL,
    invested_ticker_value DECIMAL NOT NULL,
    quantity DECIMAL NOT NULL,
    invested_value DECIMAL NOT NULL,
    current_value DECIMAL NOT NULL,
    percentage_change DECIMAL NOT NULL,
    timestamp3 TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    currency DECIMAL NOT NULL,
    PRIMARY KEY (Ticker, UUID, transaction_id, timestamp3)  -- Include timestamp3 in the primary key
);

-- Convert the table into a hypertable
SELECT create_hypertable('portfolio', 'timestamp3');

--@block
drop table portfolio;


--@block
CREATE DATABASE questionaire


--@block
select * from django_migrations 

--@block
delete from django_migrations where id=7;

--@block
DROP DATABASE pmp1;



