

## Access management
1. Write: only privilege as high as or higher than an engineer can write
2. Read: anyone logined with an account can see the dashboard display

## DB management
### Spec
- sqlite3
- in-program API: SQL language query
- Table content for each user
    - id
    - role
    - username
### Operation
1. Create: there will always be a default user with username/password being admin/admin. Only the admin can create users. (now create by hard coding)
2. Delete: only admin can delete users.

Q: How does real world system's DB being managed?
> For now just create a DB that supports at least 3 users: Admin(with highest privilege), guest(with lowest privilege), engineer(with medium privilege).