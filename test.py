import docker

# Docker 클라이언트 생성
client = docker.from_env()

# 실행 중인 모든 컨테이너 목록 가져오기
containers = client.containers.list(all=True)

print("Docker Containers:")
for container in containers:
    print(f"ID: {container.id}, Name: {container.name}, Status: {container.status}")

    # 컨테이너의 실시간 통계 정보 가져오기
    stats = container.stats(stream=False)

    print("Stats:")
    print(f"CPU Usage: {stats['cpu_stats']['cpu_usage']['total_usage']}")
    print(f"Memory Usage: {stats['memory_stats']['usage']}")
    print(f"Network IO: {stats['networks']['eth0']['rx_bytes']} RX, {stats['networks']['eth0']['tx_bytes']} TX")
    print("="*40)

# Docker 클라이언트 종료
client.close()