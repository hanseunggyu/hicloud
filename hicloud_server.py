from flask import Flask, request, jsonify
import os
import sys
import datetime
import pandas as pd
from typing import List, Union
from pydantic import BaseModel
# from common import ConfigManager, MySQLWrapper, CommonUtil

app = Flask(__name__)

# HiCloud Monitoring Server
# Note: 실제 사용시 common 모듈을 구현하거나 직접 MySQL 연결 코드를 작성하세요
# config_manager = None
# logger = None
# commonUtil = CommonUtil.CommonUtil()

class ContainerStats(BaseModel):
    """컨테이너 통계 정보 모델"""
    engine_type: str
    agent_id: str
    node_name: str
    container_name: str
    status: str
    con_cpu_percent: float
    con_memory_usage: float
    con_memory_percent: float
    con_get_datetime: str

class MonitorInfo(BaseModel):
    """모니터링 정보 모델"""
    engine_type: str
    agent_id: str
    ser_cpu_count: int
    ser_cpu_percent: float
    ser_memory_total: int
    ser_memory_used: int
    ser_memory_percent: float
    ser_get_datetime: str
    container_stats: Union[List[ContainerStats], None] = None

def setup():
    """서버 초기 설정 (실제 사용시 구현 필요)"""
    # global config_manager, logger
    # config_manager = ConfigManager.ConfigManager()
    # config_file = os.getenv('SERVER_CONFIG', './config/config.xml')
    # config_manager.load_config(config_file)
    # logger = config_manager.get_logger()
    print("Server setup completed")

@app.route('/monitor_info', methods=['POST'])
def post_monitor_info():
    """모니터링 정보를 받아 데이터베이스에 저장하는 API"""
    try:
        myfunc = sys._getframe().f_code.co_name
        
        # 실제 사용시 주석 해제
        # if not config_manager or not logger:
        #     setup()

        # JSON 데이터 파싱
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "resultCode": "400",
                "resultMessage": "No JSON data provided",
                "data": ""
            }), 400
            
        monitorInfo = MonitorInfo(**data)

        # 로깅 (실제 사용시 주석 해제)
        # logger.info(f"[{myfunc}] called api. item:{monitorInfo}")
        print(f"[{myfunc}] received data: {monitorInfo}")

        # 서버 정보 딕셔너리 구성
        server_dict = {
            'engine_type': monitorInfo.engine_type,
            'agent_id': monitorInfo.agent_id,
            'ser_cpu_count': monitorInfo.ser_cpu_count,
            'ser_cpu_percent': monitorInfo.ser_cpu_percent,
            'ser_memory_total': monitorInfo.ser_memory_total,
            'ser_memory_used': monitorInfo.ser_memory_used,
            'ser_memory_percent': monitorInfo.ser_memory_percent,
            'ser_get_datetime': monitorInfo.ser_get_datetime,
        }

        # 컨테이너 정보 리스트 구성
        container_list = []
        if monitorInfo.container_stats:
            for container in monitorInfo.container_stats:
                con_dict = {
                    'engine_type': str(container.engine_type),
                    'agent_id': str(container.agent_id),
                    'node_name': str(container.node_name),
                    'container_name': str(container.container_name),
                    'status': str(container.status),
                    'con_cpu_percent': container.con_cpu_percent,
                    'con_memory_usage': container.con_memory_usage,
                    'con_memory_percent': container.con_memory_percent,
                    'con_get_datetime': str(container.con_get_datetime),
                }
                container_list.append(con_dict)

        # 데이터베이스 저장 (실제 사용시 주석 해제하고 MySQL 연결 정보 설정)
        # mysql_wrapper = MySQLWrapper.MySQLWrapper()
        # mysql_wrapper.set_logger(config_manager.get_logger())
        # mysql_wrapper.db_connect(config_manager.get_db_connection_info())
        
        # # 서버 데이터 저장
        # df_server = pd.json_normalize(server_dict)
        # mysql_wrapper.db_insert(df_server, 'server', "insertonly")
        
        # # 컨테이너 데이터 저장
        # df_container = pd.json_normalize(container_list)
        # mysql_wrapper.db_insert(df_container, 'container', "insertonly")
        
        # mysql_wrapper.db_commit()
        # mysql_wrapper.db_close()

        # 임시로 콘솔에 출력
        print("Server Data:", server_dict)
        print("Container Data:", container_list)

        # 성공 응답
        json_data = {
            "data": "",
            "pageInfo": {},
            "resultCode": "0",
            "resultMessage": "Success",
            "success": True
        }
        return jsonify(json_data)

    except Exception as err:
        # 에러 응답
        json_data = {
            "data": "",
            "pageInfo": {},
            "resultCode": "99",
            "resultMessage": str(err),
            "success": False
        }
        print(f"[{myfunc}] Exception err:{str(err)}")
        
        # 실제 사용시 주석 해제
        # if 'mysql_wrapper' in locals():
        #     mysql_wrapper.db_close()
            
        return jsonify(json_data), 500

@app.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인 API"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    # 환경변수 설정
    os.environ.setdefault('SERVER_HOME', '/')

    try:
        setup()
        
        server_home = os.getenv('SERVER_HOME')
        now = datetime.datetime.now()
        
        if server_home is None:
            print(f"{now} ENV SERVER_HOME not found")
            raise Exception("SERVER_HOME not found")

        # 실제 사용시 config 파일에서 IP와 포트를 읽어오도록 수정
        # config_file = os.getenv('SERVER_CONFIG', './config/config.xml')
        # config_manager = ConfigManager.ConfigManager()
        # config_manager.load_config(config_file)
        # config_server = config_manager.get_server_info()
        # app.run(host=config_server.ip, port=config_server.port, debug=True)
        
        # 임시로 기본값 사용
        host = '0.0.0.0'  # 모든 인터페이스에서 접근 가능
        port = 8000       # 포트 번호
        
        print(f"{now} Starting server on {host}:{port}")
        app.run(host=host, port=port, debug=True)

    except Exception as err:
        now = datetime.datetime.now()
        print(f"{now} process terminated with exception: {err}")
        raise SystemExit(-1)