import sys
import os
import json
import webbrowser
import subprocess
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import requests
import math
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyautogui

MEMORY_FILE = 'jarvis_memory.json'
WEATHER_API = 'YOUR_API_KEY'
c=subprocess
p=Qt
t=pyautogui
class JarvisAI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Jarvis AI - Hadi Edition')
        self.setGeometry(200, 100, 900, 650)
        self.memory = self.load_memory()
        self.engine = pyttsx3.init()
        self.init_ui()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        return {'notes': [], 'history': [], 'tasks': []}

    def save_memory(self):
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        self.output = QTextEdit(); self.output.setReadOnly(True)
        self.input = QLineEdit(); self.input.returnPressed.connect(self.process_command)
        voice_btn = QPushButton('Voice Command'); voice_btn.clicked.connect(self.listen)
        layout.addWidget(QLabel('JARVIS AI'))
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        layout.addWidget(voice_btn)
        central.setLayout(layout)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def respond(self, text):
        self.output.append(f'Jarvis: {text}')
        self.speak(text)

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                cmd = r.recognize_google(audio)
                self.input.setText(cmd)
                self.process_command()
            except:
                self.respond('Could not understand.')

    def open_app(self, app):
        apps = {
            'chrome':'start chrome',
            'vscode':'code',
            'notepad':'notepad',
            'calculator':'calc',
            'spotify':'spotify'
        }
        if app in apps:
            os.system(apps[app])
            self.respond(f'Opening {app}')

    def close_app(self, app):
        processes = {
            'chrome':'chrome.exe',
            'vscode':'Code.exe',
            'notepad':'notepad.exe',
            'spotify':'Spotify.exe'
        }
        if app in processes:
            os.system(f'taskkill /f /im {processes[app]}')
            self.respond(f'Closed {app}')

    def weather(self, city='Pune'):
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric'
            data = requests.get(url).json()
            temp = data['main']['temp']
            self.respond(f'{city} temperature is {temp}°C')
        except:
            self.respond('Weather lookup failed')

    def process_command(self):
        cmd = self.input.text().lower()
        self.memory['history'].append(cmd)
        self.save_memory()

        if 'time' in cmd:
            self.respond(datetime.now().strftime('%H:%M:%S'))
        elif 'date' in cmd:
            self.respond(str(datetime.now().date()))
        elif cmd.startswith('open '):
            self.open_app(cmd.replace('open ','').strip())
        elif cmd.startswith('close '):
            self.close_app(cmd.replace('close ','').strip())
        elif cmd.startswith('search '):
            query = cmd.replace('search ','').strip().replace(' ','+')
            webbrowser.open(f'https://www.google.com/search?q={query}')
            self.respond(f'Searching Google for {query}')
        elif cmd.startswith('youtube '):
            creator = cmd.replace('youtube ','').strip().replace(' ','+')
            webbrowser.open(f'https://www.youtube.com/results?search_query={creator}')
            self.respond(f'Opening YouTube search for {creator}')
        elif cmd.startswith('weather'):
            self.weather()
        elif cmd.startswith('note '):
            self.memory['notes'].append(cmd[5:])
            self.respond('Note saved')
        elif cmd.startswith('task '):
            self.memory['tasks'].append(cmd[5:])
            self.respond('Task added')
        elif cmd.startswith('calc '):
            expr = cmd.replace('calc ','').strip()
            try:
                result = eval(expr)
                self.respond(f'Result: {result}')
            except:
                self.respond('Invalid calculation')
        elif cmd.startswith('log '):
            num = float(cmd.replace('log ','').strip())
            self.respond(f'Log: {math.log10(num)}')
        elif cmd.startswith('antilog '):
            num = float(cmd.replace('antilog ','').strip())
            self.respond(f'Antilog: {10**num}')
        elif cmd.startswith('area circle '):
            r = float(cmd.replace('area circle ','').strip())
            self.respond(f'Area: {math.pi*r*r}')
        elif cmd.startswith('volume sphere '):
            r = float(cmd.replace('volume sphere ','').strip())
            self.respond(f'Volume: {(4/3)*math.pi*r**3}')
        elif cmd.startswith('area rectangle '):
            vals = cmd.replace('area rectangle ','').split()
            self.respond(f'Area: {float(vals[0])*float(vals[1])}')
        elif cmd.startswith('volume cube '):
            s = float(cmd.replace('volume cube ','').strip())
            self.respond(f'Volume: {s**3}')
        elif cmd.startswith('area square '):
            s = float(cmd.replace('area square ','').strip())
            self.respond(f'Area: {s**2}')
        elif cmd.startswith('area triangle '):
            vals = cmd.replace('area triangle ','').split()
            self.respond(f'Area: {0.5*float(vals[0])*float(vals[1])}')
        elif cmd.startswith('volume cylinder '):
            vals = cmd.replace('volume cylinder ','').split()
            r,h = float(vals[0]), float(vals[1])
            self.respond(f'Volume: {math.pi*r*r*h}')
        elif cmd.startswith('volume cone '):
            vals = cmd.replace('volume cone ','').split()
            r,h = float(vals[0]), float(vals[1])
            self.respond(f'Volume: {(1/3)*math.pi*r*r*h}')
        elif cmd.startswith('sqrt '):
            n = float(cmd.replace('sqrt ','').strip())
            self.respond(f'Square root: {math.sqrt(n)}')
        elif cmd.startswith('factorial '):
            n = int(cmd.replace('factorial ','').strip())
            self.respond(f'Factorial: {math.factorial(n)}')
        elif cmd.startswith('sin '):
            n = float(cmd.replace('sin ','').strip())
            self.respond(f'Sin: {math.sin(math.radians(n))}')
        elif cmd.startswith('cos '):
            n = float(cmd.replace('cos ','').strip())
            self.respond(f'Cos: {math.cos(math.radians(n))}')
        elif cmd.startswith('tan '):
            n = float(cmd.replace('tan ','').strip())
            self.respond(f'Tan: {math.tan(math.radians(n))}')
        elif cmd == 'show desktop':
            os.system('powershell -command "(new-object -com shell.application).toggleDesktop()"')
            self.respond('Showing desktop')
        elif cmd == 'scan wifi':
            output = os.popen('netsh wlan show networks').read()
            self.respond(output[:800])
        elif cmd == 'wifi status':
            output = os.popen('netsh wlan show interfaces').read()
            self.respond(output[:800])
        elif cmd == 'battery':
            output = os.popen('wmic path Win32_Battery get EstimatedChargeRemaining').read()
            self.respond(output)
        elif cmd == 'cpu':
            output = os.popen('wmic cpu get loadpercentage').read()
            self.respond(output)
        elif cmd == 'ram':
            output = os.popen('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value').read()
            self.respond(output)
        elif cmd == 'disk':
            output = os.popen('wmic logicaldisk get size,freespace,caption').read()
            self.respond(output)
        elif cmd == 'desktop files':
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            files = os.listdir(desktop)
            self.respond('Desktop files: ' + ', '.join(files[:20]))
        elif cmd.startswith('find '):
            target = cmd.replace('find ','').strip().lower()
            matches=[]
            for root,dirs,files in os.walk(os.path.expanduser('~')):
                for f in files:
                    if target in f.lower():
                        matches.append(os.path.join(root,f))
                        if len(matches)>=10: break
                if len(matches)>=10: break
            self.respond(''.join(matches) if matches else 'No files found')
        elif cmd.startswith('timer '):
            mins=int(cmd.replace('timer ','').strip())
            self.respond(f'Timer started for {mins} minutes')
        elif cmd=='pomodoro':
            self.respond('Pomodoro started: 25 min study, 5 min break')
        elif cmd.startswith('note '):
            with open('notes.txt','a') as f: f.write(cmd.replace('note ','')+'')
            self.respond('Note saved')
        elif cmd=='show notes':
            self.respond(open('notes.txt').read() if os.path.exists('notes.txt') else 'No notes')
        elif cmd.startswith('add task '):
            with open('tasks.txt','a') as f: f.write(cmd.replace('add task ','')+'')
            self.respond('Task added')
        elif cmd=='show tasks':
            self.respond(open('tasks.txt').read() if os.path.exists('tasks.txt') else 'No tasks')
        elif cmd=='screenshot':
            import pyautogui
            pyautogui.screenshot('screenshot.png')
            self.respond('Screenshot saved')
        elif cmd=='clipboard':
            self.respond(self.root.clipboard_get())
        elif cmd=='joke':
            self.respond('Why do programmers prefer dark mode? Because light attracts bugs.')
        elif cmd=='motivate':
            self.respond('Stay consistent. Small daily progress builds big results.')
        elif 'study mode' in cmd:
            self.respond('25 minute focus session started')
        elif 'history' in cmd:
            self.respond('\n'.join(self.memory['history'][-10:]))
        else:
            self.respond('Command not recognized')
        self.save_memory()
        self.input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = JarvisAI()
    win.show()
    sys.exit(app.exec())
