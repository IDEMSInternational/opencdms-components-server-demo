# Test Data Server
This is a temporary folder used to run an adaptation of the test data server provided by https://github.com/opencdms/opencdms-test-data

It could also be replaced by the implementation found at https://github.com/openclimateinitiative/climsoft-api

## Running locally
`cd test-data-server`
```sh
docker-compose --file test-data-server/docker-compose.yml up
```
This will create a mariadb container, populate with the data from the exported sql file and publish on port `33308`

## Running on cloudsql
The database can also be hosted on cloudsql infrastructure and made available on demand. No particular configuration required beyond creating a new instance backed by mysql 8 and importing data

Note - due to minor differences between Mariadb and Mysql not all data will import correctly, so recommended just to import the `mariadb_climsoft_test_db_v4.sql` table as that is what is requried for the demo and has been tested as working. For access to existing cloud demo ask repo administrators