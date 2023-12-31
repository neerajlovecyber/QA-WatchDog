from PySide6 import QtWidgets, QtUiTools, QtCore
import sys
import pymongo
import socket
from resources import nspc
def show_main_window():
    windowmain.showMaximized()


def exitfcn():
    save()
    global project_names  # Access the global project_names variable
    project_names = [] 
    windowmain.close()  # Close the main window
    window.show()  # Show the login window again
    windowmain.projectlabel.setText("No Projects to show")
    windowmain.projectlabel.repaint()
    windowmain.n1.hide()
    windowmain.n2.hide()
    windowmain.n3.hide()
    windowmain.n4.hide()
    windowmain.n1.hide()
    windowmain.n5.hide()
    windowmain.n6.hide()
    windowmain.n7.hide()
    windowmain.n8.hide()
    windowmain.n9.hide()
    windowmain.n10.hide()
    windowmain.n11.hide()
    windowmain.n12.hide()
    windowmain.n13.hide()
    windowmain.n14.hide()
    windowmain.n15.hide()
    windowmain.pbar.hide()
    int_list=[0] * 67 
    set_checkbox_states(checkboxes, int_list)

def update_project_names():
    global currentproject  # Add this line to access the global variable
    user_data = collection.find_one({"username": username})
    if user_data:
        project_names = get_project_names(user_data["data"])
        print("Project names:", project_names)
        
        # Set the project name according to the first project in the list
        first_project_name = project_names[0] if project_names else None
        if first_project_name:
            windowmain.n1.setText(first_project_name)
            windowmain.n1.show()
            int_list = user_data["data"][first_project_name]
            set_checkbox_states(checkboxes, int_list)
            currentproject = first_project_name  # Set the current project to the first project name
            
            n = 1
            for names in project_names:
                label_name = f"n{n}"
                label = getattr(windowmain, label_name)
                label.setText(names)
                label.show()
                n += 1

 


def register_clicked():
    global username, password, collection
    username = window.username.text()
    password = window.password.text()
    data = {"p1": [0]*67}
    register_success, register_msg = register_user(collection, username, password, data)
    print(register_msg)
    if register_success:
        window.close()
        setusername()
        regiterproject()  # Initialize new project registration
        show_main_window()

def login_clicked():
    global username, password, collection, project_names
    username = window.username.text()
    password = window.password.text()

    login_success, login_msg = login_user(collection, username, password)
    print(login_msg)
    if login_success:
        window.close()
        setusername()
        user_data = collection.find_one({"username": username})

        if user_data:
            project_names = get_project_names(user_data["data"])
            print("Project names:", project_names)
            update_project_names() 
            windowmain.projectlabel.setText(currentproject)
            windowmain.projectlabel.repaint() # Initialize project names
        show_main_window()

            
def get_project_names(data):
    # Extract the keys from the "data" dictionary to get the project names
    project_names = list(data.keys())
    return project_names

def checkboxcheck():
    checkboxlist = []
    for a in range(1, 68):
        checkbox_name = f"c{a}"
        checkbox = getattr(windowmain, checkbox_name, None)
        
        if checkbox is not None and isinstance(checkbox, checkbox.__class__):
            if checkbox.isChecked():
                checkboxlist.append(1)
            else:
                checkboxlist.append(0)
    print(checkboxlist)
    return checkboxlist
 

# Set the checkbox states based on the list of integers
def set_checkbox_states(checkboxes, int_list):
    if len(checkboxes) != len(int_list):
        raise ValueError("The number of checkboxes and the length of the integer list must be the same.")
    
    for checkbox, value in zip(checkboxes, int_list):
        if isinstance(checkbox, checkbox.__class__):
            checkbox.setChecked(bool(value))
        else:
            raise ValueError("Input list should only contain PySide6 QCheckBox objects.")


def connect_to_mongodb():
    global collection  # Make 'collection' a global variable so you can use it outside this function
    try:
        # Attempt to establish a connection to the MongoDB database
        client = pymongo.MongoClient("mongodb+srv://neerajlovecyber:gamersnsp@rdtdb.grubyrx.mongodb.net/?retryWrites=true&w=majority")
        db = client["records"]
        collection = db["records"]

        window.logmsg.setText("Connected to MongoDB and internet")
        print("Connected to MongoDB")
        return collection
    except pymongo.errors.ConnectionFailure:
        window.logmsg.setText("Failed to connect to MongoDB. Please check your internet connection.")
        print("Failed to connect to MongoDB. Please check your internet connection.")
    except socket.gaierror:
        window.logmsg.setText("Failed to resolve host. Please check your internet connection and host name.")
        print("Failed to resolve host. Please check your internet connection and host name.")
    return None



def register_user(collection, username, password, data):
    # Check if the username is already taken
    global currentproject
    if collection.find_one({"username": username}):
        window.logmsg.setText("Username already taken")
        currentproject = windowmain.newpname.text()

        return False, "Username already taken"

    # Insert user data into the collection
    collection.insert_one({
        "username": username,
        "password": password,
        "data": data
    })
    window.logmsg.setText("Registration successful")
    return True, "Registration successful"

def login_user(collection, username, password):
    # Find the user by username
    user = collection.find_one({"username": username})
    if user:
        # Check if the provided password matches
        if user["password"] == password:
            window.logmsg.setText("Login Successful")
            return True, "Login successful"
            
        else:
            window.logmsg.setText("Invalid password")
            return False, "Invalid password"

    else:
        return False, "User not found"
def setusername():
    windowmain.usernamefield.setText("Hello, "+username)
def regiterproject():
    windowmain.pbar.show()
    global currentproject
    def hidebtn():
        global username  # Access the global username variable
        projectname = windowmain.newpname.text()
        
        # Update the project name in the data dictionary
        user_data = collection.find_one({"username": username})
        if user_data:
            data = user_data["data"]
            if "p1" in data:
                new_data = {projectname: data["p1"]}
                data.pop("p1")
                
                # Delete the "p1" key from the MongoDB document
                collection.update_one({"username": username}, {"$unset": {"data.p1": 1}})
                
                # Update the MongoDB document with the new project name and data
                collection.update_one({"username": username}, {"$set": {"data": new_data}})
                global currentproject
                currentproject=windowmain.newpname.text()
                set_checkbox_states(checkboxes, new_data[projectname])  # Set checkbox states for the updated project
                currentproject=windowmain.newpname.text()
                windowmain.n1.setText(projectname) 
                windowmain.n1.show()
                windowmain.pbar.hide()

    windowmain.newpbtn.clicked.connect(hidebtn)    



def addnewproject():
    global currentproject  # Access the global currentproject variable
    print("Adding a new project")
    windowmain.pbar.show()
    # Check the number of existing projects
    user_data = collection.find_one({"username": username})
    if user_data:
        total_projects = len(user_data.get("data", {}))
        if total_projects >= 14:
            print("Maximum projects limit reached (15)")
            windowmain.projectlabel.setText("Max projects limit reached")
            windowmain.projectlabel.repaint()
            windowmain.pbar.hide()
            return
    
     

    def hidebtn():
        global currentproject  # Access the global currentproject variable
        user_data = collection.find_one({"username": username})
        if user_data:
            total_projects = len(user_data.get("data", {}))
            print("Total projects:", total_projects)
            total_projects = total_projects + 1
            
            projectname = windowmain.newpname.text()            
            label_name = f"n{total_projects}"
        
            currentproject = projectname 
            print(currentproject) # Update the current project name
            windowmain.projectlabel.setText(currentproject)
            windowmain.projectlabel.repaint()
            # Set checkbox values to 0 for the new project
            new_project_data = [0] * 67  # Initialize with 67 zeros
            set_checkbox_states(checkboxes, new_project_data)
                
            # Trigger layout update            
            windowmain.layout().update()
                
            # Update the database with the new project data
            update_query = {"username": username}
            update_data = {"$set": {f"data.{projectname}": new_project_data}}
            collection.update_one(update_query, update_data)
                
            windowmain.pbar.hide()
            update_project_names()
            projectname = windowmain.newpname.text()   
            currentproject=projectname
            print(currentproject)
            set_checkbox_states(checkboxes,new_project_data) 
    windowmain.newpbtn.clicked.connect(hidebtn)

def project_menu(btn):
    global currentproject
    global project_names
    print("pmenu")
    user_data = collection.find_one({"username": username})
    if user_data:
        project_names = get_project_names(user_data["data"])
        print("Project names:", project_names)
    name=project_names[btn-1]
    currentproject=name
    user_data = collection.find_one({"username": username})
    int_list = user_data["data"][name]
    set_checkbox_states(checkboxes, int_list)
    windowmain.projectlabel.setText(currentproject)
    windowmain.projectlabel.repaint()
    

def save():
    global currentproject  # Access the global currentproject variable
    checkbox_values = checkboxcheck()
    
    if collection is not None and currentproject:
        try:
            query = {"username": username, "password": password}
            update = {"$set": {f"data.{currentproject}": checkbox_values}}  # Use the current project name in the update query
            collection.update_one(query, update)
            print(f"Data for project '{currentproject}' updated successfully")
        except Exception as e:
            print("Error updating data:", str(e))
    else:
        print("Not connected to MongoDB or no current project selected")


    

if __name__ == "__main__":
    print("Program start.")
    username = ""
    password = ""
    project_names = []
    currentproject=""
    app = QtWidgets.QApplication([])  # Create the application instance
    
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(".\\resources\\new.ui")
    ui_file.open(QtCore.QFile.ReadOnly)
    windowmain = loader.load(ui_file)
    ui_file.close()

    if windowmain is None:
        print("Failed to load UI file.")
        sys.exit(1)
    
    window = loader.load(".\\resources\\loginpage.ui", None)
    window.show()
    
    checkboxes = [getattr(windowmain, f"c{a}", None) for a in range(1, 68)]
    windowmain.n2.hide()
    windowmain.n3.hide()
    windowmain.n4.hide()
    windowmain.n1.hide()
    windowmain.n5.hide()
    windowmain.n6.hide()
    windowmain.n7.hide()
    windowmain.n8.hide()
    windowmain.n9.hide()
    windowmain.n10.hide()
    windowmain.n11.hide()
    windowmain.n12.hide()
    windowmain.n13.hide()
    windowmain.n14.hide()
    windowmain.n15.hide()
    windowmain.pbar.hide()
    #windowmain.main_body.setEnabled(False)
    collection = connect_to_mongodb()
    if collection is not None:
        print("Connected to MongoDB")

        window.registerbtn.clicked.connect(register_clicked)
        window.loginbtn.clicked.connect(login_clicked)

        
        window.registerbtn.clicked.connect(register_clicked)
        window.loginbtn.clicked.connect(login_clicked)
        windowmain.savebtn.clicked.connect(save)
        windowmain.newbtn.clicked.connect(addnewproject)
################################3
        windowmain.n1.clicked.connect(lambda: project_menu(1))
        windowmain.n2.clicked.connect(lambda: project_menu(2))
        windowmain.n3.clicked.connect(lambda: project_menu(3))
        windowmain.n4.clicked.connect(lambda: project_menu(4))
        windowmain.n5.clicked.connect(lambda: project_menu(5))
        windowmain.n6.clicked.connect(lambda: project_menu(6))
        windowmain.n7.clicked.connect(lambda: project_menu(7))
        windowmain.n8.clicked.connect(lambda: project_menu(8))
        windowmain.n9.clicked.connect(lambda: project_menu(9))
        windowmain.n10.clicked.connect(lambda: project_menu(10))
        windowmain.n11.clicked.connect(lambda: project_menu(11))
        windowmain.n12.clicked.connect(lambda: project_menu(12))
        windowmain.n13.clicked.connect(lambda: project_menu(13))
        windowmain.n14.clicked.connect(lambda: project_menu(14))
        windowmain.n15.clicked.connect(lambda: project_menu(15))
        windowmain.next1.clicked.connect(lambda: windowmain.stackedWidget.setCurrentWidget(windowmain.page2))
        windowmain.next2.clicked.connect(lambda: windowmain.stackedWidget.setCurrentWidget(windowmain.page1))
        windowmain.logout.clicked.connect(exitfcn)

      #############333333333
        
        sys.exit(app.exec_())
    else:
        print("Exiting due to connection error.")