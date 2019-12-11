from flask import request, Blueprint
import json

from services.courseService import CourseService

# 建立蓝图
course = Blueprint(name='course', import_name=__name__)


@course.route('/getCourseBasicInfo', methods=['POST'])
def getCourseBasicInfo():
    request_data = json.loads(request.form["json"])

    course_service = CourseService()
    course_obj, err = course_service.getCourseByCourseId(course_id=request_data["course_id"])
    return_data = {
        "error_code": err,
        "course_id": None,
        "create_timestamp": None
    }

    if course_obj is not None:
        return_data["course_id"] = course_obj.id
        return_data["create_timestamp"] = course_obj.create_timestamp
    print(return_data)
    return return_data


@course.route('/getCourseIntroduction', methods=['POST'])
def getCourseIntroduction():
    return_data = {
        "introduction_text": "通过本课程的学习，使学生了解软件工程的基本概念、基本原理、开发软件项目的工程化的方法和技\
        术及在开发过程中应遵循的流程、准则、标准和规范等；熟悉软件项目开发和维护的一般过程；熟练掌握软件需求分析、设计\
        、编码和测试等阶段的主要思想和技术方法，并且能够利用所学知识进行各种软件项目的实际开发实践。"
    }

    print(request.form["json"])

    return return_data


@course.route('/getCourseNotice', methods=['POST'])
def getCourseNotice():
    return_data = {
        "notice_text": "暂无公告"
    }

    print(request.form["json"])

    return return_data

