# devops test project

This project deploys infrastructure using Ansible.

Components:

- Docker
- PostgreSQL container
- Python init_db container
- Flask container
- Nginx container
- Ansible roles
- Ansible Vault for secrets

Description:

- PostgreSQL runs in Docker container
- init_db container creates tables and fills database with data
- Flask app reads data from PostgreSQL using JOIN query
- Nginx works as reverse proxy for Flask
- All containers are started via Ansible roles
- Docker Compose is not used
- Database password is stored in Ansible Vault

Run:

ansible-playbook ansible/playbooks/site.yml -K --ask-vault-pass
