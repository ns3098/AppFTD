# AppFTD (Application for Tabular Data)



AppFTD is an application to work with tabular data(without internet connection).


# Features!

  - Upload xlsx or csv file for each module.
  - Modify Uploaded data and perform operations like editing, resetting, deleting
  adding extra rows(above or below selected rows).
 - Data Validation(required validators are added).
 - Data Downloading in txt format in the chosen directory.
 - Option to change Opacity of the application (added for better look).
 - Beautiful and clean looking UI.


> The aim of the application is to develop a beautiful and modern
> looking UI unlike most of the naive application developed in PyQt.
> It might contains some bugs although all possible erros has been
> taken care of. Do not forget to send feedbacks and bugs issues.



### Tech

AppFTD uses these tools to work properly:

* [Python 3](https://www.python.org/)
* [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)



### Installation

AppFTD requires [Python 3](https://www.python.org/) to run. Make sure it is already installed.

1. Download the zip file and extract it in a directory.

2. Install all the required dependencies.
```sh
$ pip install -r requirements.txt
```
3. Run the AppFTD python file (be sure to stay in the same directory).
```sh
$ python AppFTD.py
```

### Some Important Instructions

1. Select a single or multiple rows and right click on the vertical header for various options
   like adding rows(above or below), clearing all the values of selected rows, clearing the table or
   deleting selected rows.

2. To edit the value of a cell double click on it and start editing. To reset the whole value of the cell
   select the cell with a single click and type in the new value. Just like Google Spreadsheet.

3. Always Validate the data before downloading.

4. If you want to close the program directly without minimizing it to system tray, make sure to uncheck
   the option 'Minimize to system tray when program is closed' option from Settings.

5. On bottom left side of the application there are 2 buttons. 1st is just for styling purpose. 2nd button
   is used to control opacity of the application. Give it a try once.

6. If due to any exceptions program crashes. Don't forget to check out the log file situated in logs
   directory.

7. Make sure to check out all the demo video and download executable file.


### TODO (If required)

1. To add Search functionality.

2. Adding various data filter options.


> Modules for above options are ready and will be added according to
  user need and requirements.
