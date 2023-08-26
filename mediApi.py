from medisearch_client import MediSearchClient

class MediSearch:
    # Initialise the MediSearch client
    # How will the chat history be managed across multiple users?
    def __init__(self):
        self.client = MediSearchClient(api_key="1DB9Yw5rHk8dQhIG5CtR")
        self.chat_history = []
        self.isFirst = True

    # Makes the API call to MediSearch
    def __askAI__(self, query):
        responses = self.client.send_user_message(
            conversation=query,
            conversation_id=self.PATIENT_ID,
            should_stream_response=False
        )
        #filter out the response and catch sources
        for response in responses:
            try:
                return "Answer: "+response["text"]
            except:
                return f"\nSources:\n{response['articles'][0]['title']}: {response['articles'][0]['url']}" # type: ignore

    # Private Method to generate the context query for the AI.
    # This and the answer the AI will give to the context needs to be filtered out in either frontend or backend
    def __generateQuery__(self, patient_data, additional_info):
        query = {
            "patient_data": {
                "age": patient_data["age"],
                "gender": patient_data["gender"],
                "medical_history": patient_data["medical_history"],
                "current_medications": patient_data["current_medications"],
                "medical_knowledge": "low"
            },
            "additional_info": additional_info
        }
        return str(query)+". Introduce yourself."

    # Public method to ask the AI a question
    def ask(self, question, patient_data="", additional_info="", patient_id=""):
        # Decide if this is the first question or not
        # If it is, generate the query and append it to the chat history, 
        if self.isFirst:
            self.PATIENT_ID = patient_id
            query = self.__generateQuery__(patient_data, additional_info)
            self.isFirst = False
            self.chat_history.append(query)
        else:
            self.chat_history.append(question)
        self.__askAI__(self.chat_history)
