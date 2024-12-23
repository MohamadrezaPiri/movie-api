## Movie Blog
A blog for cinema lovers. You can import movies from IMDB, see the details of a movie and even rate that movie.
## Technologies used:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
## Installation
- Clone the project:
```
git clone https://github.com/MohamadrezaPiri/movie-api.git
```
- Create a virtual environment:
```
py -m venv YourVirtualEnvironment
```
- Then activate it:
```
YourVirtualEnvironment/Scripts/activate
```
- Using the command below, install all the packages in ```requirements.txt``` file:
```
pip install -r requirements.txt
```
- And finally:
```
py manage.py migrate
```
- Now it's time to run the server:
```
py manage.py runserver
```
## Usage
- You can add a movie by searching its name. Example:
```
http://127.0.0.1:8000/import_movies/?title=forrest+gump
```
- Rate movies at this endpoint:
```
http://127.0.0.1:8000/ratings
```
Authentication is required for rating movies (Use [ModHeader](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en) extension for authentication)

