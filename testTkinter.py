from tkinter import *
#from PIL import imageTk
from tkinter import messagebox
from AllPackets import *
import socket
from ResurseSO import *

login_info : list = []

OurTopicsAre = ['CPUUsage','CPUFreq']


class Gui:
    ip = 'broker.mqttdashboard.com'

    port = 1883
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    aux = 0


    def __init__(self):
        self.app = Tk()
        self.app.title("MQTT Client")
        self.app.geometry('600x500')




        # Creeaza un socket IPv4, TCP


        self.titlu = Label(self.app,text = "MQTT CLIENT",font=("Arial Bold", 25))
        self.userLabel = Label(self.app,text = "Username :")
        self.passwordLabel = Label(self.app,text = "Password :")


        self.user = Entry(self.app, width=35, borderwidth=5)
        self.password = Entry(self.app, width=35, borderwidth=5)


        self.titlu.grid(column=0 , row = 0)
        self.userLabel.grid(row  = 2, column = 0)
        self.passwordLabel.grid(row  = 3, column = 0)

        self.user.grid(row=2, column=1, columnspan=3, padx=10, pady=10)
        self.password.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

        self.password.config(show = '* ')

        #login button
        self.loginButton =Button(self.app, text = "Connect", command =lambda:self.loginPress())
        self.loginButton.grid(row=3, column=5, )

        #publish button
        self.publishButton = Button(self.app, text="Publish", command=lambda: self.publishPress())
        self.publishButton.grid(row=12, column=0, )

        #subscribe button
        self.subscribeButton = Button(self.app, text="Subscribe", command=lambda: self.subscribePress())
        self.subscribeButton.grid(row=12, column=1,)

        self.app.mainloop()



    def loginPress(self):

        global login_info
        login_info.clear()
        f = open("passwd.txt", "r")
        i=0
        for line in open("passwd.txt", "r").readlines():
            #login_info[i] = line[:-1].split(':')
            login_info.append(line[:-1].split(':'))
            i += 1
            #print(login_info)

        f.close()
                #self.s.send(self.binar(connect_encode))

        print(login_info)

        userAndPwCheck = 0
        if (self.user.get() == "" or self.password.get() == ""):
            userAndPwCheck = -1

       # messagebox.showerror("Error" , "All fields are requiered",parent = self.app)

        for item in login_info:
            if(not (str(self.user.get()) != item[0] or str(self.password.get()) != item[1])):
                userAndPwCheck = 1
                break

        if (userAndPwCheck == 1):
            self.conn = CONNECT()
            # print("merge")
            self.conn.createPacketConnect("primul client", str(self.user.get()), str(self.password.get()), 22,
                                          '0100111', 'hello World',
                                          '/Register')

            connect_encode = self.conn.encode()
            print(self.binar(connect_encode))

            self.s.send(self.binar(connect_encode))
            self.aux=1
        elif userAndPwCheck == -1:
            messagebox.showerror("Error" , "All fields are requiered",parent = self.app)
        else:
            messagebox.showerror("Error", "Wrong parametres", parent=self.app)



        if self.aux == 1:
            self.user.grid_forget()
            self.password.grid_forget()
            self.loginButton.grid_forget()
            self.userLabel.grid_forget()
            self.passwordLabel.grid_forget()

    # publish button


    def publishPress(self):
       pass

    #subscribe button

    def subscribePress(self):
        pass



    def run(self):
        pass

    def binar(self,bin):
        result = bytearray()
        for index in range(0, len(bin), 8):
            result.append(int(bin[index:index + 8], 2))
        return result


app = Gui()



#creating button









