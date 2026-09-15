

# Tender Management System

A command-line application for managing tenders, built with Python.
Users can register, log in, and manage tenders. Admins can close or
award tenders.

## Features

- User registration and login (passwords hashed, never stored in plain text)
- Role-based access: regular users vs admins
- Add and view tenders
- Admins can close or award tenders
- Data is saved to JSON files, so nothing is lost between runs
- Clean, colorful CLI menus using Rich

## Requirements

- Python 3.9+
- Packages listed in `requirements.txt`

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

You'll see a menu. Pick a number and follow the prompts.

## How to use it

1. Register an account (choose role `user` or `admin`).
2. Log in with the same email and password.
3. As a **user**, you can add tenders and view the list.
4. As an **admin**, you can also close or award tenders.
5. Logout or exit anytime from the menu.

## Project structure

```
main.py                    
models/
  user.py                  
  tender.py                
  tender_collection.py     
utils/
  auth.py                  
  decorators.py            
  storage.py                
  validators.py             
data/
  users.json               
  tenders.json               
tests/                     

```

## Project management

We used Trello to track tasks across the team:
[Tender Management System board](https://trello.com/invite/b/6aa3d2f1afbe997f5d4222b5/ATTI31abc2607c1a75953e857fae2f93c7161695CE4E/tender-management-system)

