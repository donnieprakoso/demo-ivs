TEST_FILE=""
STREAM_URL=""

ffmpeg -re -stream_loop -1 -i $TEST_FILE -vcodec libx264 -preset veryfast -maxrate 1984k -bufsize 3968k -vf "format=yuv420p" -g 60 -acodec libmp3lame -b:a 96k -ar 44100 -f flv -s 1920x1080 $STREAM_URL