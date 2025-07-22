import threading
from app import app, server

if __name__ == "__main__":
    
    threading.Thread(target=app.run).start()
    server.run()
