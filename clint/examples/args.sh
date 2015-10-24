
echo 'No arguments:'
python args.py 

echo 'A few arguments:'
python args.py -s this that --import this and that and this and that

echo 'A few expanded file arguments:'
python args.py *.py

echo 'A few non-expanded file arguments:'
python args.py '*.py'

echo 'A few mixed files/flags/arguments:'
python args.py '*.py' --test test face book -s ~/.ssh
