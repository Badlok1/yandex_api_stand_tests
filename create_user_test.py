import sender_stand_request
import data


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    user_table_response = sender_stand_request.get_user_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
                + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert user_response.status_code == 201 , "Код ответа не 201"
    assert user_response.json()['authToken'] != '' , "В ответе нет токена"
    assert user_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400 , "Код ответа не 400"
    assert user_response.json()["code"] == 400 , "Код в теле не 400"
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов" , \
                                                "Сообщение в ответе не верное"

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400 , "Код ответа не 400"
    assert response.json()["code"] == 400 , "Код в теле не 400"
    assert response.json()["message"] == "Не все необходимые параметры были переданы" , \
                                            "Сообщение в ответе не верное"

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")

def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

def test_create_user_no_first_name_get_error_response():
    user_body_wofn = data.user_body.copy()
    user_body_wofn.pop("firstName")
    negative_assert_no_first_name(user_body_wofn)

def test_create_user_empty_first_name_get_error_response():
    user_body_efn = get_user_body("")
    negative_assert_no_first_name(user_body_efn)

def test_create_user_number_type_first_name_get_error_response():
    user_body_dif_tipeFn = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body_dif_tipeFn)

    assert response.status_code == 400 , "Код ответа не 400"