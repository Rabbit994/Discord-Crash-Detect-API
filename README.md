# Discord-Crash-Detect-API
Detects Discord Video Crasher MP4 and GIFs

# Endpoint
Endpoint will be <url>/checkfile?url=URL_of_file_to_test
You can also look at very simple docs provided by FastAPI swagger <url>/docs
There is also /ping endpoint, this only returns PONG but is easy way for Load Balancer to confirm endpoint is alive
# App
Python code is located in App Folder
# Developing Locally
Python 3.9 required, if you using VSCode, then use development container for easy configuration
If not, requirements.txt file provided but to execute FastAPI in Uvicorn, it's "uvicorn app.main:app"


