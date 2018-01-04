from tests.test_limesurvey import TestBase
from limesurveyrc2api.limesurvey import LimeSurveyError


class TestSurveys(TestBase):

    def test_list_surveys_success(self):
        """A valid request for list of surveys should not return empty."""
        result = self.api.survey.list_surveys()
        for survey in result:
            self.assertIsNotNone(survey.get('sid'))

    def test_list_surveys_failure(self):
        """An invalid request for list of surveys should raise an error."""
        with self.assertRaises(LimeSurveyError) as ctx:
            self.api.survey.list_surveys(username="not_a_user")
        self.assertIn("Invalid user", ctx.exception.message)

    def test_list_questions_success(self):
        """Listing questions for a survey should return a question list."""
        result = self.api.survey.list_questions(survey_id=self.survey_id)
        for question in result:
            self.assertEqual(self.survey_id, question["sid"])
            self.assertIsNotNone(question["gid"])
            self.assertIsNotNone(question["qid"])

    def test_list_questions_failure(self):
        """Listing questions for an invalid survey should returns an error."""
        with self.assertRaises(LimeSurveyError) as ctx:
            self.api.survey.list_questions(self.survey_id_invalid)
        self.assertIn("Error: Invalid survey ID", ctx.exception.message)

    def test_get_survey_properties_success_with_survey_settings(self):
        """ Should return array with specified properties for given survey. """
        survey_settings = ['active', 'expires', 'sid']
        result = self.api.survey.get_survey_properties(self.survey_id,
                                                       survey_settings)
        self.assertEqual(len(result), 3)
        for property in survey_settings:
            self.assertIn(property, result.keys())
        self.assertIs(type(result["active"]), str)
        self.assertIs(type(result["sid"]), str)  # TODO: might be int later

    def test_get_survey_properties_success_without_survey_settings(self):
        """ If no settings are specified all should be returned. """
        # TODO: raises 'No valid Data'
        result = self.api.survey.get_survey_properties(self.survey_id)
        self.assertGreater(len(result), 5)  # TODO: ask for exact number?

