{
  "mcpServers": {
    "enterprise-server": {
      "command": "bash",
      "args": [
        "-c",
        "docker images | grep -q ghcr.io/pere94/mcp-server-demo:latest || docker pull ghcr.io/pere94/mcp-server-demo:latest >/dev/null 2>&1; docker run -i --rm --init -e DOCKER_CONTAINER=true ghcr.io/pere94/mcp-server-demo:latest"
      ]
    }
  }
}

{
  "mcpServers": {
    "enterprise-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e",
        "DOCKER_CONTAINER=true",
        "mcp/enterprise-server"
      ]
    }
  }
}
