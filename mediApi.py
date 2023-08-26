from medisearch_client import MediSearchClient
from databaseManager import Manager
import requests, re


class MediSearch:
    # Initialise the MediSearch client
    def __init__(self):
        self.client = MediSearchClient(api_key="API_KEY")
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
            except Exception:
                return f"\nSources:\n{response['articles'][0]['title']}: {response['articles'][0]['url']}"  # type: ignore

    # Private Method to generate the context query for the AI.
    # This and the answer the AI will give to the context needs to be filtered out in either frontend or backend
    def __generateQuery__(self, patient_data, additional_info):
        query = f"{patient_data} {additional_info} Medical knowledge: low"
        return str(query)

    def __remove_sources__(self, response):
        return re.sub(r"\[\d+(,\s*\d+)*\]", "", response)

    def __request_patient_data__(self, patient_id):
        # make an api call to "https://health-brain-922fa718a7c7.herokuapp.com/doctor/patient/:id" to get the patient data
        url = "https://health-brain-922fa718a7c7.herokuapp.com/auth/api/profile/"

        headers = {"Authorization": f"Bearer {patient_id}"}

        return str(requests.get(url, headers=headers).json())

    # Public method to ask the AI a question
    def ask(self, question, patient_id, additional_info=""):
        # If the chat does not exist, create it and ask the question with the patient data
        if not self.manager.chat_exists(patient_id):
            self.manager.init_chat(patient_id)
            patient_data = self.__request_patient_data__(patient_id)
            query = self.__generateQuery__(patient_data, additional_info)
            self.manager.add_message(patient_id, question)
            self.manager.add_message(
                patient_id,
                self.__remove_sources__(self.__askAI__([f"{query} {question}"])),
            )
        else:
            self.manager.add_message(patient_id, question)
            self.manager.add_message(
                patient_id, self.__askAI__(self.manager.get_chat(patient_id))
            )
        return self.manager.get_latest_message(patient_id)

    def end_chat(self, patient_id):
        self.manager.remove_chat(patient_id)
