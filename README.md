# <p align="center">Image Detection</p>

This is an AI model for detecting and recognizing invoice information by yolov5 and OCR.

## Introduction

In Taiwan, companies should enter invoices into the accounting system every month to create financial statements. To solve such a single and highly repetitive matter, we decided to build a robot to automatically identify the information in the invoice and upload it to the accounting system.

There are three main steps in the system which are detecting the coordinates of invoice information, identifying the text in the coordinates, and creating files automatically by the robot. Among them, I am responsible for the first two steps.

I mainly use yolov5 to train the model to circle the coordinates of the invoice message and use the OCR library to get the text in it. However, sometimes the coordinates that yolov5 labeled are cut to numbers or wrapped to borders. To solve this problem, I use the concept of optimization to solve it, and also improve the accuracy rate through ensemble learning.

Finally, we tested 25 invoices and got 96% correct. Comparing the time and accuracy spent by financial personnel in the past, we can find that our system can effectively reduce time costs and human resources for the company.

# <p align="center">Documentation</p>

[Installation](#installition)

[Tutorials](#tutorials)

## Installition

1. Clone this repository.

   ```git
   git clone https://github.com/jyp-studio/Invoice_detection.git
   ```

2. Clone [yolov5](https://github.com/ultralytics/yolov5) respository for trainning models.

   ```git
   git clone https://github.com/ultralytics/yolov5.git
   ```

3. Install related packages for all respositories. There are `requirements.txt` in both my respository and yolov5 respository. That is, you can easily install packages by typing

   ```
   pip install requirements.txt
   ```

   on the terminal.

4. Done!

## Tutorials

run `main.py`.

It will show a friendly graphic user interface for using this system. Click buttons to select the path of input image folder and output result folder. <b>Remind that the input image must be jpg format.</b>

After that, click the start button to start the system. The console will display its states for users to know what is going on clearly.

When the system is done, the result will save to the desination that you set in the beginning as excel. In addition, the system will also show a message box to tell users that which invoice is fail to recognize.
