poetry run python src/player-piped.py | ffmpeg -i pipe: -f f32le -ar 192000 -ac 2 -acodec pcm_f32le -flush_packets 0 'udp://127.0.0.1:8899'