import unittest
from endpoint import Endpoint


class TestCase(unittest.TestCase):

    def test_part_1_look_up_product_ndc(self):
        # TODO: Complete test by adding call to method to look up product ndp for warfarin
        endpoint = Endpoint("mock")
        product_ndc = endpoint.get_product_ndc("warfarin")
        self.assertEqual(product_ndc, '71610-173')

    def test_part_2_lookup_pharm_classes_warfarin(self):
        # TODO: Complete test by adding call to method to look up pharm classes for warfarin
        endpoint = Endpoint("mock")
        pharm_classes = endpoint.get_pharm_class("warfarin")
        expected_mappings = {
            'EPC': ['Vitamin K Antagonist'],
            'MoA': ['Vitamin K Inhibitors']
        }
        self.assertDictEqual(pharm_classes, expected_mappings)

    def test_part_2_lookup_pharm_classes_aspirin(self):
        # TODO: Complete test by adding call to method to look up pharm classes for aspirin
        endpoint = Endpoint("mock")
        pharm_classes = endpoint.get_pharm_class("aspirin")
        expected_mappings = {
            'Chemical/Ingredient': ['Nonsteroidal Anti-inflammatory Compounds'],
            'PE': ['Decreased Prostaglandin Production', 'Decreased Platelet Aggregation'],
            'EPC': ['Nonsteroidal Anti-inflammatory Drug', 'Platelet Aggregation Inhibitor'],
            'MoA': ['Cyclooxygenase Inhibitors']
        }

        self.assertDictEqual(pharm_classes, expected_mappings)

    def test_part_4_look_up_active_ingredients_for_product_ndc(self):
        # TODO: Complete test by adding call to look up the 'active_ingredients' for the product_ndc: '21695-665'
        # Example lookup_method('21695-665', 'product_ndc', ['active_ingredients'])
        endpoint_cache = Endpoint("mock")
        endpoint_cache.create_cache()

        results = endpoint_cache.query_cache('21695-665', 'product_ndc', ['active_ingredients'])
        self.assertEqual(results[0]['active_ingredients'], [{
            "strength": "75 mg/1",
            "name": "CLOPIDOGREL BISULFATE"
        }])

    def test_part_4_look_up_all_product_ndc_for_ingredients(self):
        # TODO: Complete test by adding call to look up the 'product_ndc' for the drugs which have
        #  `CLOPIDOGREL BISULFATE` as an 'active_ingredients'
        # Example: lookup_method('CLOPIDOGREL BISULFATE', 'active_ingredients', ['product_ndc'])
        endpoint_cache = Endpoint("mock")
        endpoint_cache.create_cache()

        results = endpoint_cache.query_cache('CLOPIDOGREL BISULFATE', 'active_ingredients', ['product_ndc'])
        self.assertEqual(results[0]['product_ndc'], '21695-665')

    def test_query_by_brand_name(self):
        endpoint_cache = Endpoint("mock")
        endpoint_cache.create_cache()

        results = endpoint_cache.query_cache('Aspirin', 'brand_name', ['product_ndc'])
        self.assertEqual(results[0]['product_ndc'], '0615-8058')


if __name__ == '__main__':
    unittest.main()
