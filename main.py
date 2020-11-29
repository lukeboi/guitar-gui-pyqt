import time

import rtmidi
from PyQt5.QtCore import QDir, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence

import midi_io


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
    def __init__(self):
        QWidget.__init__(self)

        midi_io.init()

        self.l = QHBoxLayout()
        # self.widget = QWidget()
        # self.widget.setLayout(self.l)
        self.setLayout(self.l)

        self.refresh_button = QPushButton("Refresh MIDI Devices")
        self.refresh_button.setMaximumWidth(130)
        self.refresh_button.clicked.connect(self.refresh_button_pressed)

        self.select_dropdown = QComboBox()
        self.select_dropdown.activated[str].connect(self.port_selected)

        self.play_button = QPushButton("Play Piece")
        self.play_button.setMaximumWidth(130)
        self.play_button.clicked.connect(self.refresh_button_pressed)

        self.l.addWidget(self.refresh_button)
        self.l.addWidget(self.select_dropdown)
        self.l.addWidget(self.play_button)

        self.refresh_button_pressed()
        self.port_selected()
        self.show()

    def refresh_button_pressed(self):
        available_ports = midi_io.midiout.get_ports()
        self.select_dropdown.clear()
        self.select_dropdown.addItems(available_ports)

    def port_selected(self):
        midi_io.midiout.open_port(self.select_dropdown.currentIndex())


class file_speific_buttons(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.save_button = QPushButton("Save File")
        self.save_button.setMaximumWidth(130)
        self.layout.addWidget(self.save_button)

        self.save_as_button = QPushButton("Save File As")
        self.save_as_button.setMaximumWidth(130)
        self.layout.addWidget(self.save_as_button)
        self.show()



class file_selection_list(QWidget):
    working_dir_path = ""
    current_file = ""

    def __init__(self):
        QWidget.__init__(self)

        self.list = QTreeView()

        self.current_file = None
        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)
        self.list.setModel(self.fileModel)
        self.list.selectionModel().selectionChanged.connect(self.open_file)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.list)

    def open_folder(self):
        path = QFileDialog.getExistingDirectory(window, "Open Folder")
        if path:
            self.list.setRootIndex(self.fileModel.setRootPath(str(path)))
            self.working_dir_path = path

    def open_file(self):
        if text.document().isModified():
            answer = QMessageBox.question(
                window, None,
                "You have unsaved changes. Save before opening another file?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if answer & QMessageBox.Save:
                self.save()

            elif answer & QMessageBox.Cancel:
                return

        self.current_file = self.working_dir_path + "/" + str(self.list.selectedIndexes()[0].data())
        # self.list.itemFromIndex()
        # print(self.current_file)
        text.setPlainText(open(self.current_file).read())

    def save(self):
        if self.current_file is None:
            self.save_as()
        else:
            with open(self.current_file, "w") as f:
                f.write(text.toPlainText())
            text.document().setModified(False)

    def save_as(self):
        path = QFileDialog.getSaveFileName(window, "Save As")[0]
        if path:
            self.current_file = path
            self.save()

def play_piece(piece_str):
    piece_commands = piece_str.splitlines()
    for i in piece_commands:
        print(i)
        # remove comments
        if i.find("#") != -1:
            i = i[:i.find("#")]

        # try to get command and corresponding arguments for command
        command = i[:i.find(" ")]
        args = i[i.find(" ") + 1:]

        # if there is a command and args, run the command
        if len(i) > 0 and i.find(" ") != -1 and len(command) > 0:

            if command == "play":
                note_nums = args.replace(" ", "").split(",")
                for n in note_nums:
                    print("playing note: " + str(n))
                    midi_io.play_note(int(n))

            elif command == "wait":
                time.sleep(int(args))


app = QApplication([])
app.setApplicationName("Guitar Controller")
window = MainWindow()

window_layout = QVBoxLayout()

text = QPlainTextEdit()


central = QWidget()
central.setLayout(window_layout)

midi_bar = midi_handling_bar()
file_buttons = file_speific_buttons()
file_list = file_selection_list()

window_layout.addWidget(midi_bar)
window_layout.addWidget(file_buttons, 0)
window_layout.addWidget(file_list)
window_layout.addWidget(text)

window.setCentralWidget(central)
window.resize(600, 450)

file_buttons.save_button.clicked.connect(file_list.save)
file_buttons.save_as_button.clicked.connect(file_list.save_as)

midi_bar.play_button.clicked.connect(lambda: play_piece(str(text.toPlainText())))

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
midi_io.destroy_midi_out()