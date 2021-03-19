# ServerStatusBackend
Python program that runs as a JsonRpcServer to return server status data on request

# Install Service on Linux
Copy the JsonRpcStatusServer to /lib/systemd/system/
Adapt the path to your system

Add the service to linux


    sudo systemctl daemon-reload


Enable and start the service

    sudo systemctl enable JsonRpcStatusServer.service
    sudo systemctl start JsonRpcStatusServer.service
