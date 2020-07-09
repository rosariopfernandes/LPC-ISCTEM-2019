# Java to Pascal Pre-Processor

This is a college project I built to learn more about Compilers.
It takes Java code and converts it to Pascal. It only takes in consideration:
- Primitive variable declarations (both local and global) (eg. `int counter;`).
- value attribution (eg. `counter = 0;`).
- `if` and `while` structures.
- primitive type methods (`void` included).

This project has 3 components:
- **The Web UI** - a simple user interface written in HTML, CSS and JS. It's located
 on the [web folder](https://github.com/rosariopfernandes/LPC-ISCTEM-2019/tree/master/web). 
- **The flask server** - the server that actually does all the processing operations. It's located
 on the root folder of the projects and also includes the [converters](https://github.com/rosariopfernandes/LPC-ISCTEM-2019/tree/master/converters)
 and [models](https://github.com/rosariopfernandes/LPC-ISCTEM-2019/tree/master/models) folders.
- **The Parser** - a [jar file](https://github.com/rosariopfernandes/LPC-ISCTEM-2019/blob/master/AnalisadorJava.jar) 
 created using the [Java cup library](http://www2.cs.tum.edu/projects/cup/).
 
 
There's also a `java_files` folder where you can find examples of files that can
 be parsed by the pre-processor.

## Getting Started

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes.

### Prerequisites

The project was built using python3, so you'll need to install it.
See [Python downloads](https://www.python.org/downloads/) for instructions.

### Installing

1. Clone the project to your local machine:

    ```bash
    git clone https://github.com/rosariopfernandes/LPC-ISCTEM-2019
    cd LPC-ISCTEM-2019
    ```

1. Install the dependencies locally:

    ```bash
    pip install prettytable
    pip install flask
    ```

1. Run the server:

    ```bash
    python3 __init__.py
    ```
    
    Make sure it's running on `https://127.0.0.1/5000`. 

1. Run the web server using any static server program.
 I particularly like [Web Server for Chrome](https://chrome.google.com/webstore/detail/web-server-for-chrome/ofhbbkphhbklhfoeikjpcbhemlocgigb)
 because it provides a user interface.

1. Open the web server url on the browser.
    
    Because chrome blocks Same-Origin Requests, you might want you disable chrome security:
    ```bash
    chromium-browser --disable-web-security --user-data-dir="[SOME_DIRECTORY]"
    ``` 
    Replace [SOME_DIRECTORY] with a directory you have created on your local machine.
    Chrome will be storing your user data there.
