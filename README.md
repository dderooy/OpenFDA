# Open FDA api with Redis cache

## setup

using a Mac workspace
 
```bash
$ git clone https://github.com/dderooy/OpenFDA.git

$ cd OpenFDA

$ brew install redis

$ brew services start redis

$ pipenv install requests

$ pipenv install redis

```
 

## cache design

Using Redis, the cache was designed to store hash maps for every drug in the form:

```
"ndc_id": {
    "brand_name": "string"
    "dosage_form": "string"
    "active_ing": "list_of_dict"
    "product_ndc": "string"
}
```

## notes

All the tests are passing however there is a lot to be improved. For one, I didn't have time to learn and setup a proper mock
framework in Python. A lot of code can be refactored based on that. Second, the cache was made using the mock endpoint. 
The cache schema can also be greatly improved since its a huge pain to search by anything other than product_ndc.

In conclusion the code is functional and in need of serious refactoring.  




