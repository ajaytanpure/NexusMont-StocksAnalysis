--create database NexusMont
-----------------------------------------------------------------------------------------------
create TABLE Test.dbo.CUSTOM_SIGNAL (ID TINYINT NOT NULL, SIGNAL VARCHAR(5),PRIMARY KEY (ID))
-----------------------------------------------------------------------------------------------
insert into Test.dbo.CUSTOM_SIGNAL values(1,'BUY')
insert into Test.dbo.CUSTOM_SIGNAL values(2,'UP')
insert into Test.dbo.CUSTOM_SIGNAL values(3,'SELL')
insert into Test.dbo.CUSTOM_SIGNAL values(4,'DOWN')
insert into Test.dbo.CUSTOM_SIGNAL values(5,'IGNIS')
----------------------------------------------------------------------------------------------
create TABLE Test.dbo.CUSTOM_SETTINGS (NAME VARCHAR(15), VALUE DECIMAL(3))
-----------------------------------------------------------------------------------------------
insert into Test.dbo.CUSTOM_SETTINGS values('EX_SHORT_TERM', 3)
insert into Test.dbo.CUSTOM_SETTINGS values('SHORT_TERM', 5)
insert into Test.dbo.CUSTOM_SETTINGS values('MID_TERM', 10)
insert into Test.dbo.CUSTOM_SETTINGS values('LONG_TERM', 25)
insert into Test.dbo.CUSTOM_SETTINGS values('EX_LONG_TERM', 50)
-----------------------------------------------------------------------------------------------
CREATE TABLE Test.dbo.[CNX NIFTY 50] (COMPANY_NAME VARCHAR(30))
CREATE TABLE Test.dbo.[CNX NIFTY 200] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[ALL COMPANIES] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[CERTUS BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[CERTUS SELL] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[VELOX] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[VELOX BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[VELOX SELL] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[FUTURO BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[FUTURO SELL] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[SHORT BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[SHORT SELL] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[MID BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[MID SELL] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[LONG BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[LONG SELL] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[XSHORT BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[XSHORT SELL] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[XLONG BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[XLONG SELL] (COMPANY_NAME VARCHAR(30))

CREATE TABLE [Test].[dbo].[CERTUS-VELOX BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[CERTUS-VELOX SELL] (COMPANY_NAME VARCHAR(30))

CREATE TABLE [Test].[dbo].[FUTURO-VELOX BUY] (COMPANY_NAME VARCHAR(30))
CREATE TABLE [Test].[dbo].[FUTURO-VELOX SELL] (COMPANY_NAME VARCHAR(30))


-------------------------------------------------------------------------------------------------
--CREATE TABLE test.dbo.temp_test(REC_DATE DATE NOT NULL,
--OPEN_PRICE DECIMAL(8,2) NOT NULL,
--HIGH_PRICE DECIMAL(8,2) NOT NULL,
--LOW_PRICE DECIMAL(8,2) NOT NULL,
--CLOSE_PRICE DECIMAL(8,2) NOT NULL,

--SHRT_SIG TINYINT,
--SHRT_AVG DECIMAL(8,2),
--SHRT_CHNG DECIMAL(6,2),

--MID_SIG TINYINT,
--MID_AVG DECIMAL(8,2),
--MID_CHNG DECIMAL(6,2),

--LONG_SIG TINYINT,
--LONG_AVG DECIMAL(8,2),
--LONG_CHNG DECIMAL(6,2),

--CERTUS TINYINT,
--VELOX TINYINT,
--FUTURO TINYINT,


--PIVOT_VALUE DECIMAL(8,2),
--PIVOT_CHNG DECIMAL(6,2),
--STOCHASTIC DECIMAL(8,2),
--MOMENTUM DECIMAL(6,2),
--MOMENTUM_VARIATION DECIMAL(6,2),
--QUANTITY INT,
--TRADERS INT,

--EX_SHRT_SIG TINYINT,
--EX_SHRT_AVG DECIMAL(8,2),
--EX_SHRT_CHNG DECIMAL(6,2),
--EX_LONG_SIG TINYINT,
--EX_LONG_AVG DECIMAL(8,2),

--MACD DECIMAL(8,2),
--MACD_CHNG DECIMAL(6,2),


--PRIMARY KEY (REC_DATE),
--FOREIGN KEY (CERTUS) REFERENCES CUSTOM_SIGNAL(ID),
--FOREIGN KEY (VELOX) REFERENCES CUSTOM_SIGNAL(ID),
--FOREIGN KEY (FUTURO) REFERENCES CUSTOM_SIGNAL(ID),
--FOREIGN KEY (SHRT_SIG) REFERENCES CUSTOM_SIGNAL(ID),
--FOREIGN KEY (MID_SIG) REFERENCES CUSTOM_SIGNAL(ID),
--FOREIGN KEY (LONG_SIG) REFERENCES CUSTOM_SIGNAL(ID),
--FOREIGN KEY (EX_SHRT_SIG) REFERENCES CUSTOM_SIGNAL(ID),
--FOREIGN KEY (EX_LONG_SIG) REFERENCES CUSTOM_SIGNAL(ID)
--)
