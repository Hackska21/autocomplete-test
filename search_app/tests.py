from rest_framework.test import APITestCase


class AutoCompleteTest(APITestCase):
    """
        Warning: This unit test are created with the default catalogue on mind loaded in migrations, this catalogue should be
        loaded in the test loader if the aproach changes
    """

    def setUp(self) -> None:
        self.sarch_path = "/search/"

    def get_first_suggestion(self, query="", latitude="", longitude=""):
        response = self.client.get(self.sarch_path, {"q": query, "latitude":latitude , "longitude": longitude})
        data = response.json()
        if not data:
            return None
        most_suggested = data[0]
        return most_suggested

    def test_1(self):
        """
            test if the first result is the most similar and nearest
        :return:
        """
        most_suggested = self.get_first_suggestion(query="londo", latitude="41.3", longitude="-72.1")
        self.assertEqual(most_suggested['name'], 'New London')


    def test_2(self):
        """
            test if the first result is the most similar without latitude and longitude
        :return:
        """
        most_suggested = self.get_first_suggestion(query="Londontowne")
        self.assertEqual(most_suggested['name'], 'Londontowne')


    def test_3(self):
        """
            negative test if there are no results
        :return:
        """
        most_suggested = self.get_first_suggestion(query="RadonmWord")
        self.assertEqual(most_suggested, None)

    def test_4(self):
        """
            only passing lattitude and longitude
        :return:
        """
        most_suggested = self.get_first_suggestion( latitude="41.3", longitude="-72.1")
        self.assertEqual(most_suggested['name'], 'New London')
