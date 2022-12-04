# <center>Image Detection</center>

This is an AI model for detecting and recognizing invoice information by yolov5 and OCR.

In Taiwan, companies should enter invoices into the accounting system every month to create financial statements. To solve such a single and highly repetitive matter, we decided to build a robot to automatically identify the information in the invoice and upload it to the accounting system.

There are three main steps in the system which are detecting the coordinates of invoice information, identifying the text in the coordinates, and creating files automatically by the robot. Among them, I am responsible for the first two steps.

I mainly use yolov5 to train the model to circle the coordinates of the invoice message and use the OCR library to get the text in it. However, sometimes the coordinates that yolov5 labeled are cut to numbers or wrapped to borders. To solve this problem, I use the concept of optimization to solve it, and also improve the accuracy rate through ensemble learning.

Finally, we tested 25 invoices and got 96% correct. Comparing the time and accuracy spent by financial personnel in the past, we can find that our system can effectively reduce time costs and human resources for the company.

# <center>Documentation</center>

[Installation]("Installation")

[Tutorials]("Tutorials")

## Installition

1. clone the repository.
