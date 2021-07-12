import os, cv2,numpy as np,time
from PIL import Image

def get_avg_fps(PIL_Image_object) -> float: # stolen: https://stackoverflow.com/questions/53364769/get-frames-per-second-of-a-gif-in-python
    # Returns the average framerate of a PIL Image object
    PIL_Image_object.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += PIL_Image_object.info['duration']
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            return frames / duration * 1000

frame_h = 0
def read(_path:str) -> np.ndarray:
    global frame_h
    if '.gif' not in _path or not os.path.isfile(_path):
        print('given path does not leave to a gif')
        exit(0)
    cap = cv2.VideoCapture(_path)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_h = frameHeight
    _buf = np.empty((frameCount, frameHeight, frameWidth), np.dtype('uint8'))
    fc = 0
    ret = True
    __start = time.time()
    print("reading file...")
    while fc < frameCount and ret:
        ret, tmp_img = cap.read()
        _buf[fc] = cv2.Canny(cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY),90,175) # you can try playing with blur | 90low and 175high worked best for me but feel free to play with that aswell
        fc += 1
    cap.release()
    print(f"\rreading file finished | {round(time.time()-__start,2)} seconds")
    return _buf

if __name__ == "__main__":
    filename = input('file name ~> ')
    buf = read(f'D:\\PythonProjects\\Python\\projects\\gif_player\\{filename}')
    frames = {}
    len_buf = len(buf)
    _start = time.time()
    print(f'processing {len_buf} frames with {len(buf[0][0])} x values and {len(buf[0])} y values')
    for frame in range(len(buf)):
        print(f'\rprocessing frame {frame+1}/{len_buf} | {round(((frame+1)*100)/len_buf,1)}%',end="")
        edge_pos = []
        for y in range(len(buf[frame])):
            for x in range(len(buf[frame][y])):
                if buf[frame][y][x] == 255:
                    edge_pos.append([x,y])
        frames[frame] = edge_pos
    print(f'\rprocessing finished | {round(time.time()-_start,2)} seconds')
    _start = time.time()
    print(f'writing {len_buf} frames with {len(buf[0][0])} x values and {len(buf[0])} y values')

    _idk = 1 # change this if you want to play with the height
    # apply the _idk
    for i in range(len(frames)):
        print(f'\rwriting frame {i+1}/{len_buf} | {round(((i+1)*100)/len_buf,1)}%',end="")
        tot_str = "" # could also be a list idk what is more efficient
        white_px = {}
        for u in range(len(frames[i])):
            try:
                white_px[frames[i][u][1]/_idk].append(int(frames[i][u][0]/_idk))
            except KeyError:
                white_px[frames[i][u][1]/_idk]= [int(frames[i][u][0]/_idk)]
        l = 0
        if frame_h-330 > 0: # 330px cutoff
            l = frame_h-330
        for y in range(l,l+330):
            line = " "*768 # width
            try:
                white_px[y] # check for KeyError before running everything
                s = list(line)
                for x in white_px[y]:
                    s[x] = '#'
                    try: # should be individual checks
                        s[x+1] = '#'
                        s[x+2] = '#'
                        s[x+3] = '#'
                    except KeyError:
                        pass

                line = "".join(s)
            except KeyError:
                pass
            tot_str+=line+'\n'
        frames[i] = tot_str
    print(f'\rwriting finished | {round(time.time()-_start,2)} seconds')
    print('calculating avg fps...')
    avg_fps = get_avg_fps(Image.open(os.path.join(os.path.dirname(__file__),filename))) # PIL might be unnecessary not really familliar with cv2's way of importing Images so i'll keep it like this
    print(f'\ravg fps: {avg_fps}')
    avg_fps = 1/avg_fps
    for i in range(3):
       print(f'\r{3-i}',end="")
       time.sleep(1)
    print("\033[%d;%dH" % (0, 0))
    try:
        while True:
            for i in range(len(frames)):
                print(frames[i])
                print("\033[999A")
                print("\033[0;0f")
                time.sleep(avg_fps)
    except KeyboardInterrupt:
        pass
