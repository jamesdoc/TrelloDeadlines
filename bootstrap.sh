sudo apt-get install -y build-essential software-properties-common python-software-properties

cd /vagrant

sudo apt-get update

sudo apt-get -y install libxml2-dev libxslt1-dev python-dev
sudo wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
sudo apt-get -y install python-pip

sudo pip install tornado
sudo pip install requests
sudo pip install Jinja2