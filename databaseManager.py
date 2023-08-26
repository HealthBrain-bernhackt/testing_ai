class Manager:
    def __init__(self):
        self.chats = {}

    def init_chat(self, patient_id):
        self.chats[patient_id] = []

    def add_message(self, patient_id, message):
        self.chats[patient_id].append(message)

    def get_chat(self, patient_id):
        return self.chats[patient_id]

    def remove_chat(self, patient_id):
        del self.chats[patient_id]

    def chat_exists(self, patient_id):
        return patient_id in self.chats

    def get_latest_message(self, patient_id):
        return self.chats[patient_id][-1]
