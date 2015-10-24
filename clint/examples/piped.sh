
echo 'Piped in IP address:'
curl -s http://icanhazip.com | python piped.py 

echo 'Piped in nothing:'
python piped.py 
