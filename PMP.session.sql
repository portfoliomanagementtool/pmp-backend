
--@block
SELECT * FROM pg_catalog.pg_tables where SCHEMANAME = 'public';

--@block
SELECT * from asset;

--@block
INSERT INTO asset(ticker,category,name,description) values('REL','NSE','Reliance','This is test ');

--@block 
ALTER TABLE asset 
ADD PRIMARY KEY (ID);

--@block 
-- SET  FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE asset CASCADE;

--@block
INSERT INTO asset_pricing(ticker,market_traded,timestamp1,market_value,currency) values('REL',100,'2023-05-13',999,1);

--@block
SELECT * from asset_pricing;