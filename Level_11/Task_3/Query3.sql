create database HRSystem;
USE hrsystem;
INSERT INTO employee(id,name,department,salary) VALUES (6, 'Fiona', 'Sales', 50000),(7, 'George', 'Sales', 48000);
select * from employee;
select department, avg(salary) as avg_salary from employee where department='Engineering';
select department, avg(salary) as avg_salary from employee group by department having avg_salary>60000;