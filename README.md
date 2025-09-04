# HiCloud Monitoring System

Docker 컨테이너와 시스템 리소스를 실시간으로 모니터링하고 데이터베이스에 저장하는 HiCloud 팀의 클라우드 모니터링 시스템입니다.

## 시스템 개요

HiCloud Monitoring System은 3개의 주요 구성요소로 이루어져 있습니다:

1. **HiCloud Agent**: 시스템 리소스와 Docker 컨테이너 정보를 수집
2. **HiCloud Server**: Flask API로 데이터를 받아서 MySQL 데이터베이스에 저장
3. **HiCloud Database**: 수집된 모니터링 데이터를 저장

## HiCloud 프로젝트 구조

```
hi-cloud-main/
├── README.md                     # 프로젝트 가이드
├── requirements.txt              # Python 의존성 패키지
├── hicloud_config.py            # HiCloud 설정 파일
├── hicloud_database_schema.sql  # HiCloud 데이터베이스 스키마
│
├── hicloud_agent.py             # HiCloud Agent - 모니터링 데이터 수집
├── hicloud_server.py            # HiCloud Server - Flask REST API
├── hicloud_container_setup.py   # HiCloud 컨테이너 관리 도구
│
├── hicloud_database.py          # HiCloud 데이터베이스 연결
├── hicloud_docker_monitor.py    # HiCloud Docker 모니터링 도구
└── test.py                      # HiCloud 테스트 파일
```

## HiCloud 빠른 시작

### 1. 시스템 요구사항

- Python 3.8+
- Docker Engine
- MySQL 8.0+ (AWS RDS 권장)

### 2. HiCloud 의존성 설치

```bash
# HiCloud 필수 패키지 설치
pip install -r requirements.txt
```

### 3. HiCloud 데이터베이스 설정

#### MySQL 테이블 생성
```bash
# HiCloud 데이터베이스 스키마 생성
mysql -h YOUR_RDS_ENDPOINT -u admin -p < hicloud_database_schema.sql
```

#### HiCloud 설정 파일 수정
`hicloud_config.py`를 참고하여 HiCloud 시스템 설정을 수정하세요.

### 4. HiCloud 테스트 컨테이너 생성

```bash
# HiCloud 테스트용 컨테이너들을 자동 생성
python hicloud_container_setup.py setup

# HiCloud 컨테이너 상태 확인
python hicloud_container_setup.py list
```

### 5. HiCloud Server 시작

```bash
# HiCloud 모니터링 서버 실행
python hicloud_server.py
```
HiCloud Server가 `http://localhost:8000`에서 실행됩니다.

### 6. HiCloud Agent 실행

```bash
# HiCloud Agent에서 Server URL을 실제 주소로 변경 후 실행
python hicloud_agent.py
```

## HiCloud 수집 데이터

### 서버 시스템 정보
- CPU 코어 수 및 사용률
- 메모리 총량, 사용량, 사용률
- 데이터 수집 시각

### Docker 컨테이너 정보
- 컨테이너 이름 및 실행 상태
- CPU 사용률
- 메모리 사용량 및 사용률
- 데이터 수집 시각

## HiCloud 상세 설정

### HiCloud 데이터베이스 연결 설정

`hicloud_database.py` 파일에서 HiCloud 데이터베이스 정보를 수정하세요:

```python
# HiCloud AWS RDS 엔드포인트
host = "your-hicloud-db.xxxxx.ap-northeast-2.rds.amazonaws.com"
user = "hicloud_admin"
password = "hicloud_password"
name = 'hicloud_monitoring_db'
table = 'hicloud_table'
```

### HiCloud Agent 설정

`hicloud_agent.py` 파일에서 HiCloud Server URL을 수정하세요:

```python
# HiCloud Server API 엔드포인트
url = "http://your-hicloud-server-ip:8000/monitor_info"
agent_id = "agent_hicloud"
```

## HiCloud 컨테이너 관리

### HiCloud 테스트 컨테이너 생성
```bash
python hicloud_container_setup.py setup
```
생성되는 컨테이너: nginx-container, redis-container, busybox-container, alpine-container

### HiCloud 컨테이너 상태 확인
```bash
python hicloud_container_setup.py list
```

### HiCloud 테스트 컨테이너 정리
```bash
python hicloud_container_setup.py cleanup
```

## HiCloud API 사용법

### HiCloud 모니터링 데이터 전송 API

**Endpoint**: `POST /monitor_info`

**HiCloud 요청 형식**:
```json
{
    "engine_type": "docker",
    "agent_id": "agent_hicloud",
    "ser_cpu_count": 4,
    "ser_cpu_percent": 45.2,
    "ser_memory_total": 8192,
    "ser_memory_used": 4096,
    "ser_memory_percent": 50.0,
    "ser_get_datetime": "2024-09-04 15:30:00",
    "container_stats": [
        {
            "engine_type": "docker",
            "agent_id": "agent_hicloud",
            "node_name": "hicloud-agent",
            "container_name": "nginx-container",
            "status": "running",
            "con_cpu_percent": 0.5,
            "con_memory_usage": 50.2,
            "con_memory_percent": 0.6,
            "con_get_datetime": "2024-09-04 15:30:00"
        }
    ]
}
```

**HiCloud 응답 형식**:
```json
{
    "data": "",
    "pageInfo": {},
    "resultCode": "0",
    "resultMessage": "Success",
    "success": true
}
```

### HiCloud Server 상태 확인 API

**Endpoint**: `GET /health`

**응답**:
```json
{
    "status": "healthy",
    "timestamp": "2024-09-04T15:30:00.123456"
}
```

## HiCloud 데이터베이스 스키마

### HiCloud server 테이블
| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | INT (PK) | 자동 증가 ID |
| engine_type | VARCHAR(50) | 컨테이너 엔진 타입 (docker) |
| agent_id | VARCHAR(100) | HiCloud 에이전트 식별자 |
| ser_cpu_count | INT | 서버 CPU 코어 수 |
| ser_cpu_percent | DECIMAL(5,2) | 서버 CPU 사용률 (%) |
| ser_memory_total | INT | 서버 총 메모리 (MB) |
| ser_memory_used | INT | 서버 사용 메모리 (MB) |
| ser_memory_percent | DECIMAL(5,2) | 서버 메모리 사용률 (%) |
| ser_get_datetime | DATETIME | 데이터 수집 시각 |

### HiCloud container 테이블
| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | INT (PK) | 자동 증가 ID |
| engine_type | VARCHAR(50) | 컨테이너 엔진 타입 (docker) |
| agent_id | VARCHAR(100) | HiCloud 에이전트 식별자 |
| node_name | VARCHAR(100) | HiCloud 노드 이름 |
| container_name | VARCHAR(100) | Docker 컨테이너 이름 |
| status | VARCHAR(50) | 컨테이너 실행 상태 |
| con_cpu_percent | DECIMAL(5,2) | 컨테이너 CPU 사용률 (%) |
| con_memory_usage | DECIMAL(10,2) | 컨테이너 메모리 사용량 (MB) |
| con_memory_percent | DECIMAL(5,2) | 컨테이너 메모리 사용률 (%) |
| con_get_datetime | DATETIME | 데이터 수집 시각 |

## HiCloud 문제해결

### HiCloud 자주 발생하는 오류

1. **Docker 연결 오류**
   ```bash
   # Docker 소켓 권한 설정
   sudo chmod 666 /var/run/docker.sock
   
   # Docker 서비스 시작
   sudo systemctl start docker
   ```

2. **HiCloud MySQL 연결 오류**
   - AWS RDS 보안 그룹에서 3306 포트 인바운드 규칙 허용
   - HiCloud 데이터베이스 사용자 권한 확인
   - HiCloud RDS 엔드포인트 주소 확인

3. **HiCloud 컨테이너 통계 수집 오류**
   - Docker 컨테이너가 실제로 실행 중인지 확인
   - Docker API 버전 호환성 확인
   - 컨테이너 리소스 제한 설정 확인

### HiCloud 로그 확인

HiCloud Server 실행 시 실시간 로그:
```bash
python hicloud_server.py
# [2024-09-04 15:30:00] HiCloud received data: MonitorInfo(...)
```

## HiCloud 프로덕션 배포

### 1. HiCloud 환경변수 설정
```bash
export HICLOUD_CONFIG=/path/to/hicloud-config.py
export HICLOUD_HOME=/opt/hicloud-monitor
```

### 2. HiCloud 시스템 서비스 등록 (systemd)
```ini
[Unit]
Description=HiCloud Monitor Server
After=network.target

[Service]
Type=simple
User=hicloud
WorkingDirectory=/opt/hicloud-monitor
ExecStart=/usr/bin/python3 hicloud_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. HiCloud Agent 자동 실행 (cron)
```bash
# HiCloud Agent 매분마다 실행
* * * * * /usr/bin/python3 /opt/hicloud-monitor/hicloud_agent.py
```

## HiCloud 모니터링 대시보드

HiCloud 수집 데이터 시각화 방법:

1. **Grafana** + HiCloud MySQL 데이터소스
2. **Prometheus** + HiCloud custom exporter
3. **HiCloud 웹 대시보드** 직접 개발