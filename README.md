# Backend
Das backend ist in Python geschrieben. MediApi.py organisiert den AI Chat der app. Der databaseManager.py unterstützt dies, indem er die aktiven chats speichert. Sobald ein chat geschlossen wird, wird auch der Chat verlauf gelöscht.

Als Verbindungspunkt von backend zu Frontend benutzen wir Django. Das DjangoRestFramework bietet eine simple Schnittstelle um die beiden Welten zu verbinden.
