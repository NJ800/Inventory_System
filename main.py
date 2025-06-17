import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from database import DatabaseManager
from login import LoginDialog
from main_window import MainWindow

def main():
    print("DEBUG: Starting main()")  # Debug 1
    app = QApplication(sys.argv)
    print("DEBUG: QApplication created")  # Debug 2
    
    try:
        print("DEBUG: Initializing database...")  # Debug 3
        db = DatabaseManager()
        print("DEBUG: Database initialized")  # Debug 4
        
        print("DEBUG: Creating login dialog...")  # Debug 5
        login = LoginDialog(db)
        
        print("DEBUG: Showing login...")  # Debug 6
        if login.exec() == 1:
            print("DEBUG: Login successful")  # Debug 7
            window = MainWindow(db)
            window.show()
            print("DEBUG: Main window shown")  # Debug 8
            sys.exit(app.exec())
        else:
            print("DEBUG: Login failed/cancelled")  # Debug 9
            sys.exit()
            
    except Exception as e:
        print("DEBUG: Exception occurred:", e)  # Debug 10
        QMessageBox.critical(None, "Fatal Error", str(e))
        sys.exit(1)

if __name__ == "__main__":
    print("DEBUG: Script started")  # Debug 0
    main()
