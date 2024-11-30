import configuration
import requests
import data

def get_logs():
    return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH,
                        params={"count":15})

#logs = get_logs()

#print(logs.text)

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                        headers=data.headers,
                        json=body)

#response = post_new_user(data.user_body)
#print(response.json())

def get_user_table():
    return  requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

print(get_user_table().text)