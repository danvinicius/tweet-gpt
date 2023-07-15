DROP SCHEMA tweet_gpt;

CREATE SCHEMA tweet_gpt;
USE tweet_gpt;
CREATE USER IF NOT EXISTS 'user_tweet_gpt'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON tweet_gpt . * TO 'user_tweet_gpt'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE `User`(
	`id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
	`email` varchar(255) NOT NULL UNIQUE,
	`senha` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);
