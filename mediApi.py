from medisearch_client import MediSearchClient
from databaseManager import Manager
import requests, re


class MediSearch:
    # Initialise the MediSearch client
    def __init__(self):
        self.client = MediSearchClient(api_key="")
        self.manager = Manager()

    # Makes the API call to MediSearch
    def __askAI__(self, query):
        try:
            responses = self.client.send_user_message(
                conversation=query,
                conversation_id="",
                should_stream_response=False,
            )
        except Exception as e:
            return self.__error_handler__(e)
        # filter out the response and catch sources
        for response in responses:
            try:
                return response["text"]
            except Exception as e:
                if response["error_code"]:
                    return self.__error_handler__(response["error_code"])
                else:
                    return self.__error_handler__(e)

    # Private Method to generate the context query for the AI.
    # This and the answer the AI will give to the context needs to be filtered out in either frontend or backend
    def __generateQuery__(self, patient_data, additional_info):
        query = f"{patient_data} {additional_info} Medical knowledge: low"
        return str(query)

    def __remove_sources__(self, response):
        return re.sub(r"\s?\[\d+(,\s*\d+)*\]", "", response)

    def __request_patient_data__(self, patient_id):
        # make an api call to get the patient data
        url = "https://health-brain-922fa718a7c7.herokuapp.com/auth/api/profile/"

        headers = {"Authorization": f"Bearer {patient_id}"}

        response = str(requests.get(url, headers=headers))

        if "age" not in response:
            return self.__error_handler__("Token not valid")
        else:
            return response

    def __error_handler__(self, error_code):
        error_code = str(error_code)
        if error_code == "Token not valid":
            return (
                "Oh snap! You don't seem to be logged in. Please log in and try again."
            )
        elif error_code == "error_auth":
            return "Oh snap! Some developer messed up the API key. Please contact the developers."
        elif error_code == "error_internal":
            return "Oh snap! Some developer messed up the backend. Please contact the developers."
        elif error_code == "error_llm":
            return "Oh snap! Some developer messed up the AI. Please contact the developers."
        elif error_code == "error_missing_key":
            return "Oh snap! Some developer forgot the API key. Please contact the developers."
        elif error_code in {"error_not_enough_articles", "error_out_of_tokens"}:
            return "Oh snap! You overwhelmed our AI. Please close the chat and open it again."
        else:
            return f"Oh snap! Something went wrong. Please try again and if the problem persists, contact the developers."

    # Public method to ask the AI a question
    def ask(self, question, patient_id, additional_info=""):
        # If the chat does not exist, create it and ask the question with the patient data
        if not self.manager.chat_exists(patient_id):
            self.manager.init_chat(patient_id)
            patient_data = str(self.__request_patient_data__(patient_id))
            if "Oh snap!" in patient_data:
                return patient_data
            query = self.__generateQuery__(patient_data, additional_info)
            if "Oh snap!" in query:
                return query
            self.manager.add_message(patient_id, question)
            message = str(self.__askAI__([f"{query} {question}"]))
            if "Oh snap!" in message:
                return message
            self.manager.add_message(patient_id, self.__remove_sources__(message))
        else:
            self.manager.add_message(patient_id, question)
            message = str(self.manager.get_chat(patient_id))
            if "Oh snap!" in message:
                return message
            self.manager.add_message(patient_id, self.__askAI__(message))
        return self.manager.get_latest_message(patient_id)

    def end_chat(self, patient_id):
        self.manager.remove_chat(patient_id)
