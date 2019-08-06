
# Flask: Company Logo Generation API

### Description
The application depends on a webservices which old the list of company info
`https://next.json-generator.com/api/json/get/4JlWH4WlD`


# Setup  
```sh
Install requirements
$ pip install requests 
$ pip install requests_cache
Run app 
$ python app.py
```

## API Endpoint 
*URL* `http://localhost:8888/api/v1/company/generate_logo?id=<COMPANY_ID>`

*Example* : `http://localhost:8888/api/v1/company/generate_logo?id=C004`

*Heroku* `https://quiet-inlet-39335.herokuapp.com`

## Response
```
{
    "companyId": "C004",
    "companyName": "Apple",
    "logoCharacters": "P, A, E",
    "message": "Logo generated!!",
    "status": 0
}
```




