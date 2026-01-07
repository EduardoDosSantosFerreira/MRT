import os
import shutil
import ctypes
import winreg
import platform

from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame,
    QStackedLayout, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap  # Adicione QPixmap aqui

import logic


class SecurityTool(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MAX SECURITY PLUS")
        self.showFullScreen()  # Apenas fullscreen
        
        self.COLORS = {
            "pink": "#FF1493",
            "dark_pink": "#C71585",
            "light_pink": "#FF69B4",
            "bg": "#0A0A0A",
            "card": "#1A1A1A",
            "card_hover": "#252525",
            "text": "#FFFFFF",
            "border": "#FF1493",
            "success": "#00FF7F",
            "warning": "#FFA500",
        }

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.COLORS['bg']};
                color: {self.COLORS['text']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton {{
                border: none;
                padding: 14px 20px;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
                border-radius: 6px;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['pink']};
                color: white;
            }}
            QFrame#card {{
                background-color: {self.COLORS['card']};
                border: 1px solid {self.COLORS['border']};
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame#card:hover {{
                background-color: {self.COLORS['card_hover']};
                border-color: {self.COLORS['light_pink']};
            }}
            QLabel#title {{
                font-size: 28px;
                font-weight: bold;
                color: {self.COLORS['pink']};
                padding-bottom: 10px;
            }}
        """)

        main = QHBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ───── SIDEBAR ─────
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setStyleSheet(f"""
            QWidget#sidebar {{
                background-color: #111111;
                border-right: 2px solid {self.COLORS['pink']};
            }}
        """)
        sidebar_widget.setFixedWidth(260)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Logo
        logo_frame = QFrame()
        logo_frame.setStyleSheet(f"""
            background-color: #000000;
            border-bottom: 2px solid {self.COLORS['pink']};
        """)
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(20, 30, 20, 30)
        
        logo_icon = QLabel()
        logo_icon.setAlignment(Qt.AlignCenter)
        
        # Verifique se a imagem existe antes de carregar
        logo_path = "MRTSTANDART.ico"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_icon.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                # Se a imagem não carregar, use texto como fallback
                logo_icon.setText("MSP")
                logo_icon.setStyleSheet("""
                    color: white;
                    font-size: 36px;
                    font-weight: bold;
                """)
        else:
            # Se o arquivo não existir, use texto
            logo_icon.setText("MSP")
            logo_icon.setStyleSheet("""
                color: white;
                font-size: 36px;
                font-weight: bold;
            """)
        
        logo_text = QLabel("MAX SECURITY PLUS")
        logo_text.setAlignment(Qt.AlignCenter)
        logo_text.setStyleSheet("""
            color: #FF1493;
            font-size: 16px;
            font-weight: bold;
            line-height: 1.3;
            margin-top: 10px;
        """)
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        
        # Botões da sidebar
        btn_style = f"""
            QPushButton {{
                border: none;
                padding: 16px 25px;
                font-size: 15px;
                font-weight: 500;
                text-align: left;
                border-radius: 0px;
                border-left: 3px solid transparent;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #222222;
                border-left: 3px solid {self.COLORS['pink']};
                color: white;
            }}
        """
        
        self.btn_dashboard = QPushButton("📊 Dashboard")
        self.btn_dashboard.setStyleSheet(btn_style)
        self.btn_dashboard.setCursor(Qt.PointingHandCursor)
        
        self.btn_tools = QPushButton("⚙️ Security Tools")
        self.btn_tools.setStyleSheet(btn_style)
        self.btn_tools.setCursor(Qt.PointingHandCursor)
        
        # Botão Sair com estilo especial
        btn_exit = QPushButton("🚪 Exit Application")
        btn_exit.setStyleSheet(f"""
            QPushButton {{
                background-color: #2A0A0A;
                color: white;
                border: 1px solid #FF1493;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                margin: 20px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: #FF1493;
                color: white;
                border-color: {self.COLORS['dark_pink']};
            }}
        """)
        btn_exit.setCursor(Qt.PointingHandCursor)

        sidebar_layout.addWidget(logo_frame)
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_tools)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(btn_exit)

        # ───── STACK ─────
        self.stack = QStackedLayout()
        self.stack.addWidget(self.dashboard_page())
        self.stack.addWidget(self.tools_page())

        content_widget = QWidget()
        content_widget.setLayout(self.stack)

        main.addWidget(sidebar_widget)
        main.addWidget(content_widget)

        # Conectar sinais
        self.btn_dashboard.clicked.connect(lambda: self.set_page(0))
        self.btn_tools.clicked.connect(lambda: self.set_page(1))
        btn_exit.clicked.connect(self.confirm_exit)
        
        # Indicador visual da página atual
        self.current_button = self.btn_dashboard
        self.highlight_button(self.btn_dashboard)

    def set_page(self, index):
        self.stack.setCurrentIndex(index)
        
        # Destacar botão atual
        if index == 0:
            self.highlight_button(self.btn_dashboard)
            self.unhighlight_button(self.btn_tools)
        else:
            self.highlight_button(self.btn_tools)
            self.unhighlight_button(self.btn_dashboard)

    def highlight_button(self, button):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLORS['pink']};
                color: white;
                border-left: 3px solid white;
                padding: 16px 25px;
                font-size: 15px;
                font-weight: bold;
            }}
        """)

    def unhighlight_button(self, button):
        button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                padding: 16px 25px;
                font-size: 15px;
                font-weight: 500;
                text-align: left;
                border-radius: 0px;
                border-left: 3px solid transparent;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #222222;
                border-left: 3px solid {self.COLORS['pink']};
                color: white;
            }}
        """)

    def confirm_exit(self):
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit MSP?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()

    # ─────────────────────────────
    # DASHBOARD
    # ─────────────────────────────
    def dashboard_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("SYSTEM DASHBOARD")
        title.setObjectName("title")
        layout.addWidget(title)

        # Grid de especificações
        specs = self.get_system_specs()
        
        grid_layout = QVBoxLayout()
        grid_layout.setSpacing(15)
        
        keys = list(specs.keys())
        # Dividir em 2 colunas
        for i in range(0, len(keys), 2):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(20)
            
            # Primeiro card da linha
            if i < len(keys):
                row_layout.addWidget(self.info_card(keys[i], specs[keys[i]]))
            
            # Segundo card da linha
            if i + 1 < len(keys):
                row_layout.addWidget(self.info_card(keys[i + 1], specs[keys[i + 1]]))
            elif i < len(keys):
                # Se não houver segundo card, adiciona widget vazio para manter alinhamento
                row_layout.addWidget(QWidget())
            
            grid_layout.addLayout(row_layout)
        
        layout.addLayout(grid_layout)
        layout.addStretch()

        # Status bar
        status_bar = QFrame()
        status_bar.setStyleSheet(f"""
            background-color: {self.COLORS['card']};
            border: 1px solid {self.COLORS['border']};
            border-radius: 8px;
            padding: 15px;
        """)
        
        status_layout = QHBoxLayout(status_bar)
        
        status_dot = QLabel("●")
        status_dot.setStyleSheet(f"color: {self.COLORS['light_pink']}; font-size: 20px;")  # Rosa claro
        status_text = QLabel("System Status: All services operational")
        status_text.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        
        status_layout.addWidget(status_dot)
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        
        layout.addWidget(status_bar)

        return widget

    def get_system_specs(self):
        # RAM real
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        memory = MEMORYSTATUS()
        memory.dwLength = ctypes.sizeof(MEMORYSTATUS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
        ram_gb = round(memory.ullTotalPhys / (1024 ** 3), 2)

        # CPU real (registro do Windows)
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
        ) as key:
            cpu_name = winreg.QueryValueEx(key, "ProcessorNameString")[0]

        # Disco principal
        total, used, free = shutil.disk_usage("C:\\")
        free_percent = (free / total) * 100
        
        return {
            "🖥️ Operating System": f"{platform.system()} {platform.release()}",
            "🏷️ Computer Name": platform.node(),
            "⚡ Processor": cpu_name[:40] + "..." if len(cpu_name) > 40 else cpu_name,
            "📐 Architecture": "64-bit" if platform.machine().endswith("64") else "32-bit",
            "🧠 Installed RAM": f"{ram_gb} GB",
            "💽 Disk Total (C:)": f"{round(total / (1024**3), 2)} GB",
            "💾 Disk Free (C:)": f"{round(free / (1024**3), 2)} GB ({free_percent:.1f}%)",
            "👤 Logged User": os.getlogin(),
        }

    def info_card(self, label, value):
        frame = QFrame()
        frame.setObjectName("card")
        frame.setMinimumHeight(100)
        frame.setCursor(Qt.PointingHandCursor)

        v = QVBoxLayout(frame)
        v.setSpacing(8)

        lbl_title = QLabel(label)
        lbl_title.setStyleSheet("""
            font-size: 14px;
            color: #FF69B4;  /* Rosa claro */
            font-weight: 500;
        """)

        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: white;
        """)
        lbl_value.setWordWrap(True)

        v.addWidget(lbl_title)
        v.addWidget(lbl_value)

        return frame

    # ─────────────────────────────
    # TOOLS
    # ─────────────────────────────
    def tools_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("SECURITY TOOLS")
        title.setObjectName("title")
        layout.addWidget(title)

        # Descrição
        desc = QLabel("Select a security tool to execute. Some tools may require administrator privileges.")
        desc.setStyleSheet("font-size: 14px; color: #FFFFFF; margin-bottom: 20px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Grid de ferramentas
        tools_grid = QVBoxLayout()
        tools_grid.setSpacing(15)
        
        # Primeira linha
        row1 = QHBoxLayout()
        row1.setSpacing(20)
        row1.addWidget(self.tool_card("🛡️ MRT Scan", "Malicious Software Removal Tool", logic.run_mrt))
        row1.addWidget(self.tool_card("🔍 SFC Scan", "System File Checker", logic.run_sfc))
        
        # Segunda linha
        row2 = QHBoxLayout()
        row2.setSpacing(20)
        row2.addWidget(self.tool_card("⚙️ DISM Repair", "Deployment Image Servicing", logic.run_dism))
        row2.addWidget(self.tool_card("🧹 Clean Temp", "Temporary Files Cleaner", logic.clean_temp))
        
        tools_grid.addLayout(row1)
        tools_grid.addLayout(row2)
        
        layout.addLayout(tools_grid)
        layout.addStretch()

        return widget

    def tool_card(self, title, description, action):
        frame = QFrame()
        frame.setObjectName("card")
        frame.setMinimumHeight(150)
        frame.setCursor(Qt.PointingHandCursor)

        v = QVBoxLayout(frame)
        v.setSpacing(12)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
        """)

        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet("""
            font-size: 14px;
            color: #FFFFFF;
        """)
        lbl_desc.setWordWrap(True)

        btn = QPushButton("▶ EXECUTE NOW")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLORS['pink']};
                color: white;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                border: 2px solid transparent;
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['dark_pink']};
                border: 2px solid white;
            }}
            QPushButton:pressed {{
                background-color: #B0006A;
            }}
        """)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(action)

        v.addWidget(lbl_title)
        v.addWidget(lbl_desc)
        v.addStretch()
        v.addWidget(btn)

        return frame