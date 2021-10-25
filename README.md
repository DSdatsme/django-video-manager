# Video Manager App

This is a basic Django backend app that does CRUD operations on Videos that are stored on disk.

## Deploy the App

Updated the server IP in hostgroup `django` in inventory `hosts`.

create a file called `vpass` which will be your vault password file with value `aaaa` which is your token value.

Run the playbook

```bash
ansible-playbook -b -K django_deploy.yml -i hosts --vault-password-file vpass
```

This will setup everything from database, migrations and app.
