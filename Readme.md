python -m venv venv

./venv/bin/activate

add 1 cmd

cd backend/it_course_backend

pip install -r requirements.txt


python manage.py runserver

add 2 cmd

cd frontend

npm install

nmp run dev

or

install docker

root cmd  docker-compose up --build

clear and fix docker
 
docker rm $(docker ps -aq) - remove all containers

docker rmi $(docker images -q) - remove all images