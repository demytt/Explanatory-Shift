# Explanatory-Shift

Dependencies: Python, Vowpal

## Install git and clone repo
```
sudo apt-get install git
git clone https://github.com/demytt/Explanatory-Shift.git
```

## Install Vowpal Wabbit
```
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
sudo apt-get install python-pandas
sudo pip install nltk
sudo python
import nltk
nltk.download('stopwords')
```
