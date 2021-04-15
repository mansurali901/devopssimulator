/* Data Insertion for Apache
command = commad need to execute in container
find    = conditions to search against output of container command
tasks   = name of the task contestent did
status  = statuf of the rule 0 or 1 
stage   = at what level tasks is performing
*/
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('dpkg -l apache2', 'code=0','server', '1', 'apache');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('netstat -ntlap |grep :80 |grep apache', '0.0.0.0:80', 'portverify', '1', 'apache');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('curl -i web1.10pearls.com', '200', 'alias', '1', 'apache');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('ls -la /usr/share/doc/html/', 'root', 'directory', '1', 'apache');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('curl -i --insecure https://web1.10pearls.com', '200', 'ssl', '1', 'apache');


INSERT INTO conditions (command, find, task, status, stage ) VALUES ('dpkg -l mysql-server', 'Version','server', '1', 'mysql');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('netstat -ntlap |grep :3306 |grep -v 33060 |awk '{print $4}'', '0.0.0.0:3306','server', '1', 'mysql');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('/opt/scripts/enginecheck.sh', 'InnoDB','engine', '1', 'mysql');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('/opt/scripts/dbcheck.sh', '10PearlsDB','dbcheck', '1', 'mysql');

