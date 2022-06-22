### Projekt Turnieju na zajęcia z Python'a w architekturze Rest wykorzystując django_restframework


### Uruchomienie projektu:

* zainstalowanie paczek wymaganych z pliku
* stworzenie migracji komenda : python manage.py makemigrations
* zastosowanie migracji komenda: python manage.py migrate
* stworzenie admin/superuser: python manage.py createsuperuser

### Funkcjonalność Podstawowa

1. Panel Admina http://127.0.0.1:8000/admin/
2. Api http://127.0.0.1:8000/api/v1/

### Ogólne założenia

Niektóre widoki są dostępne tylko dla zalogowanych / zajerestrowanych użytkowników reszta jest ReadOnly.


### Funkcjonalność API

1. Rejestracja użytkownika http://127.0.0.1:8000/api/v1/register/
<br>
Wymagane jest podanie :
* username
* email ( poprawny )
* password
* birth - dzien urodzin

Po rejestracji użytkownik otrzymuje Token ( jeśli Frontend podpinałby się pod API mógłby go przechować)

2. Logowanie http://127.0.0.1:8000/api/v1/login/
<br>
Logowanie działa w poprawny sposób ponieważ jest wykorzystywany dodatkowy mechanizm django do logowania 
z django.contrib.auth

logowanie jest za pomocą :
* username
* password

3. Logout http://127.0.0.1:8000/api/v1/logout/
<br>
4. Podgląd wszystkich użytkowników http://127.0.0.1:8000/api/v1/profiles/
5. Turnieje - http://127.0.0.1:8000/api/v1/tournaments/ 

Dodatkowe akcje dla turnieji:
    1.hhttp://127.0.0.1:8000/api/v1/tournaments/{id}/add_teams_add_generate_qualifications/ gdzie id to id turnieju:
      1. Na tym widoku w RawData / Post po podaniu teamów zostaną wygnerowany randomow "stage" kwalifkacyjny
      przed tym należy jednak utworzyć Team i dodać do niego uzytkownika/ użytkowników
    2.http://127.0.0.1:8000/api/v1/tournaments/{id}/get_specific_stage/?get_specific_stage=0
      1. Na tym widoku po podaniu w query otrzymamy specificzny stage turnieju
    3.http://127.0.0.1:8000/api/v1/tournaments/{id}/end_tournament/
      1. Zakończenie konkretnego turnieju
    4.http://127.0.0.1:8000/api/v1/tournaments/historic_tournaments/?start_time=value&end_time=value
        1. Zwraca turnieje które są historyczne / ukoczone z okresu czasu 

6.Teams http://127.0.0.1:8000/api/v1/teams/

Dodatkowe akcje dla Teams:   
    1. Tworzenie Teamu z kolorem ( z walidacją dla hex )
    2. http://127.0.0.1:8000/api/v1/teams/{id}/add_me_to_team/
        1. Użytkownik może się dodać do konkretnego teamu
    3.http://127.0.0.1:8000/api/v1/teams/{id}/add_user_to_team/
        1. Uzytkownik może dodac innego użytkownika do teamu

7. Matche http://127.0.0.1:8000/api/v1/matches/

Dodatkowe akcje dla teams 
    1. http://127.0.0.1:8000/api/v1/matches/{id]/change_score_for_match/
        1. Zmiana wyniku dla matchu

8. Stages http://127.0.0.1:8000/api/v1/stages/

Dodatkowe akcje dla stages:
    1.http://127.0.0.1:8000/api/v1/stages/check_winners/
        1. Automatyczne sprawdzenie wygranego na podstawie wyniku