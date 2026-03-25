# devops test project

This project deploys infrastructure using Ansible.

Components:

- Docker
- PostgreSQL container
- Python init_db container
- Ansible roles
- Ansible Vault for secrets

Run:

ansible-playbook ansible/playbooks/site.yml -K --ask-vault-pass
