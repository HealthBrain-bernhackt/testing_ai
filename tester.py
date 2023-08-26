from mediApi import *

chatBot = MediSearch()

patient1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzMTAxODg0LCJpYXQiOjE2OTMwOTEwODQsImp0aSI6IjQxMjhjZGM5ZDM1NzQ5YTk4ZjM5NTk2OWNiZmFiMGIyIiwidXNlcl9pZCI6NSwiZW1haWwiOiJhZG1pbkBnbWFpbC5jb20iLCJkb2N0b3IiOnRydWV9.gJxSbSKkV2nUTMhu4LPHcVZLKNDrrO1F0OSt2QG32pU"

while True:
    question = input("Question: ")
    print(f"Answer: {chatBot.ask(question, patient1)}")
    