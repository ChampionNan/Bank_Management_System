Delimiter //
drop procedure if exists CHANGE_BANK_NAME; 
CREATE PROCEDURE CHANGE_BANK_NAME(
    IN oldBankName CHAR(128),
    IN newBankName CHAR(128),
    OUT result INT
)
BEGIN
	Declare tempCount INT Default 0;
    SELECT COUNT(*) INTO tempCount 
    FROM DUAL 
    WHERE EXISTS(SELECT NULL FROM SUB_BANK WHERE BANK_NAME = newBankName);

    IF(tempCount > 0) THEN
        set result = 1;
    ELSE
        SELECT COUNT(*) INTO tempCount 
        FROM DUAL 
        WHERE EXISTS(SELECT NULL FROM SUB_BANK WHERE BANK_NAME = oldBankName);

        IF(tempCount = 0) THEN
            set result = 2;
        ELSE
            set foreign_key_checks = 0;
            UPDATE  SUB_BANK 
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        
            UPDATE  LOAN 
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        
            UPDATE  CUSTOMER_DEPOSIT_ACCOUNT
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        
            UPDATE  CUSTOMER_CHECK_ACCOUNT
            SET     BANK_NAME = newBankName
            WHERE   BANK_NAME = oldBankName;
        
            set foreign_key_checks = 1;
            set result = 0;
        END IF;
    END IF;
END //
Delimiter ; 
