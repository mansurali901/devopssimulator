/* Main DB creation */
CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;
CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/* Initial Account creation */
INSERT INTO `accounts` (
	`id`, `username`, 
	`password`, 
	`email`) VALUES 
	(1, 'test', 'test', 'test@test.com'
	);

/* results table creation */

 create table scenarios (
	id int auto_increment NOT NULL, 
 	casenum varchar(10) NOT NULL, 
	validation varchar(10) NOT NULL, 
	username varchar(20), 
	task varchar(20), 
 	PRIMARY KEY(id)
	 );

/* Conditions Table */

CREATE TABLE conditions (      
	id MEDIUMINT NOT NULL AUTO_INCREMENT,      
	command VARCHAR(200) NOT NULL,  
	find VARCHAR(200) NOT NULL, 
	task VARCHAR(30), 
	status VARCHAR(10),   
	PRIMARY KEY (id) 
	);

 CREATE TABLE `tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskName` varchar(25) NOT NULL,
  `taskCode` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8
