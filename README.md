# Flask-Mongoengine RESTful API Example

This repository contains the example code for API project, using MongoEngine, Marshmallow with Flask built on Docker.

User account has to be created to use application. Only registered users can add boards, cards and comments.
Entities may be deleted by owners only.

## Project Structure

### Application Structure
```
app/
├── requirements.txt
├── wsgi.py
├── Dockerfile
└── server
    ├── __init__.py
    ├── database
    │   ├── __init__.py
    │   ├── models.py
    │   └── schemas.py
    └── resources
        ├── __init__.py
        ├── auth.py
        ├── boards.py
        ├── cards.py
        └── comments.py
```

## API

<table>
  <tr>
    <th>Method</th>
    <th>Route</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET</td>
    <td>/</td>
    <td>Index of application</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/auth/register</td>
    <td>Register to application</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/auth/login</td>
    <td>Login to applicaiton</td>
  </tr>
</table>

### Boards

<table>
  <tr>
    <th>Method</th>
    <th>Route</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET</td>
    <td>/boards/</td>
    <td>List of boards</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/boards/</td>
    <td>Create a new board</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/boards/{board_id}</td>
    <td>Get board details by ID</td>
  </tr>
  <tr>
    <td>PUT</td>
    <td>/boards/{board_id}</td>
    <td>Update board details by ID</td>
  </tr>
  <tr>
    <td>DELETE</td>
    <td>/boards/{board_id}</td>
    <td>Delete a board by ID</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/boards/{board_id}/cards/</td>
    <td>Add a new card to board</td>
  </tr>
</table>

### Cards

<table>
  <tr>
    <th>Method</th>
    <th>Route</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET</td>
    <td>/cards/{card_id}</td>
    <td>Get card details by ID</td>
  </tr>
  <tr>
    <td>PUT</td>
    <td>/cards/{card_id}</td>
    <td>Update card details by ID</td>
  </tr>
  <tr>
    <td>DELETE</td>
    <td>/cards/{card_id}</td>
    <td>Delete a card by ID</td>
  </tr>

</table>

### Comments

<table>
  <tr>
    <th>Method</th>
    <th>Route</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GET</td>
    <td>/cards/{card_id}/comments/</td>
    <td>List of comments of card</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/cards/{card_id}/comments/{comment_id}</td>
    <td>Get comment details by ID</td>
  </tr>
    <tr>
    <td>POST</td>
    <td>/cards/{card_id}/comments/</td>
    <td>Add a new comment to card</td>
  </tr>
  <tr>
    <td>PUT</td>
    <td>/cards/{card_id}/comments/{comment_id}</td>
    <td>Update comment details by ID</td>
  </tr>
  <tr>
    <td>DELETE</td>
    <td>/cards/{card_id}/comments/{comment_id}</td>
    <td>Delete a comment by ID</td>
  </tr>
</table>

## Schemas

#### User
- id *(read only)*
- email
- password
#### Board
- id *(read only)*
- name
- status *(one of: active, archived)*
- owner *(read only)*
- date_created *(read only)*
#### Card
- id *(read only)*
- title
- content
- start_date
- end_date
- date_created *(read only)*
- date_completed
- owner *(read only)*
- assigned
#### Comment
- id *(read only)*
- text
- sender
- date_created *(read only)*

## Setup

1. Install `docker` and `docker-compose`
2. Clone repository
3. Build repository using `docker-compose up -d`
4. Setup MongoDB
    1. Start interactive MongoDB shell: `docker exec -it mongodb bash`
    2. Login to the MongoDB account in container shell. Enter password defined in `docker-compose.yml`:

    `mongo -u mongodbuser -p`

    3. Switch to the `flaskdb` database: `use flaskdb`
    4. Create user to be allowed to access database. User and values must be same as defined in `docker-compose.yml`:

    `db.createUser({user: 'flaskuser', pwd: 'your_mongodb_password', roles: [{role: 'readWrite', db: 'flaskdb'}]})`

    5. Logout from database: `exit`
    6. Login again to check then exit: `mongo -u flaskuser -p your_mongodb_password --authenticationDatabase flaskdb`
    7. Exit the container by typing `exit`
5. Go to `http://localhost:3000` and check if it is working.

## Examples

### Register and Login
Save Bearer token after login
```bash
curl -i -H "Content-Type: application/json" -X POST \
  -d '{"email": "john.doe@example.com", "password": "strongpassword"}' \
  http://localhost:3000/auth/register

curl -i -H "Content-Type: application/json" -X POST \
  -d '{"email": "john.doe@example.com", "password": "strongpassword"}' \
  http://localhost:3000/auth/login
```

### Get list of boards
```bash
curl -X GET http://localhost:3000/boards/
```

### Add a board
Use Bearer token given after login
```bash
curl -i -H "Content-Type: application/json" -X POST \
  -H "Authorization: Bearer {token}" \
  -d '{"name": "New Board", "status": "active"}' \
  http://localhost:3000/boards/
```

## License

This application is licensed under the GNU GPLv3 License. See LICENSE file for more details
