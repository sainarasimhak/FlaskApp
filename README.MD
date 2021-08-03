# IS 601 Final Project
The goal of this project is to create a flask application that is based on the tutorial found [here](https://hackersandslackers.com/your-first-flask-application).  The scope and data for the project is based on an earlier project, [located here](https://github.com/sainarasimhak/Project3).  The data from that project was modified to follow with the instructions in the tutorial mentioned in the above link.

# Running the Project
This project runs using Docker.  You will need to have Docker installed on your local machine in order for this to run.  You can download and install docker [here](https://www.docker.com/products/docker-desktop).

## To run the project using the command line:
These are instructions on how to run the project:

1. Clone the GitHub repo located [here](https://github.com/sainarasimhak/FlaskApp) to a directory on your local machine, preferably a new directory.  Use the command "git clone https://github.com/sainarasimhak/FlaskApp" (without the quotes).
2. Change into the directory that you just created the project in, using the command line
3. Run the command "docker-compose build" without the quotation marks.  Wait until the services finish building; it shouldn't take longer than a couple minutes.
4. Once the build is done, run the command "docker-compose up" to bring up the services.  Again, this should take about a minute.
5. Open a browser, and go to localhost:5000.  This will open the project, and you will be able to view it.  Note that in order to edit, add or delete records, you will need to be logged in.  Create an account at the top of the page, and then log in. 
6. When you are done, run "docker-compose down".  This will stop all the containers and remove the images.  Note that you may have to hit "Ctrl + C" on the keyboard in order to type anything on the command line.  Alternatively, you could open a new window or tab in the command line, or another CLI interface of your choice.  Personally, I use Windows Terminal, but there is also Terminal if you are using a Mac, or Windows PowerShell if you are on Windows.

Note - I have add all the steps followed with the respective commit message since i havent created a branch for every individual step
