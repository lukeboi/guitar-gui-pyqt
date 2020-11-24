import rtmidi
from PyQt5.QtCore import QDir, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence


class MainWindow(QMainWindow):
    def closeEvent(self, e):
        if not text.document().isModified():
            return
        answer = QMessageBox.question(
            window, None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        if answer & QMessageBox.Save:
            file_selection_list.save()
        elif answer & QMessageBox.Cancel:
            e.ignore()


class midi_handling_bar(QWidget):
    midiout = rtmidi.MidiOut()

    def __init__(self):
        QWidget.__init__(self)

        self.layout = QHBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.refresh_button = QPushButton("Refresh MIDI Devices")
        self.refresh_button.setMaximumWidth(130)
        self.refresh_button.clicked.connect(self.refresh_button_pressed)

        self.select_dropdown = QComboBox(self)
        self.select_dropdown.activated[str].connect(self.port_selected)

        layout.addWidget(self.refresh_button)
        layout.addWidget(self.select_dropdown)

        self.refresh_button_pressed()

    def refresh_button_pressed(self):
        available_ports = self.midiout.get_ports()
        self.select_dropdown.clear()
        self.select_dropdown.addItems(available_ports)

    def port_selected(self):
        self.midiout.open_port(self.select_dropdown.currentIndex())


class file_selection_list(QWidget):
    working_dir_path = ""
    current_file = ""

    def __init__(self):
        QWidget.__init__(self)

        self.list = QTreeView()

        file_path = None
        self.fileModel = QFileSystemModel()
        # self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)
        self.list.setModel(self.fileModel)
        self.list.selectionModel().selectionChanged.connect(self.open_file)


        self.layout = QHBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        layout.addWidget(self.list)

    def open_folder(self):
        path = QFileDialog.getExistingDirectory(window, "Open Folder")
        if path:
            self.list.setRootIndex(self.fileModel.setRootPath(str(path)))
            self.working_dir_path = path

    def open_file(self):
        self.current_file = str(self.list.currentIndex().data())
        print(self.current_file)

    def save(self):
        if file_path is None:
            self.save_as()
        else:
            with open(file_path, "w") as f:
                f.write(text.toPlainText())
            text.document().setModified(False)

    def save_as(self):
        global file_path
        path = QFileDialog.getSaveFileName(window, "Save As")[0]
        if path:
            file_path = path
            self.save()

app = QApplication([])
app.setApplicationName("Guitar Controller")
window = MainWindow()

layout = QVBoxLayout()

text = QPlainTextEdit()


central = QWidget()
central.setLayout(layout)

midi_bar = midi_handling_bar()
file_list = file_selection_list()

layout.addWidget(midi_bar, 0)
layout.addWidget(file_list, 0)
layout.addWidget(text, 0)
window.setCentralWidget(central)
window.resize(600, 450)

menu = window.menuBar().addMenu("&File")
open_action = QAction("&Open Folder")




open_action.triggered.connect(file_list.open_folder)
open_action.setShortcut(QKeySequence.Open)
menu.addAction(open_action)

save_action = QAction("&Save")




save_action.triggered.connect(file_list.save)
save_action.setShortcut(QKeySequence.Save)
menu.addAction(save_action)

save_as_action = QAction("Save &As...")




save_as_action.triggered.connect(file_list.save_as)
menu.addAction(save_as_action)

close = QAction("&Close")
close.triggered.connect(window.close)
menu.addAction(close)

help_menu = window.menuBar().addMenu("&Help")
about_action = QAction("&About")
help_menu.addAction(about_action)


def show_about_dialog():
    text = "<center>" \
           "<h1>Text Editor</h1>" \
           "&#8291;" \
           "<img src=icon.svg>" \
           "</center>" \
           "<p>Version 31.4.159.265358<br/>" \
           "Copyright &copy; Company Inc.</p>"
    QMessageBox.about(window, "About Text Editor", text)


about_action.triggered.connect(show_about_dialog)

window.show()
app.exec_()
