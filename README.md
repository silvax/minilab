# minilab

This is sample repo with some Ansible code that launches and ec2 instance and installs apache. The sample code takes several parametersin the Ansible run to configure the components

##How to use it

Check out the code

install ansible on your system
```
sudo pip install ansible
```

Configure your aws credentials for boto. For more info see http://boto.readthedocs.org/en/latest/boto_config_tut.html

Now you can run the playbook to test it and play with it. The playbook needs the following parameters in the run

ssh_key - this is the ec2 key pair that will be used to launch the instance on aws
region - this is the aws region where the instance will be launched. 
instance_type - the ec2 instance type that will be launched
image - The Amazon Machine Image Id to use for the launch
vpcid - the id of the VPC that will be used in the launch. This code assumes you will be launching in VPC. But it can easly be modified to run on ec2 classic or VPC Default
vpcsubnet - The subnet that the instance will be launched in. This subnet must be in the vpc that was specified in the vpc id
welcome_message - This welcome message will be templetized on the index.html page of the apache server so it will be displayed when the web server comes up

Here is a sample command line of how run the playbook

```
ansible-playbook setup.yml \
-e ssh_key=dev.ops \
-e region=us-east-1 \
-e instance_type=m3.medium \
-e image=ami-b66ac3de \
-e vpcid=vpc-ba523bd8 \
-e vpcsubnet=subnet-56e7b967 \
-e welcome_message="Welcome to The mini lab"
```

The code also includes an automated infrastructure test. After launching the instance the playbook hits the web server to validate if is up. If the test fails the playbook run will fail
This is the section of the playbook run that validates the site availability

```
- name: test infrastructure components
  hosts: localhost
  gather_facts: false

  tasks:
    - name: get the url of the new web server to validate is up
      action: uri url=http://{{ item.public_dns_name }}/ return_content=yes
      register: webpage
      with_items: ec2.instances
      failed_when: "'Welcome' not in webpage.content"
```

