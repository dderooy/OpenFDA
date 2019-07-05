import requests
import redis
import json


class Endpoint:

    def __init__(self, name):
        self.name = name
        self.limit = 1
        self.cache = redis.Redis(
            host='localhost',
            port=6379,
            db=0)
        self.cache_ndc_ids = []

    def make_request(self, search, drug):

        if self.name == "mock":
            url = "https://biosym-code-challenge.herokuapp.com/drug/{}".format(drug)
            headers = {
                'Cache-Control': "no-cache",
                'Postman-Token': "a99ac8b5-d0b1-44f1-bc8c-f353e811874e"
            }

            try:
                response = requests.request("GET", url, headers=headers)
            except requests.exceptions.HTTPError as err:
                print err

            return response

        if self.name == "fda":
            url = "https://api.fda.gov/drug/ndc.json"
            querystring = {}
            querystring["search"] = search
            querystring["limit"] = self.limit
            headers = {
                'Cache-Control': "no-cache",
                'Postman-Token': "3635f576-df75-4c75-be6e-76cd1ac682f5"
            }

            try:
                response = requests.request("GET", url, headers=headers, params=querystring)
            except requests.exceptions.HTTPError as err:
                print err

            return response

    def get_product_ndc(self, brand_name):
        if self.name == "fda":
            search = "brand_name:{}".format(brand_name)
            resp = (self.make_request(search, None)).json()
            return resp["results"][0]["product_ndc"]

        if self.name == "mock":
            resp = (self.make_request(None, brand_name)).json()
            return resp["results"][0]["product_ndc"]

    def get_pharm_class(self, brand_name):
        if self.name == "fda":
            search = "brand_name:{}".format(brand_name)
            resp = (self.make_request(search, None)).json()
            return self.create_pharm_dict(resp)

        if self.name == "mock":
            resp = (self.make_request(None, brand_name)).json()
            return self.create_pharm_dict(resp)

    def create_pharm_dict(self, resp):
        if "pharm_class" in resp["results"][0]:
            pharm_class = resp["results"][0]["pharm_class"]
            return self.parse_string(pharm_class)

        elif "pharm_class" not in resp["results"][0]:
            openfda = resp["results"][0]["openfda"]
            pharm_list = []
            if "pharm_class_cs" in openfda:
                for s in openfda["pharm_class_cs"]:
                    pharm_list.append(s)
            if "pharm_class_epc" in openfda:
                for s in openfda["pharm_class_epc"]:
                    pharm_list.append(s)
            if "pharm_class_moa" in openfda:
                for s in openfda["pharm_class_moa"]:
                    pharm_list.append(s)
            if "pharm_class_pe" in openfda:
                for s in openfda["pharm_class_pe"]:
                    pharm_list.append(s)
            return self.parse_string(pharm_list)

        else:
            raise ValueError("Error: {}\n. There is not pharm_class data")

    @staticmethod
    def parse_string(list):
        pharm_dict = {}
        for s in list:
            category = (s[s.find("[") + 1:s.find("]")]).encode("utf-8")
            s = (s.replace("[" + category + "]", "").strip(" ")).encode("utf-8")
            if category in pharm_dict:
                pharm_dict[category].append(s)
            else:
                pharm_dict[category] = [s]
        return pharm_dict

    def create_cache(self):
        preload = ["warfarin", "aspirin", "plavix", "lipitor", "vancomycin", "ampicillin", "fentanyl", "metformin", "zoloft", "lantus"]

        if self.name == "mock":
            product = {}

            for name in preload:
                resp = (self.make_request(None, name)).json()
                product_ndc = resp["results"][0]["product_ndc"]

                product["product_ndc"] = product_ndc
                product["brand_name"] = resp["results"][0]["brand_name"]
                product["dosage_form"] = resp["results"][0]["dosage_form"]
                product["active_ingredients"] = json.dumps(resp["results"][0]["active_ingredients"])
                self.cache.hmset(product_ndc, product)
                self.cache_ndc_ids.append(product_ndc)


    def query_cache(self, id, tag, search_list):
        ans = []
        if tag == "product_ndc":
            for tagstring in search_list:
                value = self.cache.hget(id, tagstring)
                if tagstring == "active_ingredients":
                    value = json.loads(value.encode("utf-8"))
                ans_dict = {}
                ans_dict[tagstring] = value
                ans.append(ans_dict)
            return ans

        for product_ndc in self.cache_ndc_ids:
            value = self.cache.hget(product_ndc, tag)
            if tag == "active_ingredients":
                value = json.loads(value.encode("utf-8"))
                for obj in value:
                    if obj["name"] == id:
                        for tagstring in search_list:
                            ans_tag = self.cache.hget(product_ndc, tagstring)
                            ans_dict = {}
                            ans_dict[tagstring] = ans_tag
                            ans.append(ans_dict)
            elif value == id:
                for tagstring in search_list:
                    ans_tag = self.cache.hget(product_ndc, tagstring)
                    ans_dict = {}
                    ans_dict[tagstring] = ans_tag
                    ans.append(ans_dict)
        return ans



