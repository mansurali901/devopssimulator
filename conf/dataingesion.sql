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
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('python3 /opt/scripts/enginecheck.py', 'InnoDB','engine', '1', 'mysql');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('python3 /opt/scripts/print.py', '10PearlsDB','dbcheck', '1', 'mysql');
INSERT INTO conditions (command, find, task, status, stage ) VALUES ('python3 /opt/scripts/usercheck.py', 'User-has','dbcheck', '1', 'mysql');


/* Migrations for tasks*/
 insert into tasks (taskName, taskCode) values ('apache', '0001')
 insert into tasks (taskName, taskCode) values ('mysql', '0002');
 insert into tasks (taskName, taskCode) values ('aws', '0003');