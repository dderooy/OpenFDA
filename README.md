# BioSymetrics Code Challenge

## setup

using a Mac workspace
 
```bash
$ git clone https://github.com/dderooy/BioSymetrics.git

$ cd BioSymetrics

$ pipenv install requests

$ pipenv install redis

```
 

## cache design

```json
"ndc_id": {
    "brand_name": string
    "dosage_form": string
    "active_ing": list
}
```

