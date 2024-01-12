from django.test import TestCase #this is the test case class
from django.shortcuts import reverse #this is the reverse function

class LandingPageViewTest(TestCase): #this is the landing page view test class that inherits from the test case class
    def test_status_code(self):
        # TODO - test that status code is 200
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(response.status_code, 200)

    def test_template_name(self): #this is the test template name function that tests the template name of the landing page
        response = self.client.get(reverse('landing-page'))
        self.assertTemplateUsed(response, 'landing.html')