from socket import *
import threading
import time

global i
i = 0

class ThreadedServer():
    def listenToClient(self, client, addr):
        global i
        while True:
            client.send("Welcome to the quiz \n") #Send first message to client
            authentication = client.recv(1024) #Get authentication input

            client.send("Name - Surname: ")
            m1 = client.recv(1024) #Get name-surname data from user

            name, surname = m1.split() #Split input and keep them in parameters

            client.send("Enter your password: ")
            password = client.recv(1024) #Get password value

            print "Username: ", name
            print "Password: ", password

            file = open("students.txt", "r") #Open students txt file
            str_file = file.read() #Keep it in string.

            if str_file.find(name[i]) != -1: #if you can find username
                if str_file.find(password[i]): #if you can find password
                    
                    client.send("Successfuly Authenticated!.\n") 
                    file2 = open("attendance.txt", "w")	#open the authentication txt file
                    file2.write(name) #write username
                    file2.write(": yes") #if user successfuly authenticated, insert it to attendance txt file
                    file2.close() #close file

                    localtime1 = time.localtime(time.time())[4] #get local minute
                    print "Time->", time.localtime(time.time())[3], ":", time.localtime(time.time())[4] #display time.

                    #Open questions
                    questionFile = open("questions.txt", "r")
                    questions = questionFile.read()
                    questions = [y for y in (x.strip() for x in questions.splitlines()) if y]
                    questionFile.close()

                    #Open answers
                    answerFile = open("answers.txt","r")
                    answers = answerFile.read()
                    answers = [y for y in (x.strip() for x in answers.splitlines()) if y]
                    answerFile.close()

                    #Give +10 scores for each true answers
                    score = 0
                    for number in range(0, len(questions)): 
	                    client.send(questions[number])
	                    answer = client.recv(1024)
	                    if answer.lower() == answers[number]:
	                    	score = score + 10
                    
	                #get localtime minute value again.
                    localtime2 = time.localtime(time.time())[4]
                    #subtract times.
                    timestamp = localtime2 - localtime1
                    #if>30 time is up.
                    if timestamp > 30:
                        print "Your time is up!\n"
                        client.close()
                    #display total score
                    print name, surname, "score", str(score), "bonus",  str(10/(timestamp+1)), "total Score:",str(score + 10/(timestamp+1))
            else:
                client.send("Authentication cannot be completed.\n")

            i = i + 1
            file.close()


    def __init__(self, serverPort, serverName):
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
        except:
            print "Socket cannot be created"
            exit(1)
            #Sockets are the endpoints of a bidirectional communications channel.
        print "Socket is created"
        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print "Socket cannot be used"
            exit(1)
        print "Socket is being used"
        try:
            serverSocket.bind((serverName, serverPort))
        except:
            print "Binding cannot de done"
            exit(1)
        print "Binding is done"
        try:
            serverSocket.listen(45)
        except:
            print "Server cannot listen!"
            exit(1)
        print "Server is ready to receive"

        while True:
            connectionSocket, addr = serverSocket.accept()

            threading.Thread(target=self.listenToClient, args=(connectionSocket, addr)).start()

if __name__ == "__main__":
    serverName = "192.168.236.2"
    serverPort = 12000
    ThreadedServer(serverPort, serverName)

