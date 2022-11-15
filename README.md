On the first run of docker-compose, database will take some time to initialize.
Second run will be successful.

hash passwords for the insert =
https://bcrypt-generator.com/ or https://bcrypt.online/

docker-compose exec db psql --username=budget_user --dbname=budget_db

INSERT INTO users(name, hashed_password, is_active) VALUES ('username', 'hashed_pwd', TRUE);
