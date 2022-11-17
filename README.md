Family on a Budget!
=
Not yet finished, but it meets several of the requirements.

---

## 1. Installation

You need to have

- `git`,
- `docker`,
- `docker-compose`

installed.

### a. Clone this repo:

    git clone git@github.com:kamil-n/family-budget.git
    cd family-budget
### b. Prepare the .env file:
Copy or rename **.env.example** file you downloaded into **.env** and edit it:
- set the 'ENV=' variable to 'prod' for example (***uvicorn*** *shouldn't reload on code changes*)
- generate the random string for 'AUTH_SECRET' variable, for example by running `openssl rand -hex 32` on your *nix system. If you can't, just type random characters there.
- set host/port for the app and fill in the details for the database. Defaults provide in the example .env file should be good to go, though.
### c. Build and run:
    docker-compose up --build
> It is possible, that on the first run of **docker-compose**, database will take some time to initialize and the app will fail to start.
If that occurs, press `Ctrl+C` and run `docker-compose up` the second time.
## 2. Preparation
Go to the address you set in 1.b. in your browser (default = http://0.0.0.0:5000).

You will be redirected to Swagger documentation page, where you can interact with the endpoints.

Before you begin, you should acquire the token, and for that, a valid user must already be present in the database. To create it:
### a. Prepare a hashed password:
Easiest way is to go to a webpage https://bcrypt-generator.com/ or https://bcrypt.online/ and hash a string there. For example, string *test* hashes to *$2a$04$xaVeFtb/uotowOpW7cpbh.qbPZgPVnRNMiTiFdSQBaO0aKHyw3Hgm*. Write it down.
### b. Connect directly to the database by typing

    docker-compose exec db psql --username=budget_user --dbname=budget_db
where **db** is the name of the service from docker-compose file.

You shoud see a psql prompt.
### c. Add your first user:

    INSERT INTO users(name, hashed_password, is_active) VALUES ('<your username>', '<your hashed password', TRUE);
and it should be immediately available from the Swagger interface.
## 3. Execution
In the web browser, click the green "Authenticate" button. Type your username and **plain** password in the top fields and send (other fields are irrelevant). You should be authenticated now and all endpoints should be available. You can send and retrieve test data using the interface.
> When calling the API directly, you can call the `/token` endpoint with a JSON containing 'username' and 'password' (hashed one). You should get the token, which you can then attach in a header ({'Authentication': 'Bearer \<token\>'}) to your following requests.
## 4. Cleanup
The usual:

    docker-compose down --volumes
and remove the containers and volumes with `docker container|volume rm` or `prune`.
