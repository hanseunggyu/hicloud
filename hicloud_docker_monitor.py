import docker

# Docker 클라이언트 생성
client = docker.from_env()

# 실행 중인 모든 컨테이너 목록 가져오기
containers = client.containers.list(all=True)

print("Docker Container Monitoring System:")
for container in containers:
    print(f"ID: {container.id}, Name: {container.name}, Status: {container.status}")

    # 컨테이너의 실시간 통계 정보 가져오기
    stats = container.stats(stream=False)

    print("System Stats:")
    print(f"CPU Usage: {stats['cpu_stats']['cpu_usage']['total_usage']}")
    print(f"Memory Usage: {stats['memory_stats']['usage']}")
    
    # 네트워크 인터페이스가 존재하는 경우에만 출력
    if 'networks' in stats and stats['networks']:
        network_key = list(stats['networks'].keys())[0]  # 첫 번째 네트워크 인터페이스 사용
        rx_bytes = stats['networks'][network_key]['rx_bytes']
        tx_bytes = stats['networks'][network_key]['tx_bytes']
        print(f"Network IO: {rx_bytes} RX, {tx_bytes} TX")
    else:
        print("Network IO: No network interface found")
    
    print("="*50)

# Docker 클라이언트 종료
client.close()