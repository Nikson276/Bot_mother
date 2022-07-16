import sqlite3
import datetime


now = datetime.datetime.now()

str_now = now.strftime('%H:%M:%S')

try:
    conn = sqlite3.connect("sleepcounter.db")
    cursor = conn.cursor()
    act_type = 'rise'
    user_id = '3'

    # создаем пользователя с user_id = 1000
    #cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (1000,))

    # Считываем всех юзеров
    # users = cursor.execute("SELECT * FROM 'users'")
    # print(users.fetchall())
    # AND     ORDER BY `act_datetime`
    db_query_time = """
    SELECT `act_datetime` 
    FROM `records` 
    WHERE `id` = (SELECT MAX(id) FROM `records` 
                    WHERE `act_datetime` BETWEEN datetime('now', '-1 day', 'start of day') AND datetime('now', 'localtime') 
                    AND `user_id` = ? 
                    AND `act_type` <> ?);
    """
   
    # start_time_db = cursor.execute("SELECT `act_datetime` FROM `records` WHERE `id` = (SELECT MAX(id) FROM `records` WHERE `act_datetime` BETWEEN datetime('now', '-1 day', 'start of day') AND datetime('now', 'localtime') AND `act_type` <> ?)",
    #                             (act_type,))   
    # datetime_now_start = cursor.execute("SELECT datetime('now', 'start of day')")
    # max_id = cursor.execute("SELECT MAX(id) FROM `records` WHERE `user_id` = '3' AND `act_type` <> 'rise' AND `act_datetime` BETWEEN datetime('now', '-1 day', 'start of day') AND datetime('now', 'localtime')")
    # # datetime_now_local = cursor.execute("SELECT datetime('now', 'localtime')")
    # #datetime_now_start = 0#cursor.execute("SELECT datetime('now')")
    # #datetime_now_local = cursor.execute("SELECT datetime('now', 'localtime')")
    # #print('Начало дня', datetime_now_start.fetchall())
    # #print('Текущее время', datetime_now_local.fetchall())
    # print('максИД', max_id.fetchall())
    
    start_time_db = cursor.execute(db_query_time,(user_id, act_type,)) 
    print(start_time_db) 
    start_time_fetch = start_time_db.fetchall() 
    print(start_time_fetch)
    #checks
    if len(start_time_fetch):
        pass
    else:
        print("ERROR")
        
        
    date_time_str = str(start_time_fetch)[3:22]
    print(date_time_str)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    
    
    
    start_time = date_time_obj.time().strftime('%H:%M:%S')
    print('Это время старта для рассчета', start_time)
 
    end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print('Время текущее для расчета', end_time)
    
    total_time=(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(start_time,'%H:%M:%S'))
    print('Разница', total_time)
    print('ТИП', type(total_time))
    duration = str(total_time)
    print('Разница', duration)
    print('ТИП', type(duration))
    
    
    # COMMIT 
    #conn.commit()

except sqlite3.Error as error:
    print("Error", error)

finally:
    if(conn):
        conn.close()
