# GPS tracking API

The project, based on Django Framework and Django Rest Framework, provides API for GPS trackers to send location data to the server and to retrieve these data by their owners using JSON, KML and GPX formats.

**User registration**
----
  Returns an http status code.

* **URL:** `/register`

* **Method:** `POST`
  
* **Data Params:**

  Supported JSON format:

  `{ "email" : "example@mail.com", "password" : "12345678" }`

* **Success Response:**

  **Code:** `HTTP 201 CREATED`
 
* **Error Response:**

  **Code:** `HTTP 404 NOT FOUND`

**User login**
----
  Returns an authentication token.

* **URL:** `/login`

* **Method:** `POST`
  
* **Data Params:**

  Supported JSON format:

  `{ "email" : "example@mail.com", "password" : "12345678" }`

* **Success Response:**

  * **Code:** `HTTP 200 OK`<br />
  * **Content:** `{ "token" : "012b3cf390fcd04aa9df503e3d08c23054f7fd90" }`
 
* **Error Response:**

  **Code:** `HTTP 404 NOT FOUND`

**User logout**
----
  The authentication token is required. Returns an http status code.

* **URL:** `/logout`

* **Method:** `POST`
  
* **Success Response:**

  **Code:** `HTTP 200 OK`
 
* **Error Response:**

  **Content:** `{ "detail" : "Authentication credentials were not provided." }`

**Send entry**
----
  The authentication token is required. Returns an http status code.

* **URL:** `/devices/:device_id/entries`

* **Method:** `POST`
  
* **Data Params:**

  **JSON**

  ```
  { 
      "latitude" : xx.xxxxxx, 
      "longitude" : xx.xxxxxx, 
      "datetime" : "mm/dd/YYYYTHH:MM:SSZ" 
  }
  ```
  
  **NMEA**
  
  ```
  $GPRMC,125504.049,A,5542.2389,N,03741.6063,E,0.19,25.82,200919,,,*17
  ```

* **Success Response:**

  **Code:** `HTTP 201 CREATED`
 
* **Error Response:**

  **Content:** `{ "detail" : "Authentication credentials were not provided." }`
  
**Get entries**
----
  The authentication token is required. Receives `accept-type` and `datetime` parameters. Returns collected entries. If the parameter `datetime` wasn't passed, the response contains all of the records.

* **URL:** `/devices/:device_id/entries`

* **Method:** `GET`

* **Success Response:**

  **Code:** `HTTP 200 OK`
  
  **JSON**
  
  ```
  { 
      "entries" : [ 
          { 
              "latitude" : xx.xxxxxx, 
              "longitude" : xx.xxxxxx, 
              "datetime" : "mm/dd/YYYYTHH:MM:SSZ" 
          }, 
      ]
  }
  ```
  
  **KML**
  
  ```
  <?xml version="1.0" encoding="utf-8"?>
  <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
          <name>entries</name>
          <Placemark>
              <name>Point #1</name>
              <TimeStamp>
                  <when>mm/dd/YYYYTHH:MM:SSZ</when>
              </TimeStamp>
              <Point>
                  <coordinates>xx.xxxxxx,xx.xxxxxx</coordinates>
              </Point>
          </Placemark>
      </Document>
  </kml>
  ```
  
  **GPX**
  
  ```
  <?xml version="1.0" encoding="utf-8"?>
  <gpx xmlns="http://www.topografix.com/GPX/1/1">
      <name>entries</name>
      <wpt lat="xx.xxxxxx" lon="xx.xxxxxx">
          <time>mm/dd/YYYYTHH:MM:SSZ</time>
          <name>Point #1</name>
      </wpt>
  </gpx>
  ```
  
 
* **Error Response:**

  **Content:** `{ "detail" : "Authentication credentials were not provided." }`
  
**Get devices**
----
  The authentication token is required. Returns all added devices using JSON format.

* **URL:** `/devices/`

* **Method:** `GET`

* **Success Response:**

  **Code:** `HTTP 200 OK`
  
  **Content:** 
  
  ```
  { 
      "devices" : [ 
          { 
              "id" : "1234123412341234", 
              "name" : "example_name"
          }, 
      ]
  }
  ```
 
* **Error Response:**

  **JSON Content:** `{ "detail" : "Authentication credentials were not provided." }`
