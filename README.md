# Explanatory-Shift

Dependencies: Python, Vowpal

## Install git and clone repo
```
sudo apt-get install git
git clone https://demytt@bitbucket.org/demytt/git_uchidata.git
```

## Install Vowpal Wabbit

```
#!shell
#sudo apt-get install vowpal-wabbit 
sudo apt-get install libboost-program-options-dev libboost-python-dev
sudo apt-get install zlib1g-dev
sudo apt-get install libboost1.48-all-dev
sudo apt-get install clang
sudo ln -s /usr/bin/clang-3.5 /usr/bin/clang
sudo ln -s /usr/bin/clang++-3.5 /usr/bin/clang++
sudo apt-get install build-essential g++
cd vowpal-wabbit
sudo make
sudo make test
sudo make install
```

## Install python dependencies ##
```
#!shell

sudo apt-get install python-pandas
sudo pip install nltk
sudo python
import nltk
nltk.download('stopwords')
```
