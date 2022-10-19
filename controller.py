from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from main_gui import Ui_MainWindow
from InvoiceDetection import *
from setting import *
import traceback, sys


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
        print(
            "Multithreading with maximum %d threads" % self.threadpool.maxThreadCount()
        )

    def setup_control(self):
        self.ui.btnLoad.clicked.connect(self.open_folder)
        self.ui.btnSave.clicked.connect(self.select_save_folder)
        self.ui.btnStart.clicked.connect(self.startThread)

    def startThread(self):
        self.btnEnable(False)
        worker = Worker(self.recognition)
        worker.signals.finished.connect(self.thread_complete)

        self.threadpool.start(worker)

    def thread_complete(self):
        self.btnEnable(True)

    def btnEnable(self, state):
        self.ui.btnLoad.setEnabled = state
        self.ui.btnSave.setEnabled = state
        self.ui.btnStart.setEnabled = state
        self.ui.lineEditLoad.setEnabled = state
        self.ui.lineEditSave.setEnabled = state
        self.ui.comboBoxFormat.setEnabled = state

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder", "./")
        self.ui.lineEditLoad.setText(folder_path)

    def select_save_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder", "./")
        self.ui.lineEditSave.setText(folder_path)

    def recognition(self):
        self.ui.labelConsole.setText("start running...")
        open_path = self.ui.lineEditLoad.text()
        save_path = self.ui.lineEditSave.text()
        # try:
        selected_format = self.ui.comboBoxFormat.currentText()
        print(selected_format)
        model = ALL_MODELS[selected_format]
        print(model)
        weight = ALL_WEIGHTS[selected_format]
        print(weight)
        name_list = NAME_LIST

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
        FORMAT_ID = 25

        counter = 0
        all_img = os.listdir(open_path)
        for img in all_img:

            # load image and dectect infos' location
            img_path = os.path.join(open_path, img)
            print(img_path)
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
            format_id.append(FORMAT_ID)
            try:
                untaxed.append(int(result_dict["untaxed"]))
            except:
                untaxed.append(result_dict["untaxed"])

            counter += 1
            self.ui.labelConsole.setText(f"start running... {counter}/{len(all_img)}")

        # save to excel
        final = [years, months, dates, id, invoice_num, format_id, untaxed]
        invoice_det.save(save_path, final, COLUMES)
        self.ui.labelConsole.setText("Done")
        # except:
        #     print("error")
