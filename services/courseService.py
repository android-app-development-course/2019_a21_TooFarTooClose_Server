from utils.mysql import *
from models.joinCourse import JoinCourse


class CourseService:
    def __init__(self):
        # 连接数据库
        self.conn = getDatabaseConnection()
        self.cursor = self.conn.cursor()

    def getCourseBasicListByUid(self, uid):
        """
            获取课程的基本信息（course_id、 course_name）
            通过用户uid获取用户加入（或创建）的课程的基本信息
        :param uid: 用户id
        :return: 返回列表res，若无课程则为空列表
                 其中元素为字典，keys如下
                 |-dict
                    |-course_id
                    |-course_name
        """
        sql = "SELECT id AS course_id, name AS course_name " \
              "FROM course " \
              "WHERE id IN (SELECT course_id FROM join_course WHERE uid=%s)"
        self.cursor.execute(sql, uid)
        res = self.cursor.fetchall()

        return res
