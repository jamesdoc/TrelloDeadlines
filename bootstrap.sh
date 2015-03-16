sudo apt-get install -y curl build-essential software-properties-common python-software-properties
sudo apt-get update

## Go get NodeJS for laters
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get install -y nodejs

cd /vagrant

## Get some python libraries...
sudo apt-get -y install libxml2-dev libxslt1-dev python-dev
sudo wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
sudo apt-get -y install python-pip

sudo pip install tornado
sudo pip install requests
sudo pip install Jinja2

## Sass and & Compass for CSS complication
sudo gem update --system
sudo gem install sass
sudo gem install compass

sudo npm install --global gulp
sudo npm install --save-dev gulp