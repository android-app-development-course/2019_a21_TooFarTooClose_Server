from utils.mysql import *
from models.user import User


class UserService:
    def __init__(self):
        # 连接数据库
        self.conn = getDatabaseConnection()
        self.cursor = self.conn.cursor()

    def login(self, account, pwd, account_type):
        """
            用户登录
            除了核对账号密码外
            还需核对账号类型
        :param account: 用户输入的账号
        :param pwd: 用户输入的密码
        :param account_type: 用户输入的账号类型
        :return: 存在且所有参数核对无误则返回user对象，否则返回None
        """
        sql = "SELECT * FROM user WHERE account=%s AND pwd=%s AND type=%s"
        self.cursor.execute(sql, (account, pwd, account_type))
        res = self.cursor.fetchall()

        user = None
        if len(res) != 0:
            dict = res[0]  # 返回是一个列表，取第一个（也只有一个）
            user = User(id=dict["id"], open_id=dict["open_id"], account=dict["account"],
                        name=dict["name"], type=dict["type"],  phone_num=dict["phone_num"],
                        pwd=dict["pwd"],  create_timestamp=dict["create_timestamp"], status=dict["status"])

        return user
