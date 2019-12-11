from flask import request, Blueprint
import json
import time
import os

from config.conf import *
from services.courseService import CourseService

# 建立蓝图
course = Blueprint(name='course', import_name=__name__)


@course.route('/getCourseBaseInfo', methods=['POST'])
def getCourseBaseInfo():
    return_data = {
        "course_id": json.loads(request.form["json"])["course_id"],
        "create_timestamp": int(time.time())
    }

    print(json.loads(request.form["json"]))
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


@course.route('/getCourseResourceList', methods=['POST'])
def getCourseResourceList():
    request_data = json.loads(request.form["json"])

    course_service = CourseService()
    res, err = course_service.getCourseResourceListByCourseId(course_id=request_data["course_id"])
    return_data = {
        "error_code": err,
        "file_info_list": res
    }

    return return_data


@course.route('/uploadCourseResource', methods=['POST'])
def uploadCourseResource():
    request_data = json.loads(request.form["json"])
    request_file = request.files["file"]

    # 存储的相对路径
    relative_path = request_data["course_id"] + "/" + request_data["resource_title"]
    absolute_path = COURSE_RESOURCE_PATH + "/" + relative_path
    # 检测路径是否存在，不存在则创建
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    file_relative_path = relative_path + "/" + request_data["filename"]
    file_absolute_path = COURSE_RESOURCE_PATH + "/" + file_relative_path
    request_file.save(file_absolute_path)

    course_service = CourseService()
    res, err = course_service.insertCourseResourceRecord(course_id=request_data["course_id"],
                                                         title=request_data["resource_title"],
                                                         filename=request_data["filename"],
                                                         uploader_id=request_data["uid"],
                                                         path=file_relative_path,
                                                         size=request_data["file_size"])

    return_data = {
        "error_code": err
    }

    return return_data
