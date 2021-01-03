**Name**

Next Generation Clothing Finder

**Description**

This product is a one-stop shop that gathers data from popular clothing sites and presents the products to its users in a way that is convenient to the users. From predefined clothing categories, the user is able to select the gender and subcategories to display the results. The user can also sort the results by name, price, sale price, store and brand, in both ascending and descending order. If the user wishes to add certain products into a favorites list, each product has an “add to favorites” button that, when pressed, will add the item to a favorites list, which can be accessed in the menu bar. Finally, the user can give feedback to the developers. 

_List of Features_

    - A sorting feature (Can sort alphabetically, by price, and by brand. Also included reverse sorting.)
    - A search engine that takes in three parameters (Gender, Category, Subcategory), and returns all data that matches.
    - An image for each result that can be clicked to be brought right to the item's website.
    - Users can send feedback to our group email.
    - Users can add and remove items from list of favorites.

_List of Websites_

    - Nike
    - Arc'teryx
    - H&M
    - Billabong
    - Bluenotes

**Requirements and Installation**

(This was created in the PyCharm IDE, with Python 3.4 or higher)

Ensure that you have Python version 3.x and the following modules installed via the following commands.

For help with installing pip: visit [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

Download our source files here: [https://git.cs.usask.ca/CMPT370-01-2020/group6](https://git.cs.usask.ca/CMPT370-01-2020/group6)

Or if you are familiar with cloning (Using PyCharm for this example): 

    Step 1: Start a new project in PyCharm and click on VCS --> Get from Version Control.
    Step 2: Enter the following url: https://git.cs.usask.ca/CMPT370-01-2020/group6.git and hit clone.
    Step 3: Make sure you have a python interpreter selected, (Python 3.6 or above recommended.)
    Step 3: Enter this command into the terminal to install all required modules "pip install -r requirements.txt"
    Step 4: You can now run our program by simply running the main_GUI file in the group 6 directory.

_Required Modules_

    You should be able to install all modules using this command.
    "pip install -r requirements.txt"

    pip install pytest ---- if this doesn't work, then try "pip install -U pytest"
    pip install bs4
    pip install requests
    pip install helium
    pip install lxml
    pip install tkinter
    pip install Pillow 
    pip install smtplib
    pip install pygdrive3
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    pip install io
    pip install os
    pip install csv
    pip install shutil

**Setting up the Project**
- If you downloaded our source folder, open the folder with an IDE or coding program.
- With PyCharm, create a new project with the source folder as the project.

**Running**

The actual running of our program starts from the main_GUI file. Run the main_GUI file to open the search screen and start.
Please ensure that your default browser is set to Chrome, Opera, or Firefox. Microsoft Edge and Internet Explorer add additional characters to the url when opening links associated with products and the webpage will not be opened correctly.

**Tests**
- Go to the terminal, and enter pytest to run our test suite.
- The program should run the tests for you automatically, showing which tests succeeded and which tests failed. 

**Authors and Acknowledgement**

_List of Developers_

    Jeffery Xie
    Ana-Pietje Du Plessis
    Henry Nguyen
    Enhan Zhao
    Manaf Bargash

**Demo**

_Search Screen_

![Search Screen](https://media.discordapp.net/attachments/770779709172613122/785655849787326474/unknown.png)

_Results Screen_

![Results Screen](https://media.discordapp.net/attachments/770779709172613122/785656004582440980/unknown.png)

_Sorting Options_

![Sorting Options](https://media.discordapp.net/attachments/770779709172613122/785656110190166046/unknown.png)

_Favorites Screen_

![Favorites Screen](https://media.discordapp.net/attachments/770779709172613122/785656348141420584/unknown.png)

_Feedback Screen_

![Feedback Screen](https://media.discordapp.net/attachments/770779709172613122/785656403208962058/unknown.png)