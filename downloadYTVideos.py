
import json
import os

DIR='../../Downloads/android.system.programming/'

def main():
    videolistfn = os.path.join(DIR, 'videolist')
    for l in open(videolistfn).read().splitlines():
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
                        "save_path": DIR,
                        "subtitle": "en",
                        "url": v['url'],
                        "video_quality": "1080P"
                      },
                      "ffmpeg_location": "/usr/local/bin",
                      "log_path": "/tmp/"
                    }
                json.dump(dlparas, open('/tmp/tt.json','w'))
                cmd = 'cd dl && python3 itubego-dl.py /tmp/tt.json'; os.system(cmd)
                cmd = '/Applications/VidJuice\ UniTube.app/Contents/MacOS/media-dl /tmp/tt.json'; os.system(cmd)

if __name__ == '__main__':
    main()

