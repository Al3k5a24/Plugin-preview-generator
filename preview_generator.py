#!/usr/bin/env python3
"""
Minimal universal project runner: detects project type by files and runs it in Docker.
Supported: Node.js (package.json), Python (requirements.txt), Go (main.go), .NET (.csproj)
"""
import sys
import subprocess
from pathlib import Path

def detect_command_and_port(project_path: Path):
    if (project_path / "package.json").exists():
        return "npm install && npm start", "3000:3000"
    if (project_path / "requirements.txt").exists():
        return "pip install -r requirements.txt && python app.py", "5000:5000"
    if (project_path / "main.go").exists():
        return "go run .", "8080:8080"
    for file in project_path.glob("*.csproj"):
        return "dotnet run", "5000:5000"
    return None, None

def main():
    if len(sys.argv) < 2:
        print("Usage: python preview_generator.py <project_path>")
        sys.exit(1)
    project_path = Path(sys.argv[1]).resolve()
    if not project_path.exists():
        print(f"❌ Path '{project_path}' does not exist!")
        sys.exit(1)
    command, ports = detect_command_and_port(project_path)
    if not command:
        print("❌ Could not detect project type (supported: Node.js, Python, Go, .NET). Add package.json, requirements.txt, main.go, or .csproj.")
        sys.exit(1)
    docker_image = "universal-project-runner"
    dockerfile_path = Path("Dockerfile")
    if not dockerfile_path.exists():
        print("❌ Dockerfile not found in current directory!")
        sys.exit(1)
    result = subprocess.run(["docker", "images", "-q", docker_image], capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"🔨 Building Docker image '{docker_image}'...")
        subprocess.run(["docker", "build", "-t", docker_image, "."], check=True)
    container_name = f"{project_path.name.lower().replace(' ', '-')}-sandbox"
    result = subprocess.run(["docker", "ps", "-a", "-q", "-f", f"name={container_name}"], capture_output=True, text=True)
    if result.stdout.strip():
        subprocess.run(["docker", "stop", container_name])
        subprocess.run(["docker", "rm", container_name])
    port_args = []
    if ports:
        host_port, container_port = ports.split(":")
        port_args = ["-p", f"{host_port}:{container_port}"]
    docker_cmd = [
        "docker", "run", "--rm", "--name", container_name,
        "-v", f"{project_path}:/app", "-w", "/app"
    ] + port_args + [docker_image, "bash", "-c", command]
    print(f"🚀 Running {project_path.name} in Docker as {container_name}...")
    print(f"   Command: {command}")
    print(f"   Ports: {ports}")
    # Print all output from the container live
    process = subprocess.Popen(docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        for line in process.stdout:
            print(line, end="")
    except KeyboardInterrupt:
        process.terminate()
    process.wait()

if __name__ == "__main__":
    main()