import docker
from time import strftime, localtime
import json, time
import psutil
import requests
from collections import OrderedDict

# HiCloud Monitoring Agent Configuration
engine_type = "docker"
agent_id = "agent_hicloud"

def get_server_stats(dt):
    """서버의 시스템 리소스 정보를 수집하는 함수"""
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    mem_info = psutil.virtual_memory()
    memory_total = round(mem_info.total/1024/1024, 0)
    available_memory = round(mem_info.available/1024/1024, 0)
    memory_used = memory_total - available_memory
    memory_percent = round(memory_used/memory_total*100, 2)

    _dict = {}
    _dict['engine_type'] = engine_type
    _dict['agent_id'] = agent_id
    _dict['ser_cpu_count'] = cpu_count
    _dict['ser_cpu_percent'] = cpu_percent
    _dict['ser_memory_total'] = memory_total
    _dict['ser_memory_used'] = memory_used
    _dict['ser_memory_percent'] = memory_percent
    _dict['ser_get_datetime'] = dt
    print(_dict)
    return _dict


def get_container_stats(dt):
    """Docker 컨테이너의 상태 및 리소스 정보를 수집하는 함수"""
    client = docker.from_env()
    _list = []
    
    for container in client.containers.list(all=True):
        _dict = {}
        _dict['engine_type'] = "docker"
        _dict['agent_id'] = "agent_hicloud"
        _dict['node_name'] = "hicloud-agent"
        _dict['container_name'] = container.name
        _dict['status'] = container.status
        _dict['con_get_datetime'] = dt

        if container.status == "running":
            try:
                stats = container.stats(stream=False)
                
                # CPU 사용률 계산
                total_usage = stats['cpu_stats']['cpu_usage']['total_usage']
                prev_total_usage = stats['precpu_stats']['cpu_usage']['total_usage']
                system_cpu_usage = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
                cpu_usage = total_usage - prev_total_usage
                
                if system_cpu_usage > 0:
                    cpu_percentage = (cpu_usage / system_cpu_usage) * 100
                else:
                    cpu_percentage = 0

                # 메모리 사용률 계산
                memory_usage = stats['memory_stats']['usage']
                memory_limit = stats['memory_stats']['limit']
                memory_percentage = (memory_usage / memory_limit) * 100

                _dict['con_cpu_percent'] = round(cpu_percentage, 2)
                _dict['con_memory_usage'] = round(memory_usage/1024/1024, 2)
                _dict['con_memory_percent'] = round(memory_percentage, 2)
                
            except Exception as e:
                print(f"Error getting stats for {container.name}: {e}")
                _dict['con_cpu_percent'] = 0
                _dict['con_memory_usage'] = 0
                _dict['con_memory_percent'] = 0
        else:
            _dict['con_cpu_percent'] = 0
            _dict['con_memory_usage'] = 0
            _dict['con_memory_percent'] = 0
            
        print(_dict)
        _list.append(_dict)

    client.close()
    return _list


if __name__ == '__main__':
    # 현재 시간 정보 생성
    now = time.time()
    tm = localtime(now)
    dt = strftime('%Y-%m-%d %I:%M:%S', tm)

    # 서버 및 컨테이너 통계 수집
    server_stats = get_server_stats(dt)
    container_stats = get_container_stats(dt)

    # JSON 데이터 구성
    body = OrderedDict()
    body = server_stats
    body['container_stats'] = container_stats
    data = json.dumps(body, ensure_ascii=False, indent="\t")
    print(data)

    # 서버로 데이터 전송 (실제 사용시 URL과 포트를 변경하세요)
    url = "http://YOUR_SERVER_IP:YOUR_PORT/monitor_info"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print(f"Failed to send data to server: {e}")