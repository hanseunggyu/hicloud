import docker
import time

def setup_test_containers():
    """테스트용 컨테이너들을 생성하고 실행하는 함수"""
    
    client = docker.from_env()
    
    containers_to_create = [
        {
            "image": "nginx",
            "name": "nginx-container",
            "command": None,
            "detach": True
        },
        {
            "image": "busybox", 
            "name": "busybox-container",
            "command": "sh -c 'while true; do echo Hello from Busybox; sleep 3600; done'",
            "detach": True
        },
        {
            "image": "alpine",
            "name": "alpine-container", 
            "command": "sleep 1000",
            "detach": True
        },
        {
            "image": "redis",
            "name": "redis-container",
            "command": None,
            "detach": True
        }
    ]
    
    print("Creating and starting test containers...")
    
    for container_config in containers_to_create:
        try:
            # 기존 컨테이너가 있으면 제거
            try:
                existing_container = client.containers.get(container_config["name"])
                print(f"Stopping and removing existing container: {container_config['name']}")
                existing_container.stop()
                existing_container.remove()
                time.sleep(2)
            except docker.errors.NotFound:
                pass
            
            # 새 컨테이너 생성 및 실행
            if container_config["command"]:
                container = client.containers.run(
                    container_config["image"],
                    container_config["command"],
                    name=container_config["name"],
                    detach=container_config["detach"]
                )
            else:
                container = client.containers.run(
                    container_config["image"],
                    name=container_config["name"],
                    detach=container_config["detach"]
                )
                
            print(f"✓ Created and started: {container_config['name']}")
            
        except Exception as e:
            print(f"✗ Failed to create {container_config['name']}: {e}")
    
    print("\nContainer setup completed!")
    print("\nCurrent containers:")
    list_containers()
    
    client.close()

def list_containers():
    """현재 실행 중인 컨테이너 목록을 출력하는 함수"""
    
    client = docker.from_env()
    containers = client.containers.list(all=True)
    
    if not containers:
        print("No containers found.")
        return
    
    print(f"{'Name':<20} {'Status':<15} {'Image':<15}")
    print("-" * 50)
    
    for container in containers:
        name = container.name
        status = container.status
        image = container.image.tags[0] if container.image.tags else container.image.id[:12]
        print(f"{name:<20} {status:<15} {image:<15}")
    
    client.close()

def cleanup_containers():
    """모든 테스트 컨테이너를 정리하는 함수"""
    
    client = docker.from_env()
    container_names = ["nginx-container", "busybox-container", "alpine-container", "redis-container"]
    
    print("Cleaning up test containers...")
    
    for container_name in container_names:
        try:
            container = client.containers.get(container_name)
            print(f"Stopping and removing: {container_name}")
            container.stop()
            container.remove()
            print(f"✓ Removed: {container_name}")
        except docker.errors.NotFound:
            print(f"Container not found: {container_name}")
        except Exception as e:
            print(f"✗ Failed to remove {container_name}: {e}")
    
    print("Cleanup completed!")
    client.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python container_setup.py [setup|list|cleanup]")
        print("  setup   - Create and start test containers")
        print("  list    - List current containers") 
        print("  cleanup - Stop and remove test containers")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup_test_containers()
    elif command == "list":
        list_containers()
    elif command == "cleanup":
        cleanup_containers()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: setup, list, cleanup")