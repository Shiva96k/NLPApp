from tkinter import *
from tkinter import messagebox

from PIL.ImageOps import expand

import mydb
import requests

class NLPApp :

    def __init__(self):
        self.root = Tk()
        self.dbo = mydb.Database()


        self.root.title("NLPApp")
        self.root.geometry("400x700")
        self.root.configure(bg = "#34495E")
        self.login()
        self.root.mainloop()


    def login(self):
        self.clear()
        heading = Label( self.root , text = "NLPApp" , bg ="#34495E")
        heading.configure(font=("verdana", 26 , "bold"))
        heading.pack(pady = (40 , 30))

        sub_heading = Label(self.root, text="User Login", bg="#34495E" )
        sub_heading.configure(font=("verdana", 18, "bold"), fg= "#3498DB")
        sub_heading.pack(pady=(20, 10))

        label1 = Label(self.root, text = "Enter email", bg= 'white')
        label1.pack(pady = (10, 10))

        self.email_input = Entry(self.root , width= 50)
        self.email_input.pack(pady = (10, 10) , ipady = 5)

        label2 = Label(self.root, text = "Enter password", bg = "white")
        label2.pack(pady = (10, 10))

        self.password_input = Entry(self.root, width = 50 , show= "*")
        self.password_input.pack(pady = (10, 10), ipady = 5)

        login_button = Button(self.root, text = "Login", command= self.login_process)
        login_button.pack(pady = (10, 10))

        label3 = Label(self.root, text = "Not a Member?" , bg ="#34495E" , fg= "green" , font=("arial", 14) )
        label3.pack(pady = (10, 10))

        register_button = Button(self.root, text= "Register" , bg = "white" , command= self.register_gui)
        register_button.pack(pady = (10, 10))

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def register_gui(self):
        self.clear()

        heading = Label(self.root, text="NLPApp", bg="#34495E")
        heading.configure(font=("verdana", 26, "bold"))
        heading.pack(pady=(40, 30))

        sub_heading = Label(self.root, text="Register Here", bg="#34495E")
        sub_heading.configure(font=("verdana", 18, "bold"), fg="#8E44AD")
        sub_heading.pack(pady=(20, 10))

        label1 = Label(self.root, text="Enter name", bg='white')
        label1.pack(pady=(10, 10))

        self.name_input = Entry(self.root, width=50)
        self.name_input.pack(pady=(10, 10), ipady=5)

        label1 = Label(self.root, text="Enter email", bg='white')
        label1.pack(pady=(10, 10))

        self.email_input = Entry(self.root, width=50)
        self.email_input.pack(pady=(10, 10), ipady=5)

        label2 = Label(self.root, text="Enter password", bg="white")
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50, show="*")
        self.password_input.pack(pady=(10, 10), ipady=5)

        submit_button = Button(self.root, text="Submit", command = self.process_registration)
        submit_button.pack(pady=(10, 10))

        label3 = Label(self.root, text="Already a Member?", bg="#34495E", fg="green", font=("arial", 14))
        label3.pack(pady=(10, 10))

        login_button = Button(self.root, text="Login", bg="white" , command= self.login)
        login_button.pack(pady=(10, 10))

    def process_registration(self):
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.add_data(name, email, password)

        if response:
            messagebox.showinfo("Success" , "Registration Successful. You can login Now")
        else:
            messagebox.showerror("Error", "Email already exists")
        self.login()


    def login_process(self):
        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.search(email, password)

        if response :
            messagebox.showinfo("Success" , "Login Successful")
            self.homepage()
        else:
            messagebox.showerror("Error", "Incorrect Password or email")
            self.login()


    def homepage(self):
        self.clear()

        heading = Label(self.root, text="NLPApp", bg="#34495E")
        heading.configure(font=("verdana", 26, "bold"))
        heading.pack(pady=(40, 30))

        sentiment = Button(self.root, text= "Sentiment analysis" , height= 5 , width= 30, command= self.sentiment_analysis)
        sentiment.pack(pady = (30, 20))

        summery = Button(self.root , text= "Summerization", height= 5 , width= 30, command=self.summerization)
        summery.pack(pady=(20 , 20))

        imagegeneration = Button(self.root, text= "Image Generation", height= 5 , width= 30 , command=self.imagegeneration)
        imagegeneration.pack(pady = (20, 20))

    def sentiment_analysis(self):
        self.clear()

        heading = Label(self.root, text="NLPApp", bg="#34495E")
        heading.configure(font=("verdana", 26, "bold"))
        heading.pack(pady=(30, 20))

        sub_lebel = Label(self.root, text="Sentiment Analysis", bg="#34495E")
        sub_lebel.configure(font=("verdana", 26, "bold"))
        sub_lebel.pack(pady=(30, 20))

        label1 = Label(self.root , text= "Enter text" , bg="white")
        label1.configure(font= ("verdana", 14))
        label1.pack(pady = (10 , 10))

        self.input_text = Entry(self.root, width= 70)
        self.input_text.pack(pady = (10,10), ipady = 10)

        sentiment_analysis_button = Button(self.root, text="Analyse Sentiment" , height= 2 , width=20 , command= self.do_sentiment_analysis)
        sentiment_analysis_button.pack(pady = (10, 10))

        self.sentiment_result = Label(self.root, text= "")
        self.sentiment_result.configure(font=("verdana", 18))
        self.sentiment_result.pack(pady=(10,10))

        Go_back = Button(self.root, text= "Go Back", height= 2 , width = 15 , command= self.homepage)
        Go_back.pack(pady=(30,10))


    def do_sentiment_analysis(self):

        input_para_text = self.input_text.get()

        API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        payload = {"inputs" : input_para_text,}
        response = query(payload)

        label_mapping = {
            "LABEL_0" : "Negative",
            "LABEL_1" : "Neutral" ,
            "LABEL_2" : "Positive"
        }
        txt = ""
        for i in response[0]:
            txt = txt + label_mapping[i['label']] + " ---> " + str(round(i["score"] * 100 , 2)) + "%" + "\n"

        self.sentiment_result["text"] = txt

    def summerization(self):

        self.clear()

        heading = Label(self.root, text="NLPApp", bg="#34495E")
        heading.configure(font=("verdana", 26, "bold"))
        heading.pack(pady=(30, 20))

        sub_lebel = Label(self.root, text="Summerization", bg="#34495E")
        sub_lebel.configure(font=("verdana", 26, "bold"))
        sub_lebel.pack(pady=(30, 20))

        label1 = Label(self.root, text="Enter paragraph", bg="white")
        label1.configure(font=("verdana", 14))
        label1.pack(pady=(10, 10))

        self.input_para = Entry(self.root, width=70)
        self.input_para.pack(pady=(10, 10), ipady=10)

        summerization_button = Button(self.root, text="Get Summery", height=2, width=20,command=self.do_summerization)
        summerization_button.pack(pady=(10, 10))

        self.summary_result = Label(self.root, text="")
        self.summary_result.configure(font=("verdana", 12))
        self.summary_result.pack(pady=(10, 10))

        Go_back = Button(self.root, text="Go Back", height=2, width=15, command=self.homepage)
        Go_back.pack(pady=(30, 10))

    def do_summerization(self):

        input_paragraph = self.input_para.get()

        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        payload = {"inputs" : input_paragraph,}
        response = query(payload)

        words = response[0]["summary_text"].split()
        print(words)
        k = 0
        txt = ""
        for word in words:
            if k % 12 == 0:
                txt = txt + "\n"
                k += 1
            else:
                txt = txt + " " + word
                k += 1
        print(txt)
        self.summary_result["text"] = txt

    # def imagegeneration(self):
    #     self.clear()
    #
    #     heading = Label(self.root, text="NLPApp", bg="#34495E")
    #     heading.configure(font=("verdana", 26, "bold"))
    #     heading.pack(pady=(30, 20))
    #
    #     sub_lebel = Label(self.root, text="Image Generator", bg="#34495E")
    #     sub_lebel.configure(font=("verdana", 20, "bold"))
    #     sub_lebel.pack(pady=(30, 20))
    #
    #     label1 = Label(self.root, text="Enter text", bg="white")
    #     label1.configure(font=("verdana", 14))
    #     label1.pack(pady=(10, 10))
    #
    #     self.image_text_input = Entry(self.root, width=70)
    #     self.image_text_input.pack(pady=(10, 10), ipady=20)
    #
    #     image_generation_button = Button(self.root, text="Get Image", height=2, width=20, command=self.do_image_generation)
    #     image_generation_button.pack(pady=(10, 10))
    #
    #     # self.image_result = Label(self.root, image=None)
    #     # self.image_result.pack(pady=(10, 10))
    #
    #     Go_back = Button(self.root, text="Go Back", height=2, width=15, command=self.homepage)
    #     Go_back.pack(pady=(30, 10))
    #
    #
    #
    # def do_image_generation(self):
    #
    #     image_text = self.image_text_input.get()
    #
    #     # API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    #     # headers = {"Authorization": "Bearer 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"}
    #     #
    #     # def query(payload):
    #     #     response = requests.post(API_URL, headers=headers, json=payload)
    #     #     return response.content
    #     #
    #     # image_bytes = query({
    #     # "inputs": image_text,
    #     # })
    #     # You can access the image with PIL.Image for example
    #     import io
    #     from PIL import Image , ImageTk
    #     # image = Image.open(io.BytesIO("C:\\roshani kaku\\Pictures\\Instagram\\anu.jpg"))
    #
    #     # image = image.resize((512, 512))
    #
    #
    #     # print(image.width , image.height)
    #     # print(image.mode)
    #
    #     # img = ImageTk.PhotoImage("anu.jpg")
    #     # print (img)
    #     # # img_ref = img
    #     # #
    #     #self.clear()
    #     #
    #     image_result = Label(self.root, image="response/s.jpg")
    #
    #     image_result.pack()

obj = NLPApp()