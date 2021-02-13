import urllib.request
from urllib.parse import urlparse
import ssl
import os
from abc import ABC, abstractmethod

ssl._create_default_https_context = ssl._create_unverified_context

def dowload_url(url):
    file_name = os.path.basename(urlparse(url).path)
    urllib.request.urlretrieve(url, file_name)
        
    return file_name

class VideoValidPointsListGenerator(object):

    def __init__(self, file_name):
        self.file_name = file_name

    @abstractmethod
    def generate_valid_points_list(self):
        pass

class VideoValidPointsListGeneratorFfmpeg(VideoValidPointsListGenerator):

    def __init__(self, file_name):
        super().__init__(file_name)
    
    def generate_valid_points_list(self):
        os.system('ffmpeg -i {file_name} -vf "freezedetect=n=0.003,metadata=mode=print:file={file_name}.txt" -map 0:v:0 -f null -'.format(file_name=self.file_name))
        os.system('ffprobe -i {file_name} -show_entries format=duration -v quiet -of csv="p=0" > {file_name}.duration'.format(file_name=self.file_name))   
        
        valid_period_list = []
        valid_period = [0]
        with open('{file_name}.txt'.format(file_name=self.file_name), 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                if line.startswith('lavfi.freezedetect.freeze_start='):
                    if len(valid_period) == 1:
                        number = line[len('lavfi.freezedetect.freeze_start='):]
                        valid_period.append(float(number))
                        valid_period_list.append(valid_period)
                        valid_period = []
                    else:
                        fp.close()
                        raise AssertionError
                if line.startswith('lavfi.freezedetect.freeze_end='):
                    if len(valid_period) == 0:
                        number = line[len('lavfi.freezedetect.freeze_end='):]
                        valid_period.append(float(number))
                    else:
                        fp.close()
                        raise AssertionError
        
        fp.close()
        os.system('rm -f {file_name}.txt'.format(file_name=self.file_name))
        with open('{file_name}.duration'.format(file_name=self.file_name), 'r') as fp:
            number = fp.readline()
            valid_period.append(float(number))
            valid_period_list.append(valid_period)
        fp.close()
        os.system('rm -f {file_name}.duration'.format(file_name=self.file_name))
        
        return valid_period_list                

