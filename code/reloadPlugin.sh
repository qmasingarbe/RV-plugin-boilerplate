# This little bash script (linux only) will enable you to test your code quicly
# 1. copy python file in devlopment folder to install folder of rv
cp /path/to/python/file/in/ide/my_code.py /path/to/rv/plugin/directory/my_code.py
# 2. kill any running instance of RV
kill $(ps aux | grep rv.bin | awk '{print $2}')
# 3. launch a new instance of RV (with custom env or test file loading)
rv /path/to/test/movie.mov