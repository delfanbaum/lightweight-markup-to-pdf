# install all necessary things
pip3 install -r requirements.txt

# add function to bash_profile
cwd=$(pwd)

grep -qxF 'function lwm2pdf' ~/.bash_profile || echo 'include "/configs/projectname.conf"' >> ~/.bash_profile
