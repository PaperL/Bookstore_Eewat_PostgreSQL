# Bookstore Eewat

> Single assignment for SJTU CS3952

- A bookstore system with database written with Python ORM
  - Frontend
    - Just test, no GUI, based on Flask
  - Backend
    - based on **PostgreSQL**
- Problem description: [intro.md](docs/intro.md)
- Project report: [Report.md](docs/Report.md)

## Get started

- `sudo apt install postgresql`
  - Maybe `libpq-dev` is also needed
  - `sudo su - postgres`, `pg_ctlcluster 12 main start`

- `pip install -r requirements.txt` in the folder `bookstore`
  - Maybe `psycopg2` and `pytest-cov` is also needed