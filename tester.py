from mediApi import *

chatBot = MediSearch()

patient1 = "AN_ACCESS_TOKEN"

while True:
    question = input("Question: ")
    print(f"Answer: {chatBot.ask(question, patient1)}")
    