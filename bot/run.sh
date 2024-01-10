while true
do
  python3 main.py
  echo "Updating..."
  sleep 1
  cd ..
  sh get_files.sh
  cd bot
done
