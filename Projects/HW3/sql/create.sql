CREATE SCHEMA `csvcatalog`;

CREATE TABLE `csvcatalog`.`table` (
  `table_name` VARCHAR(64) NOT NULL,
  `file_name` TEXT NOT NULL,
  PRIMARY KEY (`table_name`));

CREATE TABLE `csvcatalog`.`column` (
  `table_name` VARCHAR(64) NOT NULL,
  `column_name` VARCHAR(64) NOT NULL,
  `column_type` ENUM('text', 'number') NOT NULL,
  `not_null` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`table_name`, `column_name`));

CREATE TABLE `csvcatalog`.`index` (
  `table_name` VARCHAR(64) NOT NULL,
  `index_name` VARCHAR(45) NOT NULL,
  `column_name` VARCHAR(45) NOT NULL,
  `index_type` ENUM('PRIMARY', 'UNIQUE', 'INDEX') NOT NULL,
  PRIMARY KEY (`table_name`, `index_name`,`column_name`));

ALTER TABLE csvcatalog.column ADD 
FOREIGN KEY (table_name) 
REFERENCES csvcatalog.table(table_name) ON DELETE CASCADE;

ALTER TABLE csvcatalog.index ADD 
FOREIGN KEY (table_name) 
REFERENCES csvcatalog.table(table_name) ON DELETE CASCADE;

ALTER TABLE csvcatalog.index ADD CONSTRAINT fk_column 
FOREIGN KEY (table_name,column_name)
REFERENCES csvcatalog.column(table_name,column_name) ON DELETE CASCADE;