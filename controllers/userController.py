from flask import request, Blueprint
import json

from static.edu import *
from services.userService import UserService
from services.courseService import CourseService

# 建立蓝图
user = Blueprint(name='user', import_name=__name__)


@user.route('/loginPC', methods=['POST'])
def loginPC():
    request_data = json.loads(request.form["json"])

    user_service = UserService()
    user_obj = user_service.login(account=request_data["account"],
                                  pwd=request_data["pwd"],
                                  account_type=request_data["account_type"])

    course_service = CourseService()
    course_list = course_service.getCourseBasicListByUid(uid=user_obj.id)

    return_data = {
        "user_pic": "NULL",
        "uid": user_obj.id,
        "username": user_obj.name,
        "account_type": user_obj.type,
        "course_list": course_list,
        "user_status": user_obj.status
    }

    return return_data
