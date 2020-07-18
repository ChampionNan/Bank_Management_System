Delimiter //
drop procedure if exists CHANGE_CUSTOMER_NAME;
CREATE PROCEDURE CHANGE_CUSTOMER_NAME(
    IN oldBankName CHAR(128),
    IN newBankName CHAR(128),
    OUT result  INT
)
BEGIN
	Declare tempCount INT Default 0;
    SELECT COUNT(*) INTO tempCount 
    FROM DUAL 
    WHERE EXISTS(SELECT NULL FROM CUSTOMER WHERE CUSTOMER_ID = newBankName);

    IF(tempCount > 0) THEN
        Set result = 1;
    ELSE
        SELECT COUNT(*) INTO tempCount 
        FROM DUAL 
        WHERE EXISTS(SELECT NULL FROM CUSTOMER WHERE CUSTOMER_ID = oldBankName);

        IF(tempCount = 0) THEN
            Set result = 2;
        ELSE
			set foreign_key_checks=0;
            UPDATE  CUSTOMER 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        
            UPDATE  EMPLOYEE_CUSTOMER 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        
            UPDATE  CUSTOMER_DEPOSIT_ACCOUNT 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        
            UPDATE  CUSTOMER_CHECK_ACCOUNT 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
        
            UPDATE  LOAN_CUSTOMER 
            SET     CUSTOMER_ID = newBankName
            WHERE   CUSTOMER_ID = oldBankName;
			
            set foreign_key_checks=1;
            
            set result = 0;
        END IF;
    END IF;
END //
Delimiter ;
