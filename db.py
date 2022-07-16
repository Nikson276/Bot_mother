from asyncio.windows_events import NULL
import sqlite3
from xmlrpc.client import DateTime
import datetime

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()


    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def calc_duration(self, user_id, act_type):
        """Расчет временной продолжительности"""
        #запрос к БД за последней записью о действии <> текущему act_type
        db_query_time = """
            SELECT `act_datetime` 
            FROM `records` 
            WHERE `id` = (SELECT MAX(id) FROM `records` 
                            WHERE `act_datetime` BETWEEN datetime('now', '-1 day', 'start of day') AND datetime('now', 'localtime') 
                            AND `user_id` = ? 
                            AND `act_type` <> ?);
            """       
        start_time_db = self.cursor.execute(db_query_time, (user_id, act_type,))
        start_time_fetch = start_time_db.fetchall()
        if len(start_time_fetch):
            date_time_str = str(start_time_fetch)[3:22]
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S') #преобразовываем в объект datetime
            start_time = date_time_obj.time().strftime('%H:%M:%S')    # берем только время
            end_time = datetime.datetime.now().time().strftime('%H:%M:%S') #форматируем 
            duration = str(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(start_time,'%H:%M:%S')) #расчитываем продолжительность
        else:
            duration = 0
        return duration

    def add_record(self, user_id, act_type):
        """Создаем запись о сне\пробуждении
        Где: act_type = rise - проснулся \ fall - уснул
        """
        #count duration 
        duration = BotDB.calc_duration(self, self.get_user_id(user_id), act_type)
        
        self.cursor.execute("INSERT INTO `records` (`user_id`, `act_type`, duration) VALUES (?, ?, ?)",
            (self.get_user_id(user_id),
            act_type, duration),)
        return self.conn.commit()

    def get_records(self, user_id, within = "all"):
        """Получаем историю о сне\пробуждении"""
        #это все лучше потом вынесты в отдельный модуль (файл)
        db_query_day = """
        SELECT * FROM `records` 
        WHERE `user_id` = ? 
        AND `act_datetime` BETWEEN datetime('now', 'start of day') 
        AND datetime('now', 'localtime') 
        ORDER BY `act_datetime`
        """
        db_query_week = """
        SELECT * FROM `records` 
        WHERE `user_id` = ? 
        AND `act_datetime` BETWEEN datetime('now', '-6 days') 
        AND datetime('now', 'localtime') 
        ORDER BY `act_datetime`
        """
        db_query_month = """
        SELECT * FROM `records` 
        WHERE `user_id` = ? 
        AND `act_datetime` BETWEEN datetime('now', 'start of month') 
        AND datetime('now', 'localtime') 
        ORDER BY `act_datetime`
        """
        
        if(within == "day"):
            result = self.cursor.execute(db_query_day,
                (self.get_user_id(user_id),))
        elif(within == "week"):
            result = self.cursor.execute(db_query_week,
                (self.get_user_id(user_id),))
        elif(within == "month"):
            result = self.cursor.execute(db_query_month,
                (self.get_user_id(user_id),))
        else:
            result = self.cursor.execute("SELECT * FROM `records` WHERE `user_id` = ? ORDER BY `act_datetime`",
                (self.get_user_id(user_id),))

        return result.fetchall()
        


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()