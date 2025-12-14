# Example: Spin Postgres

This is an example showcasing the use of Spin PostgreSQL bindings within a guest component. 

## Preparing the Environment

Run the following commands to setup a virtual environment with Python.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages specified in the `requirements.txt` using the command:

```bash
pip3 install -r requirements.txt
```

For this example, a PostgreSQL database named `spin_dev` must be accessible at `127.0.0.1` with a user `postgres` should exist. 

### Setting Up the Test Table

Create a test table in your PostgreSQL database:

```sql
CREATE TABLE test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value INTEGER
);

INSERT INTO test (name, value) VALUES 
    ('foo', 42),
    ('bar', 100);
```

## Building and Running the Examples

```bash
spin build --up
```

## Testing the App

```bash
$ curl localhost:3000
id | name | value
-----------------
1 | foo | 42
2 | bar | 100
```
