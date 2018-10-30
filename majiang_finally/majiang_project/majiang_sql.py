from pymysql import *

class Mysqlpython():
    """
    此类示意：创建数据库游标和服务端进行交互
    """
    def __init__(self,user='root',passwd="123456",db='Majiang',
          host="localhost",port=3306,charset="utf8"):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.host = host
        self.port = port
        self.charset = charset

    def open(self):
        """
        此方法示意：和数据库创建连接，创建游标
        """
        self.conn = connect(user=self.user,
                            passwd=self.passwd,
                            db=self.db,
                            host=self.host,
                            port=self.port,
                            charset=self.charset
                            )

        self.cursor = self.conn.cursor()

    def close(self):
        """
        此方法示意：关闭游标，关闭连接
        """
        self.cursor.close()
        self.conn.close()

    def Exec(self, sql, canshu=[]):
        """
        此方法示意：执行sql语句对数据库进行相应的操作
        """
        self.open()
        self.cursor.execute(sql, canshu)
        self.conn.commit()
        self.close()
    
    def insert(self, userName, userPwd, name):
        """
        此方法示意：对数据库进行插入记录操作
        服务端接收的注册请求在此处插入到数据库，在数据库创建用户信息
        """
        try:
            sql = 'insert into user(userName, pwd, name) values(%s, %s, %s);'
            self.Exec(sql, [userName, userPwd, name])
        except:
            return 'E'

    def select(self, userName, pwd):
        """
        此方法示意：对数据库进行查询pwd操作
        服务端要求客户端发送的登陆请求在此处进行密码对比
        """
        sql = 'select * from user where userName = %s and pwd = %s'
        self.Exec(sql, [userName, pwd])
        data = self.cursor.fetchall()
        return data

    def get_name(self, userName):
        """
        此方法示意：对数据库进行查询name操作
        客户端要求服务端发送自己的昵称给客户端
        """
        sql = 'select name from user where userName = %s'
        self.Exec(sql, [userName])
        data = self.cursor.fetchone()
        return data




# create database Majiang;
# use Majiang;
# create table user(
# id int primary key auto_increment,
# userName char(8),
# pwd char(12),
# name varchar(20),
# unique(userName),
# unique(name)
# );
