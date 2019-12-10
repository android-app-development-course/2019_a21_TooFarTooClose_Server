from flask import request, Blueprint
import json
import time

from utils.mysql import *


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

    db = getDatabaseConnection()
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql = "CREATE TABLE EMPLOYEE (FIRST_NAME  CHAR(20) NOT NULL,LAST_NAME  CHAR(20),AGE INT,SEX CHAR(1),INCOME FLOAT )"
    cursor.execute(sql)

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
    return_data = {
        "file_info_list": [
            {"file_id": "1001", "filename": "语文.pdf", "upload_timestamp": 1575301104, "uploader": "教师",
             "file_size": 213123},
            {"file_id": "1001", "filename": "专业.ppt", "upload_timestamp": 1575301104, "uploader": "教师",
             "file_size": 213123},
            {"file_id": "1001", "filename": "撒旦撒.docx", "upload_timestamp": 1575301104, "uploader": "教师",
             "file_size": 213123},
            {"file_id": "1001", "filename": "阿松大沙发沙发.doc", "upload_timestamp": 1575301104, "uploader": "教师",
             "file_size": 213123},
            {"file_id": "1001", "filename": "啊发撒法沙发沙发.jpg", "upload_timestamp": 1575301104, "uploader": "教师",
             "file_size": 213123},
            {"file_id": "1001", "filename": "pycharm.exe", "upload_timestamp": 1575301104, "uploader": "教师",
             "file_size": 213123}
        ]
    }

    print(request.form["json"])

    return return_data


@course.route('/uploadCourseResource', methods=['POST'])
def uploadCourseResource():
    return_data = {
        "upload_status": ""
    }

    print(request.form["json"])
    request.files["file"].save(request.files["file"].filename)

    return return_data
