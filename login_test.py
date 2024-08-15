import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtCore import Qt, QDateTime

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("User Login")
        self.setGeometry(100, 100, 300, 200)
        
        # Layouts
        layout = QVBoxLayout()
        
        # User Role Dropdown
        self.role_label = QLabel("Select Role:")
        layout.addWidget(self.role_label)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Operator", "Supervisor", "Admin"])
        layout.addWidget(self.role_combo)
        
        # Username
        self.user_label = QLabel("Username:")
        layout.addWidget(self.user_label)
        
        self.user_input = QLineEdit()
        layout.addWidget(self.user_input)
        
        # Password
        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)
        
        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Set layout to the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def check_login(self):
        # Placeholder for actual authentication logic
        username = self.user_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()
        
        # Example check (replace with actual authentication)
        if username == "admin" and password == "admin" and role == "Admin":
            self.log_login(username, role)
            self.status_label.setText("Login Successful! Role: Admin")
            self.status_label.setStyleSheet("color: green;")
            self.start_process(role)
        elif username == "supervisor" and password == "supervisor" and role == "Supervisor":
            self.log_login(username, role)
            self.status_label.setText("Login Successful! Role: Supervisor")
            self.status_label.setStyleSheet("color: green;")
            self.start_process(role)
        elif username == "operator" and password == "operator" and role == "Operator":
            self.log_login(username, role)
            self.status_label.setText("Login Successful! Role: Operator")
            self.status_label.setStyleSheet("color: green;")
            self.start_process(role)
        else:
            self.status_label.setText("Login Failed!")
            self.status_label.setStyleSheet("color: red;")
        
    def log_login(self, username, role):
        current_time = QDateTime.currentDateTime().toString(Qt.ISODate)
        with open("user_log.txt", "a") as file:
            file.write(f"{current_time} - {username} logged in as {role}\n")
    
    def start_process(self, role):
        # Placeholder to start the process based on role
        # Example:
        # if role == "Admin":
        #     self.admin_dashboard()
        # elif role == "Supervisor":
        #     self.supervisor_dashboard()
        # else:
        #     self.operator_dashboard()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
