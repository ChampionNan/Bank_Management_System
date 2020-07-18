Delimiter //
drop procedure if exists CHANGE_EMPLOYEE_NAME;
CREATE PROCEDURE CHANGE_EMPLOYEE_NAME(
    In oldBankName CHAR(128),
    In newBankName CHAR(128),
    Out result INT
)
BEGIN
	Declare tempCount INT default 0;
    SELECT COUNT(*) INTO tempCount 
    FROM DUAL 
    WHERE EXISTS(SELECT NULL FROM EMPLOYEE WHERE EMPLOYEE_ID = newBankName);

    IF(tempCount > 0) THEN
        set result = 1;
    ELSE
        SELECT COUNT(*) INTO tempCount 
        FROM DUAL 
        WHERE EXISTS(SELECT NULL FROM EMPLOYEE WHERE EMPLOYEE_ID = oldBankName);

        IF(tempCount = 0) THEN
            set result = 2;
        ELSE
            set foreign_key_checks=0;
            UPDATE  EMPLOYEE 
            SET     EMPLOYEE_ID = newBankName
            WHERE   EMPLOYEE_ID = oldBankName;
       
            UPDATE  EMPLOYEE_CUSTOMER 
            SET     EMPLOYEE_ID = newBankName
            WHERE   EMPLOYEE_ID = oldBankName;
			set foreign_key_checks=1;
            set result = 0;
        END IF;
    END IF;
END //
Delimiter ;
