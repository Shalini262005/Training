CREATE TABLE department_stats (department VARCHAR(100) PRIMARY KEY,avg_salary DECIMAL(10, 2));
DELIMITER //
CREATE PROCEDURE CalculateAvgSalary(IN department_name varchar(100))
BEGIN
	DECLARE avg_salary DECIMAL(10,2);
    select avg(salary) into avg_salary from employee where department=department_name;
    insert into department_stats(department,avg_salary) values(department_name,avg_salary) on duplicate key update avg_salary=avg_salary;
END //
DELIMITER ;
CALL CalculateAvgSalary('Engineering');
select * from department_stats;