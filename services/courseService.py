import time

from utils.mysql import *
from static.edu import *
from models.course import Course
from models.courseResource import CourseResource


class CourseService:
    def __init__(self):
        # 连接数据库
        self.conn = getDatabaseConnection()
        self.cursor = self.conn.cursor()

    def getCourseByCourseId(self, course_id):
        """
            获取课程模型
        :param course_id: 课程id
        :return: 存在返回course对象，否则返回None
        """
        sql = "SELECT * FROM course WHERE id=%s"
        self.cursor.execute(sql, course_id)
        res = self.cursor.fetchall()

        course = None
        err = ErrorCode.NoError
        if len(res) == 0:
            err = ErrorCode.ResourceNotFoundError
        else:
            dict = res[0]  # 返回是一个列表，取第一个（也只有一个）
            course = Course(id=str(dict["id"]), name=dict["name"], key=dict["key"],
                            creator_id=str(dict["creator_id"]), create_timestamp=dict["create_timestamp"],
                            status=dict["status"], notice=dict["notice"], introduction=dict["introduction"],
                            joinable=dict["joinable"])
        return course, err

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
        sql = "SELECT CAST(id AS CHAR) AS course_id, name AS course_name " \
              "FROM course " \
              "WHERE id IN (SELECT course_id FROM join_course WHERE uid=%s)"
        self.cursor.execute(sql, uid)
        res = self.cursor.fetchall()

        return res

    def insertCourseResourceRecord(self, course_id, title, filename, uploader_id, path, size):
        """
            插入一条课程资源记录
            注意course_resource表有course_id与tile的唯一性约束
        :param course_id: 课程id
        :param title: 资源标题
        :param filename: 文件名
        :param uploader_id: 上传者id
        :param path: 相对存储路径
        :param size: 文件大小
        :return: 插入成功返回course_resource对象，否则返回None
        """
        type = filename[filename.rfind(".")+1:]
        upload_timestamp = int(time.time())

        course_resource = None
        err = ErrorCode.NoError
        try:
            sql = "INSERT INTO " \
                  "course_resource (course_id, title, filename, type, upload_timestamp, uploader_id, path, size) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (course_id, title, filename, type, upload_timestamp, uploader_id, path, size))

            sql = "SELECT * FROM course_resource WHERE course_id=%s AND title=%s"
            self.cursor.execute(sql, (course_id, title))
            res = self.cursor.fetchall()
            dict = res[0]
            course_resource = CourseResource(id=str(dict["id"]), course_id=dict["course_id"], title=dict["title"],
                                             filename=dict["filename"], type=dict["type"],
                                             upload_timestamp=dict["upload_timestamp"], uploader_id=dict["uploader_id"],
                                             path=dict["path"])
        except pymysql.err.IntegrityError:  # 完整性约束，course_id与tile的唯一性约束
            err = ErrorCode.ResourceTitleDuplicateError

        return course_resource, err

    def deleteCourseResourceRecordByFileId(self, file_id):
        """
            移除某一课程资源
            仅移除数据库中的记录
        :param file_id: 需要删除的文件（或资源）id
        :return:
        """
        sql = "SELECT * FROM course_resource WHERE id=%s"
        self.cursor.execute(sql, file_id)
        res = self.cursor.fetchall()

        course_resource = None
        err = ErrorCode.NoError
        if len(res) == 0:
            err = ErrorCode.ResourceNotFoundError
        else:
            dict = res[0]
            course_resource = CourseResource(id=str(dict["id"]), course_id=dict["course_id"], title=dict["title"],
                                             filename=dict["filename"], type=dict["type"],
                                             upload_timestamp=dict["upload_timestamp"], uploader_id=dict["uploader_id"],
                                             path=dict["path"])

            sql = "DELETE FROM course_resource WHERE id=%s"
            self.cursor.execute(sql, file_id)

        return course_resource, err

    def getCourseResourceListByCourseId(self, course_id):
        """
            获取课程资源列表（course_id、 course_name）
            通过course_idd获取获取课程资源列表
        :param course_id: 课程id
        :return: 返回列表res，若无资源则为空列表
                 其中元素为字典，keys如下
                 |-dict
                    |-file_id
                    |-resource_title
                    |-filename
                    |-upload_timestamp
                    |-uploader
                    |-file_size
        """
        err = ErrorCode.NoError
        sql = "SELECT " \
              "CAST(course_resource.id AS CHAR) AS file_id, " \
              "title AS resource_title, filename, upload_timestamp, " \
              "name AS uploader, size AS file_size " \
              "FROM course_resource " \
              "LEFT JOIN user ON uploader_id=user.id " \
              "WHERE course_id=%s " \
              "ORDER BY upload_timestamp DESC"
        self.cursor.execute(sql, course_id)
        res = self.cursor.fetchall()

        return res, err
