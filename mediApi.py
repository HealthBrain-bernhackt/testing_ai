from medisearch_client import MediSearchClient
from databaseManager import Manager

class MediSearch:
    # Initialise the MediSearch client
    def __init__(self):
        self.client = MediSearchClient(api_key="1DB9Yw5rHk8dQhIG5CtR")
        self.manager = Manager()

    # Makes the API call to MediSearch
    def __askAI__(self, query):
        responses = self.client.send_user_message(
            conversation=query,
            conversation_id="",
            should_stream_response=False,
        )
        # filter out the response and catch sources
        for response in responses:
            try:
                return response["text"]
            except:
                return f"\nSources:\n{response['articles'][0]['title']}: {response['articles'][0]['url']}"  # type: ignore

    # Private Method to generate the context query for the AI.
    # This and the answer the AI will give to the context needs to be filtered out in either frontend or backend
    def __generateQuery__(self, patient_data, additional_info):
        query = {
            "patient_data": {
                "age": patient_data["age"],
                "gender": patient_data["gender"],
                "medical_history": patient_data["medical_history"],
                "current_medications": patient_data["current_medications"],
                "medical_knowledge": "low",
            },
            "additional_info": additional_info,
        }
        return str(query) + ". Introduce yourself."

    # Public method to ask the AI a question
    def ask(self, question, patient_id):
        self.manager.add_message(patient_id, question)
        self.manager.add_message(patient_id, self.__askAI__(self.manager.get_chat(patient_id)))
        return self.manager.get_latest_message(patient_id)
    
    def initialise_chat(self, patient_id, patient_data={}, additional_info=""):
        self.manager.init_chat(patient_id)
        query = self.__generateQuery__(patient_data, additional_info)
        self.manager.add_message(patient_id, self.__askAI__([query]))
        return self.manager.get_latest_message(patient_id)

    def get_whole(self):
        return self.manager.chats