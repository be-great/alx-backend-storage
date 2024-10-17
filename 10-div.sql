-- create a function that divide two numbers
DELIMITER //
CREATE FUNCTION SafeDiv(a INT, B INT) RETURNS FLOAT
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;

END;
//
DELIMITER ;
