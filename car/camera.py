from threading import Thread
import subprocess
from time import sleep

"""
/opt/vc/bin/raspivid -n -ih -t 0 -w 800 -h 600 -fps 15 -b 20000000 -o - 
| 
ffmpeg -i - -vcodec libx264 -tune zerolatency -crf 18 
http://localhost:1234/feed1.ffm
"""

raspivid = ['/opt/vc/bin/raspivid',
            '-n',
            '-ih',
            '-t', '0',
            '-w', '480',
            '-h', '320',
            '-fps', '15',
            '-b', '20000000',
            '-o', '-']

ffmpeg = ['ffmpeg',
          '-i', '-',
          '-vcodec', 'libx264',
          '-tune', 'zerolatency',
          '-preset', 'ultrafast',
          'http://localhost:8090/feed1.ffm']

class Camera(Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        self.cam_proc = None
        self.running = False
        Thread.__init__(self)

    def stop(self):
        """Stop the camera."""
        self.cam_proc.terminate()
        sleep(0.5)
        self.cam_proc.kill()
        self.running = False

    def run(self):
        self.running = True
        self.cam_proc = subprocess.Popen(raspivid,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

class Stream(Thread):
    def __init__(self, cam):
        self.cam = cam
        self.stdout = None
        self.stderr = None
        self.running = False
        Thread.__init__(self)

    def stop(self):
        """Stop the stream."""
        self.stream_proc.terminate()
        sleep(0.5)
        self.stream_proc.kill()
        self.running = False

    def run(self):
        self.running = True
        self.stream_proc = subprocess.Popen(ffmpeg,
                shell=False,
                #stdout=subprocess.PIPE,
                #stderr=subprocess.PIPE,
                stdin=self.cam.cam_proc.stdout)
        #self.stdout, self.stderr = self.stream_proc.communicate()

"""
try:
    cam = Camera()
    cam.start()
    sleep(0.1)
    stream = Stream(cam)
    stream.start()
    #sleep(60)
    #stream.stop()
    #cam.stop()
    #print(stream.stderr)
    stream.join()
    cam.join()
except KeyboardInterrupt:
    print("Keyboard interrupt received, stopping threads")
    stream.stop()
    cam.stop()
"""

