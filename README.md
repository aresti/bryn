# bryn
The CLIMB management web interface

## setting up virtualenv

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

### Deploying updates

* Commit and push changes to repo
* ensure local settings files are present
* from `deploy_tools` dir on local machine: `fab deploy:host=ubuntu@bryn.climb.ac.uk`

### Local development environment setup

* clone the repo
* setup venv and install requirements
* obtain credentials for auth_settings.py and a copy of locals.py
* install sshuttle on local machine
* sshuttle --dns -H -r user@someVMwithinCLIMB 0/0