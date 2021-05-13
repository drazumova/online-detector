# online-detector

The project for my bachelor thesis. This is a web application using browser fingerprinting to interact with users. An application responses user activity status (ONLINE, OFFLINE, SLEEP) based on calculated fingerprint. Also, it is storing fingerprint parameters in the Clickhouse database for future analytics.


## Application

The application separated into four modules. The main module named user_status_service parses users requests, collects fingerprint parameters and communicate with fingerprint block and database to found out  user last online time. Fingerprint block calculates a fingerprint and stores it to the database. Data processing block implements asynchronous queue for future analytics data saving, also where are geoip module that complements data with location information based on http request ip.


## Configuration

Configuration for docker containers and kubernetes services located in the `conf` folder. 


## Browser fingerprints

In the `main` branch, the fingerprint is computed using the http headers. In the `js-feeatures` branch, [FingerprintJS](https://github.com/fingerprintjs/fingerprintjs) is used to get more parameters. 



Hash comparison links 
* https://github.com/Cyan4973/xxHash
* https://github.com/rurban/smhasher/
