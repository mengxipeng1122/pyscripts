
import json
import os
def main():
	for l in open('android.system.programming/videolist').read().splitlines():
		info = json.loads(l)
		if 'type' in info and 'playlist' == info['type']:
			msg = info['msg']
			for v in msg['videos']:	
				print(v)
				dlparas = {
					  "converter": {
					  },
					  "downloader": {
					    "audio_quality": "1080P",
					    "device": "android",
					    "media_type": "video",
					    "playlist": "false",
					    "save_id3": "false",
					    "save_path": "android.system.programming/",
					    "subtitle": "en",
					    "url": v['url'],
					    "video_quality": "1080P"
					  },
					  "ffmpeg_location": "/usr/local/bin",
					  "log_path": "/tmp/logs"
					}
				json.dump(dlparas, open('/tmp/tt.json','w'))
				cmd = '/Applications/VidJuice\ UniTube.app/Contents/MacOS/media-dl /tmp/tt.json'
				os.system(cmd)
				cmd = 'cd unitube && python3 itubego-dl.py /tmp/tt.json'
				os.system(cmd)

if __name__ == '__main__':
	main()

