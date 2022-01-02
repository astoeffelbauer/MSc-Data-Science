ADD JAR /usr/lib/hive-hcatalog/share/hcatalog/hive-hcatalog-core-2.3.7.jar; /*add jar file*/

USE yelp; DESCRIBE users; /*get schema*/

SELECT count(*) FROM users; /*get rowcount*/

SELECT name, review_count FROM users ORDER BY review_count DESC LIMIT 10; /*get most active reviewers*/
