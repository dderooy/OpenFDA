import unittest
from endpoint import Endpoint


class TestQueries(unittest.TestCase):

    def test_mock_request(self):
        endpoint = Endpoint("mock")
        response = endpoint.make_request(None, "warfarin")
        obj = response.json()
        self.assertTrue("200", response.status_code)
        # print(obj["results"][0]["brand_name"])
        self.assertEqual("Warfarin Sodium", obj["results"][0]["brand_name"])

    def test_fda_request(self):
        endpoint = Endpoint("fda")
        response = endpoint.make_request("brand_name:warfarin", None)
        obj = response.json()
        self.assertTrue("200", response.status_code)
        # print(obj["results"][0]["brand_name"])
        self.assertEqual("Warfarin Sodium", obj["results"][0]["brand_name"])

    def test_get_fda_ndc(self):
        endpoint = Endpoint("fda")
        ndc = endpoint.get_product_ndc("warfarin")
        # print(ndc)
        self.assertEqual("53217-001", ndc)

    def test_get_pharm_class(self):
        endpoint = Endpoint("fda")
        pharm_class = endpoint.get_pharm_class("warfarin")
        print pharm_class

    def test_create_cache(self):
        endpoint = Endpoint("mock")
        endpoint.create_cache()






if __name__ == '__main__':
        unittest.main()