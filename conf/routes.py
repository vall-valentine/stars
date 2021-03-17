from flask_restful import Api

from resources.resurces import UsersResource, UsersListResource, RolesResource, RolesListResource, GroupsResource, \
    GroupsListResource, TeacherGroupsResource, TeacherGroupsListResource, GroupStudentsResource, \
    GroupStudentsListResource, TestResource, TestListResource, QuestionsResource, QuestionsListResource, \
    TestQuestionsResource, TestQuestionsListResource, TestResultsResource, TestResultsListResource
from resources.error_handler import page_not_found


def generate_routes(app):
    app.register_error_handler(404, page_not_found)
    api = Api(app)

    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')

    api.add_resource(RolesListResource, '/api/roles')
    api.add_resource(RolesResource, '/api/roles/<int:role_id>')

    api.add_resource(GroupsListResource, '/api/groups')
    api.add_resource(GroupsResource, '/api/groups/<int:group_id>')

    api.add_resource(TeacherGroupsListResource, '/api/teachergroups')
    api.add_resource(TeacherGroupsResource, '/api/teachergroups/<int:tg_id>')

    api.add_resource(GroupStudentsListResource, '/api/groupstudents')
    api.add_resource(GroupStudentsResource, '/api/groupstudents/<int:gs_id>')

    api.add_resource(TestListResource, '/api/test')
    api.add_resource(TestResource, '/api/users/<int:test_id>')

    api.add_resource(QuestionsListResource, '/api/questions')
    api.add_resource(QuestionsResource, '/api/questions/<int:question_id>')

    api.add_resource(TestQuestionsListResource, '/api/testquestions')
    api.add_resource(TestQuestionsResource, '/api/testquestions/<int:tq_id>')

    api.add_resource(TestResultsListResource, '/api/testresults')
    api.add_resource(TestResultsResource, '/api/testresults/<int:tr_id>')