#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os
from biliup.downloader import download
from biliup.plugins.bili_webup import BiliBili, Data

def downloadVideo(url, infofn='/tmp/tt.json', save_path='/tmp',video_quality='720P'):
    info = {                                  
        "converter": {
        },
        'downloader':{                          
            "audio_quality": video_quality,           
            "device": "android",                
            "media_type": "video",              
            "playlist": "false",                
            "save_id3": "false",                
            "save_path": save_path,           
            "subtitle": "en",                   
            "url": url ,                          
            "video_quality": video_quality,
            },                                    
            "ffmpeg_location": "/usr/bin/ffmpeg",
            "log_path": "/tmp/",
        }
    json.dump(info, open(infofn,'w'))
    cmd = f'''cd dl ;
    unset http_proxy
unset socks_proxy
unset https_proxy
unset all_proxy
unset no_proxy

export all_proxy="http://127.0.0.1:7890"
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export no_proxy="localhost, 127.0.0.1"
export 
    python3 itubego-dl.py {infofn}
    '''
    os.system(cmd)
    #runCmd(cmd);

def getVideoDlLog(url, infofn='/tmp/tt.json', save_path='/tmp',video_quality='720P', logfn='/tmp/tt.log'):
    info = {                                  
        "converter": {
        },
        'downloader':{                          
            "audio_quality": video_quality,           
            "device": "android",                
            "media_type": "video",              
            "playlist": "false",                
            "save_id3": "false",                
            "save_path": save_path,           
            "subtitle": "en",                   
            "url": url ,                          
            'sniff_only': True,
            "video_quality": video_quality,
            },                                    
            "ffmpeg_location": "/usr/bin/ffmpeg",
            "log_path": "/tmp/",
        }
    #saveJson2File(info, infofn)
    json.dump(info,open(infofn,'w'))
    cmd = f'''cd dl ;
    unset http_proxy
unset socks_proxy
unset https_proxy
unset all_proxy
unset no_proxy

export all_proxy="http://127.0.0.1:7890"
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export no_proxy="localhost, 127.0.0.1"
export 
    python3 itubego-dl.py {infofn} | tee {logfn}
    '''
    #runCmd(cmd);
    os.system(cmd)

LOG_FN='/tmp/tt.log'
TMP_VIDEOFN='/tmp/tt.mp4'
TMP_COVERFN='/tmp/tt.png'

def uploadBiliBilit(title, tags, videofn, coverfn, tid=17):
    video = Data()
    video.title = title
    video.desc =  title
    video.copyright=2
    video.source = 'youtube'
    # 设置视频分区,默认为160 生活分区
    video.tid = tid
    video.set_tag(tags)
    cmd= f'cp "{videofn}" {TMP_VIDEOFN}'
    os.system(cmd)# runCmd(cmd)
    cmd= f'convert "{coverfn}" {TMP_COVERFN}'
    os.system(cmd)# runCmd(cmd)
    file_list=[TMP_VIDEOFN]
    print(video)
    with BiliBili(video) as bili:
        bili.login('engine/bili.cookie',{'account':'13537853751'})
        for f in file_list:
            video_part = bili.upload_file(f)  # 上传视频
            video.append(video_part)  # 添加已经上传的视频
        video.cover = bili.cover_up(TMP_COVERFN)
        ret = bili.submit()  # 提交视频

def main():
    info = json.load(open('paras.json'))
    for t, v in enumerate(info):
        dlurl = v['dlurl']
        downloadVideo(dlurl)
        getVideoDlLog(dlurl, logfn=LOG_FN)
        for tt, ll in enumerate(open(LOG_FN).read().splitlines()):
            info= json.loads(ll)
            if info['type'] == 'sniff':
                msg = info['msg']
                videofn = os.path.join('/tmp', msg['filepath'])
                coverfn = os.path.join('/tmp', msg['local_thumbnail'])
                title = v['bilibili']['title']
                tags =  v['bilibili']['tags']
                print(videofn, coverfn)
                uploadBiliBilit(title, tags, videofn, coverfn)
        
    

if __name__ == '__main__':
    main()

