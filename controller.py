from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QGraphicsScene
from main_gui import Ui_MainWindow
from InvoiceDetection import *
from setting import *
import traceback, sys
import copy
import time

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
            self.signals.result.emit(
                result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Controller(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

        self.threadpool = QThreadPool()

        # error list for recognition fail
        self.error_list = []
        self.indices = []
        self.final = []
        self.final1 = []
        self.final2 = []
        self.final3 = []
        self.final4 = []
        self.final5 = []

        self.time_start = 0
        self.time_end = 0
        self.time_cost = 0

    def setup_control(self):
        self.ui.btnLoad.clicked.connect(self.open_folder)
        # self.ui.btnLoad.clicked.connect(self.draw)
        self.ui.btnSave.clicked.connect(self.select_save_folder)
        self.ui.btnStart.clicked.connect(self.startThread)

    def startThread(self):
        self.time_start = time.time()
        worker1 = Worker(self.recognition_worker_1)
        worker2 = Worker(self.recognition_worker_2)
        worker3 = Worker(self.recognition_worker_3)
        worker4 = Worker(self.recognition_worker_4)
        worker5 = Worker(self.recognition_worker_5)

        worker1.signals.finished.connect(self.compare_and_save)
        worker2.signals.finished.connect(self.compare_and_save)
        worker3.signals.finished.connect(self.compare_and_save)
        worker4.signals.finished.connect(self.compare_and_save)
        worker5.signals.finished.connect(self.compare_and_save)

        self.threadpool.start(worker1)
        self.threadpool.start(worker2)
        self.threadpool.start(worker3)
        self.threadpool.start(worker4)
        self.threadpool.start(worker5)

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
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder",
                                                       "./")
        self.ui.lineEditLoad.setText(folder_path)

    def select_save_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder",
                                                       "./")
        self.ui.lineEditSave.setText(folder_path)

    def recognition_worker_1(self):
        print("w1")
        self.ui.labelConsole.setText("worker1 start running...")
        open_path = self.ui.lineEditLoad.text()
        # save_path = self.ui.lineEditSave.text()
        selected_format = self.ui.comboBoxFormat.currentText()
        format_id = ALL_FORMATS[selected_format]
        model = MODELS_1[selected_format]
        weight = WEIGHTS_1[selected_format]
        name_list = NAME_LIST
        text = "worker1 start running..."
        self.final1 = []
        self.final1 = self.recognition(open_path, model, weight, name_list,
                                       format_id, text)

    def recognition_worker_2(self):
        print("w2")
        self.ui.labelConsole.setText("worker2 start running...")
        open_path = self.ui.lineEditLoad.text()
        # save_path = self.ui.lineEditSave.text()
        selected_format = self.ui.comboBoxFormat.currentText()
        format_id = ALL_FORMATS[selected_format]
        model = MODELS_2[selected_format]
        weight = WEIGHTS_2[selected_format]
        name_list = NAME_LIST
        text = "worker2 start running..."
        self.final2 = []
        self.final2 = self.recognition(open_path, model, weight, name_list,
                                       format_id, text)

    def recognition_worker_3(self):
        print("w3")
        self.ui.labelConsole.setText("worker3 start running...")
        open_path = self.ui.lineEditLoad.text()
        # save_path = self.ui.lineEditSave.text()
        selected_format = self.ui.comboBoxFormat.currentText()
        format_id = ALL_FORMATS[selected_format]
        model = MODELS_3[selected_format]
        weight = WEIGHTS_3[selected_format]
        name_list = NAME_LIST
        text = "worker3 start running..."
        self.final3 = []
        self.final3 = self.recognition(open_path, model, weight, name_list,
                                       format_id, text)

    def recognition_worker_4(self):
        print("w4")
        self.ui.labelConsole.setText("worker4 start running...")
        open_path = self.ui.lineEditLoad.text()
        # save_path = self.ui.lineEditSave.text()
        selected_format = self.ui.comboBoxFormat.currentText()
        format_id = ALL_FORMATS[selected_format]
        model = MODELS_4[selected_format]
        weight = WEIGHTS_4[selected_format]
        name_list = NAME_LIST
        text = "worker4 start running..."
        self.final4 = []
        self.final4 = self.recognition(open_path, model, weight, name_list,
                                       format_id, text)

    def recognition_worker_5(self):
        print("w5")
        self.ui.labelConsole.setText("worker5 start running...")
        open_path = self.ui.lineEditLoad.text()
        # save_path = self.ui.lineEditSave.text()
        selected_format = self.ui.comboBoxFormat.currentText()
        format_id = ALL_FORMATS[selected_format]
        model = MODELS_5[selected_format]
        weight = WEIGHTS_5[selected_format]
        name_list = NAME_LIST
        text = "worker5 start running..."
        self.final5 = []
        self.final5 = self.recognition(open_path, model, weight, name_list,
                                       format_id, text)

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
                self.ui.labelConsole.setText(
                    f"{text} {counter}/{len(all_img)}")
                # print(text)

                # load image and dectect infos' location
                img_path = os.path.join(open_path, img)
                try:
                    image = cv2.imread(img_path)
                    image_info_loc = invoice_det.info_detection(img_path)
                except:
                    continue
                # get name
                name = os.path.basename(img_path)
                if text == "worker1 start running...":
                    self.indices.append(name)
                # image processing
                image_mod = invoice_det.img_contrast(image,
                                                     contrast=100,
                                                     brightness=0)

                # ocr
                result_dict = invoice_det.ocr(image_mod, image_info_loc)

                # print("=========ANSWER==========")
                # for key, value in result_dict.items():
                #    print(f"{key}: {value}")
                # print("=========ANSWER==========")

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
            self.ui.labelConsole.setText("Path not found or Network error")

    def compare_and_save(self):
        isDone = False
        if self.final1 and self.final2 and self.final3 and self.final4 and self.final5:
            isDone = True

        if isDone:
            self.final = self.compare()
            self.time_end = time.time()
            self.time_cost = self.time_end - self.time_start
            print("cost", self.time_cost)
            self.save()

    def compare(self):
        print(self.indices)
        print(self.final1)
        print(self.final2)
        print(self.final3)
        print(self.final4)
        print(self.final5)
        result = copy.deepcopy(self.final1)
        compare_list = []
        for i in range(len(self.final1)):
            for j in range(len(self.final1[i])):
                print(i, j)
                compare_list.append(self.final1[i][j])
                compare_list.append(self.final2[i][j])
                compare_list.append(self.final3[i][j])
                compare_list.append(self.final4[i][j])
                compare_list.append(self.final5[i][j])

                while "" in compare_list:
                    compare_list.remove("")
                most = max(compare_list, key=compare_list.count, default="")
                if most != "":
                    result[i][j] = most
                else:
                    result[i][j] = ""
                    print("error", self.indices[i])
                    if self.indices[j] not in self.error_list:
                        self.error_list.append(self.indices[j])
                compare_list.clear()

        return result

    def save(self):
        save_path = self.ui.lineEditSave.text()
        self.draw()
        save_to_excel(save_path, self.final, COLUMES)
        self.ui.labelConsole.setText("Result saved")

    def __cal(self):
        row_wrong_counter = 0
        counter_80 = 0
        total = len(self.final[0])
        matrix = np.mat(self.final)
        matrix = matrix.T
        matrix = matrix.tolist()
        for i in range(len(matrix)):
            value_wrong_counter = 0
            for j in range(len(matrix[i])):
                if matrix[i][j] == "":
                    value_wrong_counter += 1
            if value_wrong_counter > 0:
                row_wrong_counter += 1
                if value_wrong_counter == 1:
                    counter_80 += 1

        X = []
        LABELS = []
        if total - row_wrong_counter > 0:
            X.append(total - row_wrong_counter)
            LABELS.append("100%")
        if counter_80 > 0:
            X.append(counter_80)
            LABELS.append("80%")
        if row_wrong_counter - counter_80 > 0:
            X.append(row_wrong_counter - counter_80)
            LABELS.append("Fail")

        return X, LABELS

    def draw(self):
        dr = Figure_Canvas()

        X, LABELS = self.__cal()

        dr.axes.pie(
            x=X,
            labels=LABELS,
            radius=1.5,
            startangle=60,
            autopct="%.1f%%",
            textprops={
                "weight": "bold",
                "size": 16
            },
        )

        graphicscene = QGraphicsScene()
        graphicscene.addWidget(dr)
        self.ui.canvas.setScene(graphicscene)
        self.ui.canvas.show()

        self.show_message()

    def show_message(self):
        text = ""
        for txt in self.error_list:
            text += txt + '\n'

        QMessageBox.warning(self, "Warning", f"recognition fail:\n{text}")


# connect pyqt and matplot
class Figure_Canvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=135)
        super(Figure_Canvas, self).__init__(fig)
        # self.setParent(parent)
        self.axes = fig.add_subplot(111)
