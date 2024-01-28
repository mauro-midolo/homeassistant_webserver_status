import unittest
#import sys
#sys.path.append("..")
from custom_components.webserver_status.http.httpvalidator import HttpValidator


class HttpValidatorTest(unittest.TestCase):

    def test_should_exists(self):
        HttpValidator()
        assert True
        
    def test_should_return_false_if_not_url(self):
        assert HttpValidator().is_valid("NoValidUrl") == False
    
    def test_should_return_true_if_url_in_https_is_valid(self):
        assert HttpValidator().is_valid("https://www.google.it") == True

    def test_should_return_true_if_url_with_path_is_valid(self):
        assert HttpValidator().is_valid("https://it.wikipedia.org/wiki/Carlo_Magno") == True

if __name__ == '__main__':
    unittest.main()