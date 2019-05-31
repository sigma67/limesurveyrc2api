from collections import OrderedDict

class _Survey(object):

    def __init__(self, api):
        self.api = api

    def get_question_properties(self, question_id):
        """ Return the ids and all attributes of groups belonging to survey.

        Parameters
        :param survey_id: ID of the question.
        :rtype survey_id: Integer
        """
        method = "get_question_properties"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", question_id)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        assert response_type is list
        return response