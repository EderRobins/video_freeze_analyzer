from videos_freeze_analyzer import VideosFreezeAnalyzer
from video_valid_points_list_generator import dowload_url
from video_valid_points_list_generator import VideoValidPointsListGeneratorFfmpeg
from video_freeze_analyzer import VideoFreezeAnalyzer

import json

def main(urls):
    files = []
    for url in urls:
        files.append(dowload_url(url))
    
    videos_list =[]
    for file_name in files:
        video_valid_list = VideoValidPointsListGeneratorFfmpeg(file_name).generate_valid_points_list()
        videos_list.append(VideoFreezeAnalyzer().analyze(video_valid_list))
    
    videos_output = VideosFreezeAnalyzer(videos_list).analyze()
    results = json.dumps(videos_output, indent=4)
    print(results)

if __name__ == '__main__':
    urls = ["https://storage.googleapis.com/hiring_process_data/freeze_frame_input_a.mp4",
            "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_b.mp4",
            "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_c.mp4"]
    

    main(urls)    

            