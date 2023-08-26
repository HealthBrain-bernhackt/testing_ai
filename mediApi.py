from medisearch_client import MediSearchClient
from databaseManager import Manager
import requests, re


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
            except Exception as e:
                if response["error_code"]:
                    self.__error_handler__(response["error_code"])
                else:
                    self.__error_handler__(e)

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

        response = str(requests.get(url, headers=headers).json())

        if (
            response
            == "{'detail': 'Given token not valid for any token type', 'code': 'token_not_valid', 'messages': [{'token_class': 'AccessToken', 'token_type': 'access', 'message': 'Token is invalid or expired'}]}"
        ):
            self.__error_handler__("Token not valid")
        else:
            return

    def __error_handler__(self, error_code):
        if error_code == "Token not valid":
            return (
                "Oh snap! You don't seem to be logged in. Please log in and try again."
            )
        elif error_code == "[Errno 11001] getaddrinfo failed":
            return "Oh snap! You seem to be offline. Check your internet connection and try again."
        elif error_code == "error_auth":
            return "Oh snap! Some developer messed up the API key. Please contact the developers."
        elif error_code == "error_internal":
            return "Oh snap! Some developer messed up the backend. Please contact the developers."
        elif error_code == "error_llm":
            return "Oh snap! Some developer messed up the AI. Please contact the developers."
        elif error_code == "error_missing_key":
            return "Oh snap! Some developer forgot the API key. Please contact the developers."
        elif error_code in ["error_not_enough_articles", "error_out_of_tokens"]:
            return "Oh snap! You overwhelmed our AI. Please close the chat and open it again."
        else:
            return "Oh snap! Something went wrong. Please try again and if the problem persists, contact the developers."

    # Public method to ask the AI a question
    def ask(self, question, patient_id, additional_info=""):
        try:
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
        except Exception as e:
            return self.__error_handler__(e)

    def end_chat(self, patient_id):
        self.manager.remove_chat(patient_id)
