app="vacuum-cleaner"
docker build -t ${app} .
docker run -d -p 8000:3000 ${app}
