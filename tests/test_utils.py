from django.test import TestCase
from bullhorn.utils import normalize_string, get_metadata


class UtilsTest(TestCase):

    metadata = 'Falcons,Corning,monster'
    denormalized_string = "Bob IS a GoD"
    normalized_string = "bob_is_a_god"

    def test_normalize(self):
        self.assertEquals(normalize_string(self.denormalized_string),
                          self.normalized_string)
        self.assertEquals(normalize_string(self.normalized_string),
                          self.normalized_string)

    def test_get_metadata(self):
        results = get_metadata(self.metadata)
        for meta in self.metadata.split(","):
            self.assertTrue(meta in results)
