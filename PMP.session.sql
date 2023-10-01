
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