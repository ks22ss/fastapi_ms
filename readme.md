# Ecommerce Website Backend Server in FastAPI

# Introduction
This is a backend server for an ecommerce website. It is built using FastAPI and PostgresSQL. It is a REST API server. It has the following features:
- User Authentication
- User Authorization
- User Profile
- Product Management
- Order Management
- Customer Management


## Installation Setup
```bash
pip install -r requirements.txt
```
- Setup a SECRET and Database env variable in .env file

## Usage

```bash
pip install uvicorn
uvicorn main:app --reload
```

## API Documentation

```bash
[http://](http://127.0.0.1:8000/docs)
```
### Example


#### Register User

http://localhost:8000/api/v1/auth/register

```json
{
  "email":"test.unit@unittest.com",
  "name": "My Unit Test Ac",
  "password": "unittest"
}
```

#### Register User

http://localhost:8000/api/v1/auth/login

```json
{
  "email":"test.unit@unittest.com",
  "password": "unittest"
}
```

#### Register User

http://localhost:8000/api/v1/auth/login

```json
{
  "email":"test.unit@unittest.com",
  "password": "unittest"
}
```