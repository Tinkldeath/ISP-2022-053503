Mysql query script:
    create user dbadmin identified by '12345';
    grant all on djangodatabase.*to 'dbadmin'@'%';

Then migrate