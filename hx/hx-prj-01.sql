use hx;
SET SESSION sql_mode = '';

LOAD DATA LOCAL INFILE '/Users/i070599/Documents/Balance.csv' INTO TABLE Balance FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/i070599/Documents/Withdraw.csv' INTO TABLE Withdraw FIELDS TERMINATED BY ',';

select *
from Balance 
where UserID not in(
	select UserID from Withdraw
);


select count(1)
from Balance T1 left join Withdraw T2 on T1.UserID = T2.UserID
;

select count(1)
from Balance T1 
where T1.UserID not in (select distinct UserID from Withdraw T2);
#360427 - > 360427 users with balance but never withdraw

select count(1)
from Withdraw T1 
where T1.UserID not in (select distinct UserID from Balance T2);
#873923

select count(1)
from Balance T1 left join Withdraw T2 on T1.UserID = T2.UserID;
#

select sum(T1.Balance), sum(T2.ToApprove), sum(T2.Succeed), sum(T2.Total)
from Balance T1 left join Withdraw T2 on T1.UserID = T2.UserID
group by T1.UserID;
#

select *
from withdraw
where UserID = 11;

select *
from balance
where UserId = 11;

select T1.UserID, T1.UserName, sum(ToApprove) as ToApprove, sum(Succeed) as Succeed, sum(Total) as Total
from Withdraw T1
group by T1.UserID, T1.UserName
INTO OUTFILE '/tmp/WithdrawSum.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
;

insert into WithdrawSum 
select T1.UserID, T1.UserName, sum(ToApprove) as ToApprove, sum(Succeed) as Succeed, sum(Total) as Total
from Withdraw T1
group by T1.UserID, T1.UserName
;

select UserID
from Balance T1
group by T1.UserID
having count(T1.UserID) > 1;
#null -> no duplicated UserID in Balance

select UserId, UserName, sum(ToApprove), sum(Succeed), sum(Total)
from withdraw
group by UserID, UserName;



select count(distinct(UserName)) from Withdraw;
#578370

select count(distinct(UserID)) from Withdraw;
#954289

select count(1) from Withdraw;
#967345

select * from Withdraw order by ID limit 10 ;

select UserID
from Withdraw 
group by UserID
having count(UserID) > 1;




select * from Withdraw T1, Withdraw T2 where T1.UserName = T2.UserName and T1.UserID <> T2.UserID;

select count(1) from withdraw;

CREATE TABLE `hx`.`Withdraw` (
  `UserID` INT NULL,
  `UserName` VARCHAR(45) NULL,
  `ToApprove` DECIMAL(16,2) NULL,
  `Succeed` DECIMAL(16,2) NULL,
  `Total` DECIMAL(16,2) NULL,
  `ID` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID`));

DROP table `hx`.`Balance`;

CREATE TABLE `Balance` (
  `UserID` INT NOT NULL,
  `Balance` DECIMAL(16,2) NULL,
  `IDCard` VARCHAR(20) NULL,
  `Mobile` VARCHAR(20) NULL,
  PRIMARY KEY (`UserID`));


select count(1) from Account;

#delete from Account
select * from Account limit 10;

#empty IdCard number
select count(1)
from Account
where IDCard = '';

#duplicated IdCard, include empty IDCard
select IDCard, count(1)
from Account
group by IDCard
having count(1) > 1;


#18,370,886.830000
select sum(Balance), count(1)
from Account 
where IDCard not in(
select IDCard
from Account
group by IDCard
having count(1) > 1
) and length(IDCard) = 18;

#27185401.440000
select sum(balance) from account;

#451405
select count(1) from account;

#448082
select count(1) from account where length(IDCard) >= 15;

#125
select count(1) from account where length(IDCard) < 15 and IDCard <> '';

#IDCard length 15~17
select *, length(IDCard) as IDCardLen from account where length(IDCard)>=15 and length(IDCard) <=17 order by length(IDCard);
#0
select * from account where length(IDCard) > 18;

select max(balance), min(balance) from account;

select * from account order by balance asc limit 10;

select * from account
order by balance desc 
limit 10;

select count(1), round(balance / 10000)
from account
group by round(balance / 10000) 
order by round(balance / 10000);

select * from Balance order by ID asc limit 10 ;

select count(1) from WithdrawSum;

delete from Balance;
drop table Balance;

select T1.UserID, T2.UserName, T1.Balance, T2.ToApprove, T2.Succeed, T2.Total
from Balance T1 left outer join WithdrawSum T2 on T1.UserID = T2.UserID
INTO OUTFILE '/tmp/BalanceWithdrawSum.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

select sum(T1.Balance), sum(T2.ToApprove), sum(T2.Succeed), sum(T2.Total)
from Balance T1 left outer join WithdrawSum T2 on T1.UserID = T2.UserID;
