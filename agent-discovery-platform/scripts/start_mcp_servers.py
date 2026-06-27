import subprocess
import os
import sys

def start_server(script_name):
    # Using python -m mcp run to start the servers
    # Alternatively we can just run the python file directly if it has mcp.run()
    print(f"Starting {script_name}...")
    return subprocess.Popen([sys.executable, f"backend/mcp_servers/{script_name}"])

if __name__ == "__main__":
    servers = [
        "github_server.py",
        "confluence_server.py",
        "agent_registry_server.py",
        "mcp_catalog_server.py"
    ]
    
    processes = []
    try:
        for server in servers:
            processes.append(start_server(server))
            
        print("All MCP servers started. Press Ctrl+C to stop.")
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("Stopping servers...")
        for p in processes:
            p.terminate()
        print("Servers stopped.")
