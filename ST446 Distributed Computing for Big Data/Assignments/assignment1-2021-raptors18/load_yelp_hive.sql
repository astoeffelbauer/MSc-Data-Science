CREATE DATABASE IF NOT EXISTS yelp;

USE yelp;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
	user_id STRING,
	name STRING,
	review_count INT,
	yelping_since DATE,
	friends ARRAY<STRING>,
	useful INT,
	funny INT,
	cool INT,
	fans INT,
	elite ARRAY<STRING>,
	average_stars FLOAT,
	compliment_hot INT,
	compliment_more INT,
	compliment_profile INT,
	compliment_cute INT,
	compliment_list INT,
	compliment_note INT,
	compliment_plain INT,
	compliment_cool INT,
	compliment_funny INT,
	compliment_writer INT,
	compliment_photos INT,
	type STRING
)

ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe' STORED AS TEXTFILE;
ADD JAR /usr/lib/hive-hcatalog/share/hcatalog/hive-hcatalog-core-2.3.7.jar; /* add the jar file (may not be neccessary here as I have to reload it again anyway) */
LOAD DATA LOCAL INPATH 'data/yelp/yelp_academic_dataset_user.json' INTO TABLE users;
