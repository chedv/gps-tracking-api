# GPS tracking API

The project, based on Django Framework and Django Rest Framework, provides API for GPS trackers to send location data to server and to read these data by their owners. Other features are under developing.

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
  The authentication token required. Receives a datetime string and returns a json content of entries list which datetime is greater than or equal of the received datetime. If the parameter wasn't passed, it returns a list of all records.

* **URL** `/devices/:device_id/entries/`

* **Method:** `GET`

* **Success Response:**

  **Code:** `HTTP_200_OK`
  **Content:** 
  
  ```
  { 
      "entries" : [ 
          { 
              "latitude" : xx.xxx, 
              "longitude" : xx.xxx, 
              "datetime" : "mm/dd/YYYY HH:MM:SS" 
          }, 
      ]
  }
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
