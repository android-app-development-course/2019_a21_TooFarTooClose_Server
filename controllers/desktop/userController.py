from flask import request, Blueprint
import json

from services.userService import UserService
from services.courseService import CourseService

# 建立蓝图
user = Blueprint(name='user', import_name=__name__)


@user.route('/loginPC', methods=['POST'])
def loginPC():
    request_data = json.loads(request.form["json"])

    user_service = UserService()
    user_obj, err = user_service.loginPC(account=request_data["account"],
                                         pwd=request_data["pwd"],
                                         account_type=request_data["account_type"])

    return_data = {
        "error_code": err,
        "user_pic": None,
        "uid": None,
        "username": None,
        "account_type": None,
        "course_list": None,
        "user_status": None
    }
    if user_obj is not None:
        course_service = CourseService()
        course_list = course_service.getCourseBasicListByUid(uid=user_obj.id)

        return_data["user_pic"] = "NULL"
        return_data["uid"] = user_obj.id
        return_data["username"] = user_obj.name
        return_data["account_type"] = user_obj.type
        return_data["course_list"] = course_list
        return_data["user_status"] = user_obj.status
    print(return_data)
    return return_data
