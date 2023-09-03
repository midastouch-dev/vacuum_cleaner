# Robot Vacuum Cleaner

![Run](https://github.com/midastouch-dev/vacuum_cleaner/blob/main/screenshot/run.jpg)

Control the robot vacuum cleaner by comments and get some results such as traversing path, cleaned rooms, rooms passed without clean, etc. It receives the cleaning instructions as an array of arrays like [[3,2,4],[2,8,4],[4,6,4,9]]. Also receives set of comments called ‘Priority Rooms’, [7,14, 1]. The vacuum cleaner cleans the rooms using two type of comments.
This project is based on Ubuntu 22.04.

## Environment
- [Install the Git](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-22-04)
- [Install the Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04) 

## Project Structure

```bash
├── screenshot
├── vacuumcleaner
│   ├── __init__.py
│   ├── vacuumcleaner.py
├── test
│   ├── __init__.py
│   ├── test.py
├── app.py
├── Dockerfile
├── requirements.txt
├── start.sh
├── README.md
```
## Technologies used

[<img align="left" alt="Python" width="30px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png" />](#)
[<img align="left" alt="Flask" width="30px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/flask/flask.png" />](#)
[<img align="left" alt="Docker" width="30px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/docker/docker.png" />](#)
<br/>

## Running the app locally
1. Run the docker image
```
sudo bash start.sh
```

Once the server is up-and-running, go to your browser, and visit http://localhost:8000 to use the app.

You can check the running containers by the following comment.
```
sudo docker ps
```
2. Test the project
Implemented the test case using Pytest.  This project sets 12 cases of test case and passed 100%
```
Sudo docker exec [CONTAINER ID] pytest test/test.py -v
```
![Test](https://github.com/midastouch-dev/vacuum_cleaner/blob/main/screenshot/test.jpg)


3. Finish the docker image
```
sudo docker stop [CONTAINER ID]
```
