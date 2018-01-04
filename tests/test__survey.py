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

    def test_copy_survey_success(self):
        """ Copying a survey should return array with new survey id. """
        result = self.api.survey.copy_survey(self.survey_id, "copy_test")
        # fails because result is None
        # TODO: Why is this?
        self.assertIn("newsid", result.keys())

    def test_import_survey_success_lss(self):
        """ Importing a survey should return the id of the new survey. """
        valid_files = [
            'tests/fixtures/a_rather_interesting_questionnaire_for_testing.lss',
            'tests/fixtures/an_other_questionnaire_different_fileformat.lsa',
            'tests/fixtures/same_questionnaire_different_fileformat.txt'
        ]
        new_survey_ids = []  # for deleting after test
        for file in valid_files:
            new_name = 'copy_test_%s' % file[-3:]
            result = self.api.survey.import_survey(file, new_name)
            self.assertIs(int, type(result))
            new_survey_ids.append(result)
        for new_survey_id in new_survey_ids:  # delete new surveys
            self.api.survey.delete_survey(new_survey_id)

    def test_import_survey_failure_invalid_file_extension(self):
        """ Survey with invalid file extension should raise an error. """
        invalid = 'tests/fixtures/same_questionnaire_different_fileformat.xml'
        with self.assertRaises(LimeSurveyError) as ctx:
            self.api.survey.import_survey(invalid)
        self.assertIn("Invalid extension", ctx.exception.message)

    def test_delete_survey_success(self):
        """ Deleting a Survey should return status OK. """
        s = 'tests/fixtures/a_rather_interesting_questionnaire_for_testing.lss'
        new_survey_id = self.api.survey.import_survey(s, new_name='delete_me')
        result = self.api.survey.delete_survey(new_survey_id)
        self.assertEqual("OK", result["status"])
