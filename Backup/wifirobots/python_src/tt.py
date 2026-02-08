import os
path_sh = 'sh '+ os.path.split(os.path.abspath(__file__))[0] + '/mjpg-streamer-master/mjpg-streamer-experimental/start_mjpg_streamer.sh &'
print(path_sh)