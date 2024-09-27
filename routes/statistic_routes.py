from flask import Blueprint, request
from controllers.statisc_controller import *
from db.bd_mysql import db_connection

statistic_app = Blueprint("statistic_app", __name__)


@statistic_app.route('/api/statistic', methods=['POST'])
def create_statistic_routes():
    connection = db_connection()
    data = request.json
    response = create_statistc_controller(connection, data)
    return response

@statistic_app.route('/api/activity/<id_student>', methods=['GET'])
def get_activity_statistics_routes(id_student):
    connection = db_connection()

    id_activity = request.args.get('id_activity')

    response = group_answer_by_id_student_controller(connection,id_student,id_activity)
    return response, 200

@statistic_app.route('/api/activity/all', methods=['GET'])
def get_all_statistics_routes():
    connection = db_connection()

    id_activity = request.args.get('id_activity')

    response = get_all_statistics_by_activity(connection,id_activity)
    return response, 200