import os
import sys
from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

class Backend(QObject):
    @Slot(str, result=str)
    def process_data(self, message):
        print(f"Received message from frontend: {message}")
        return f"Processed {message} in Python"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PySide6 React Integration')
        self.setGeometry(100, 100, 800, 600)

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QWebEngineView
        self.browser = QWebEngineView()

        # Set the URL to the local React app build
        react_build_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'react_build', 'index.html')
        self.browser.load(QUrl.fromLocalFile(react_build_path))
        
        # Add the browser to the layout
        layout.addWidget(self.browser)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Setup QtWebChannel
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('backend', self.backend)
        self.browser.page().setWebChannel(self.channel)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
