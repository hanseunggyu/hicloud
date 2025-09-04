import pymysql

# HiCloud Monitoring System - Database Connection

# AWS RDS 엔드포인트를 여기에 입력 
# 예: your-db.xxxxx.ap-northeast-2.rds.amazonaws.com (서울 리전)
# 예: your-db.xxxxx.ap-southeast-2.rds.amazonaws.com (시드니 리전)  
host = "YOUR_RDS_ENDPOINT"
# 데이터베이스 사용자명
user = "YOUR_DB_USERNAME"
# 데이터베이스 비밀번호
password = "YOUR_DB_PASSWORD"
# 사용할 데이터베이스명
name = 'YOUR_DATABASE_NAME'
# 테이블명
table = 'YOUR_TABLE_NAME'

connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    db = name
)

try:
    with connection.cursor() as cursor:
        # 삽입할 데이터 (id, name, email 형식)
        insert_data = [
            ('SAMPLE_ID', 'SAMPLE_NAME', 'sample@email.com')
        ]
        
        sql = f"INSERT INTO {table} (id, name, email) VALUES (%s, %s, %s)"
        
        cursor.executemany(sql, insert_data)
        
        connection.commit()
        
        print("데이터 추가 완료")
        
finally:
    connection.close()