# GPS tracking API

The project, based on Django Framework and Django Rest Framework, provides API for GPS trackers to send location data to the server and to read these data by their owners.

**User registration**
----
  Returns an http status code.

* **URL:** `/register/`

* **Method:** `POST`
  
* **Data Params:**

  `{ "email" : "example@mail.com", "password" : "12345678" }`

* **Success Response:**

  **Code:** `HTTP_201_CREATED`
 
* **Error Response:**

  **Code:** `HTTP_404_NOT_FOUND`

**User login**
----
  Returns an authentication token.

* **URL:** `/login/`

* **Method:** `POST`
  
* **Data Params:**

  `{ "email" : "example@mail.com", "password" : "12345678" }`

* **Success Response:**

  * **Code:** `HTTP_200_OK`<br />
  * **Content:** `{ "token" : "012b3cf390fcd04aa9df503e3d08c23054f7fd90" }`
 
* **Error Response:**

  **Code:** `HTTP_404_NOT_FOUND`

**User logout**
----
  The authentication token required. Returns an http status code.

* **URL:** `/logout/`

* **Method:** `POST`
  
* **Success Response:**

  **Code:** `HTTP_200_OK`
 
* **Error Response:**

  **Content:** `{ "detail" : "Authentication credentials were not provided." }`

**Send entry**
----
  The authentication token required. Returns an http status code.

* **URL** `/devices/:device_id/entries/`

* **Method:** `POST`
  
* **Data Params:**

  `{ "latitude" : xx.xxx, "longitude" : xx.xxx, "datetime" : "mm/dd/YYYY HH:MM:SS" }`

* **Success Response:**

  **Code:** `HTTP_201_CREATED`
 
* **Error Response:**

  **Content:** `{ "detail" : "Authentication credentials were not provided." }`
  
**Get entries**
----
  The authentication token required. Receives a type of the returned data and a datetime string. Returns a json content of entries list which datetime is greater than or equal of the received datetime. If the parameter wasn't passed, it returns a list of all records.

* **URL** `/devices/:device_id/entries`

* **Method:** `GET`

* **Data Params:**

  `{ "datetime" : "mm/dd/YYYY HH:MM:SS" }`

* **Success Response:**

  **Code:** `HTTP_200_OK`
  
  **JSON:**
  
  ```
  { 
      "entries" : [ 
          { 
              "latitude" : xx.xxxxxx, 
              "longitude" : xx.xxxxxx, 
              "datetime" : "mm/dd/YYYY HH:MM:SS" 
          }, 
      ]
  }
  ```
  
  **KML:**
  
  ```
  <?xml version="1.0" encoding="UTF-8"?>
  <kml xmlns="http://earth.google.com/kml/2.1">
    <Document id="feat_1">
      <Placemark id="feat_2">
        <name>Point #1</name>
        <TimeStamp id="time_0">
          <when>mm/dd/YYYY HH:MM:SS</when>
        </TimeStamp>
        <Point id="geom_0">
          <coordinates>xx.xxxxxx,xx.xxxxxx,0.0</coordinates>
        </Point>
      </Placemark>
     </Document>
  </kml>
  ```
  
  **GPX:**
  
  ```
  <?xml version="1.0" encoding="UTF-8"?>
  <gpx>
    <trk>
      <name>Point #1</name>
      <trkseg>
        <trkpt lat="xx.xxxxxx" lon="xx.xxxxxx">
          <time>mm/dd/YYYY HH:MM:SS</time>
        </trkpt>
      </trkseg>
    </trk>
  </gpx>
  ```
  
 
* **Error Response:**

  **Content:** `{ "detail" : "Authentication credentials were not provided." }`
  
**Get devices**
----
  The authentication token required. Returns a json content.

* **URL** `/devices/`

* **Method:** `GET`

* **Success Response:**

  **Code:** `HTTP_200_OK`
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

  **Content:** `{ "detail" : "Authentication credentials were not provided." }`
