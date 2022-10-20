from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from main_gui import Ui_MainWindow
from InvoiceDetection import *
from setting import *
import traceback, sys
import copy

import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

        self.threadpool = QThreadPool()

        self.final = []
        self.final1 = []
        self.final1_done = False
        self.final2 = []
        self.final2_done = False

    def setup_control(self):
        self.ui.btnLoad.clicked.connect(self.open_folder)
        # self.ui.btnLoad.clicked.connect(self.draw)
        self.ui.btnSave.clicked.connect(self.select_save_folder)
        self.ui.btnStart.clicked.connect(self.startThread)

    def startThread(self):
        worker1 = Worker(self.recognition_init)
        # worker1.signals.finished.connect(self.verifyThread)
        worker1.signals.finished.connect(self.compare_and_save)
        worker2 = Worker(self.recognition_verify)
        worker2.signals.finished.connect(self.compare_and_save)
        self.threadpool.start(worker2)
        self.threadpool.start(worker1)

    def verifyThread(self):
        worker2 = Worker(self.recognition_verify)
        worker2.signals.finished.connect(self.compare_and_save)
        self.threadpool.start(worker2)

    def thread_complete(self):
        self.btnEnable(True)

    def btnEnable(self, state):
        self.ui.btnLoad.setEnabled = state
        self.ui.btnSave.setEnabled = state
        self.ui.btnStart.setEnabled = state
        self.ui.lineEditLoad.setEnabled = state
        self.ui.lineEditSave.setEnabled = state
        self.ui.comboBoxFormat.setEnabled = state

    def btnDisable(self):
        self.ui.btnLoad.setEnabled = False
        self.ui.btnSave.setEnabled = False
        self.ui.btnStart.setEnabled = False
        self.ui.lineEditLoad.setEnabled = False
        self.ui.lineEditSave.setEnabled = False
        self.ui.comboBoxFormat.setEnabled = False

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder", "./")
        self.ui.lineEditLoad.setText(folder_path)

    def select_save_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder", "./")
        self.ui.lineEditSave.setText(folder_path)

    def recognition_init(self):
        self.ui.labelConsole.setText("start running...")
        open_path = self.ui.lineEditLoad.text()
        # save_path = self.ui.lineEditSave.text()
        selected_format = self.ui.comboBoxFormat.currentText()
        format_id = ALL_FORMATS[selected_format]
        model = ALL_MODELS[selected_format]
        weight = ALL_WEIGHTS[selected_format]
        name_list = NAME_LIST
        text = "start running..."
        self.final1 = []
        self.final1 = self.recognition(
            open_path, model, weight, name_list, format_id, text
        )

    def recognition_verify(self):
        self.ui.labelConsole.setText("verifying...")
        open_path = self.ui.lineEditLoad.text()
        # save_path = self.ui.lineEditSave.text()
        selected_format = self.ui.comboBoxFormat.currentText()
        format_id = ALL_FORMATS[selected_format]
        model = VERIFY_MODELS[selected_format]
        weight = VERIFY_WEIGHTS[selected_format]
        name_list = NAME_LIST
        text = "verifying..."
        self.final2 = []
        self.final2 = self.recognition(
            open_path, model, weight, name_list, format_id, text
        )

    def recognition(self, open_path, model, weight, name_list, format, text):
        try:
            # set up model
            invoice_det = InvoiceDetection(model, weight, name_list)

            # set up final results
            years = []
            months = []
            dates = []
            id = []
            invoice_num = []
            format_id = []
            untaxed = []

            counter = 1
            all_img = os.listdir(open_path)
            for img in all_img:
                self.ui.labelConsole.setText(f"{text} {counter}/{len(all_img)}")

                # load image and dectect infos' location
                img_path = os.path.join(open_path, img)
                try:
                    image = cv2.imread(img_path)
                    image_info_loc = invoice_det.info_detection(img_path)
                except:
                    continue
                # image processing
                image_mod = invoice_det.img_contrast(image, contrast=100, brightness=0)

                # ocr
                result_dict = invoice_det.ocr(image_mod, image_info_loc)

                print("=========ANSWER==========")
                for key, value in result_dict.items():
                    print(f"{key}: {value}")
                print("=========ANSWER==========")

                # append to final list
                try:
                    year = int(result_dict["date"][:4])
                except:
                    year = ""
                try:
                    month = int(result_dict["date"][4:6])
                except:
                    month = ""
                try:
                    day = int(result_dict["date"][6:8])
                except:
                    day = ""
                years.append(year)
                months.append(month)
                if year != "" and month != "" and day != "":
                    dates.append(f"{year}/{month}/{day}")
                else:
                    dates.append("")
                try:
                    id.append(int(result_dict["id"]))
                except:
                    id.append("")
                invoice_num.append(result_dict["invoice_number"])
                format_id.append(format)
                try:
                    untaxed.append(int(result_dict["untaxed"]))
                except:
                    untaxed.append(result_dict["untaxed"])

                counter += 1

            # save to excel
            final = [years, months, dates, id, invoice_num, format_id, untaxed]
            return final
        except:
            self.ui.labelConsole.setText("Path not found")

    def compare_and_save(self):
        if len(self.final1) > 0 and len(self.final2) > 0:
            self.final = self.compare()
            self.save()

    def compare(self):
        result = copy.deepcopy(self.final1)
        for i in range(len(self.final1)):
            for j in range(len(self.final1[i])):
                if self.final1[i][j] == "":
                    result[i][j] = self.final2[i][j]
        return result

    def save(self):
        save_path = self.ui.lineEditSave.text()
        self.draw()
        save_to_excel(save_path, self.final, COLUMES)
        self.ui.labelConsole.setText("Result saved")

    def draw(self):
        dr = Figure_Canvas()
        dr.draw_pie(self.final)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.ui.canvas.setScene(graphicscene)
        self.ui.canvas.show()


# connect pyqt and matplot
class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=135)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.axes = fig.add_subplot(111)

    def draw_pie(self, final):
        counter = 0
        total = len(final[0])
        matrix = np.mat(final)
        matrix = matrix.T
        matrix = matrix.tolist()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == "":
                    counter += 1
                    break

        # draw
        self.axes.pie(
            x=[total - counter, counter],
            labels=["100%", "Fail"],
            radius=1.5,
            startangle=60,
            autopct="%.1f%%",
            textprops={"weight": "bold", "size": 16},
        )
