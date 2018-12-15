DELIMITER $$
CREATE trigger insert_check_orderdetails before insert 
on orderdetails 
for each row BEGIN 
    IF NEW.orderLineNumber < 1 THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'orderLineNumber is invalid';
    END IF;

    IF  NEW.quantityOrdered < 1 THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'quantityOrdered is invalid';
    END IF;

    IF NEW.priceEach < 0.0 THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'priceEach is invalid';
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE trigger insert_check_products before insert 
on products 
for each row BEGIN 
    IF NEW.quantityInStock < 0 THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'quantityInStock is invalid';
    END IF;

    IF  NEW.buyPrice < 0.0 THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'buyPrice is invalid';
    END IF;

    IF NEW.MSRP < 0.0 THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'MSRP is invalid';
    END IF;
END$$
DELIMITER ;