from flask import Flask
import os
import psutil
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask app! Visit the <a href='/htop'>/htop</a> endpoint for system information."

@app.route('/htop')
def htop():
    try:
        # Get system information
        name = "Abhinash Kumar"  # Replace with your full name
        username = os.getenv('USER', 'codespace')  # Fallback for Codespaces
        ist_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

        # Get process information using psutil
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            processes.append(proc.info)

        # Format the response
        response = f"""
        <pre>
        Name: {name}
        Username: {username}
        Server Time (IST): {ist_time}
        Top Output:
        PID\tName\t\tCPU%\tMemory
        """
        for proc in processes[:10]:  # Show top 10 processes
            response += f"{proc['pid']}\t{proc['name']}\t{proc['cpu_percent']}%\t{proc['memory_info'].rss / 1024 / 1024:.2f} MB\n"
        response += "</pre>"
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
