import pymysql

class DB():
    def __init__(self,database = "my01",user = "root",password = "123456",port = 3306,host = "localhost"):
        self.db = pymysql.connect(host = host,port = port, user = user, database = database, password = password,
                                  cursorclass = pymysql.cursors.DictCursor, charset='utf8mb4')
        self.cursor = self.db.cursor()

    # 为什么使用data这个元组
    #
    def update(self,sql, data):

            self.cursor.execute(sql, data)
            self.db.commit()

    def query(self,sql):

            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data

    def __del__(self):
        self.cursor.close()
        self.db.close()



if __name__ == '__main__':
    db = DB()
    # CREATE TABLE ceshi (id INT PRIMARY KEY AUTO_INCREMENT,
    # rank INT(10)
    # )DEFAULT CHARSET=utf8mb4;
    # money = 16
    # insert_sql = 'INSERT INTO ceshi(rank)VALUES(%s)'
    # data = (money)
    # db.update(insert_sql, data)

    insert_sql = 'INSERT INTO qiutan_score(`name`, `time`, city, home, address, `style`, score_date)' \
                 'VALUES (%s, %s, %s, %s, %s, %s, %s)'
    data = ('12345', '2013-08-20 03:00', '曼彻斯特城', '4-0', '纽卡斯尔联', '[[1.5, 0.75]]', "[['阻止对方创造机会^阻止對方創造機會'], ['远射防守能力^遠射防守能力']]")

    # insert_sql = 'INSERT INTO qiutan_test(rank_id, rank, `time`, host_id, score, guest_id, concede_points, dx, ban_score)' \
    #              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    # data = ('12345', 1, '2013-08-20 03:00', '曼彻斯特城', '4-0', '纽卡斯尔联', '(1.5, 0.75)', '(2.5/3, 1/1.5)', '2-0')
    db.update(insert_sql, data)
