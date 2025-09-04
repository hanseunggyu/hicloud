# HiCloud Monitoring System Configuration Example
# 실제 시스템 구성을 참고하여 작성

class DatabaseConfig:
    """데이터베이스 설정"""
    # AWS RDS 설정 (실제 값으로 변경 필요)
    HOST = "YOUR_RDS_ENDPOINT"  # 예: your-db.xxxxx.ap-northeast-2.rds.amazonaws.com
    USER = "admin"              # RDS 마스터 사용자명
    PASSWORD = "YOUR_PASSWORD"  # RDS 마스터 비밀번호  
    DATABASE = "monitoring_db"  # 데이터베이스명
    PORT = 3306                 # MySQL 기본 포트

class ServerConfig:
    """서버 설정"""
    HOST = "0.0.0.0"           # 모든 인터페이스에서 접근 허용
    PORT = 8000                # Flask 서버 포트
    DEBUG = True               # 개발 모드

class AgentConfig:
    """에이전트 설정"""  
    AGENT_ID = "agent_hicloud"   # 에이전트 식별자
    NODE_NAME = "hicloud-agent"  # 노드 이름
    ENGINE_TYPE = "docker"     # 컨테이너 엔진 타입
    
    # 서버 API 엔드포인트
    SERVER_URL = "http://YOUR_SERVER_IP:8000/monitor_info"
    
    # 데이터 수집 간격 (초)
    COLLECTION_INTERVAL = 60

class APIResponse:
    """API 응답 형식 (August.md 참조)"""
    @staticmethod
    def success_response():
        return {
            "data": "",
            "pageInfo": {},
            "resultCode": "0",
            "resultMessage": "",
            "success": True
        }
    
    @staticmethod
    def error_response(error_message):
        return {
            "data": "",
            "pageInfo": {},
            "resultCode": "99", 
            "resultMessage": error_message,
            "success": False
        }