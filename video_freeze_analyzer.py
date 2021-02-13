class VideoFreezeAnalyzer(object):
        
    def analyze(self,valid_period_list):
        longest_valid_period = 0
        total_valid_video_period = 0
        for valid_video_period in valid_period_list:
            valid_video_period =  valid_video_period[1]- valid_video_period[0]
            #add to total
            total_valid_video_period += valid_video_period
            #update max
            if longest_valid_period < valid_video_period:
                longest_valid_period = valid_video_period
        #calculate precentage
        valid_video_percentage = total_valid_video_period/valid_period_list[-1][1]*100
        video_dict ={
            "longest_valid_period": longest_valid_period,
            "valid_video_percentage": valid_video_percentage,
            "valid_periods":valid_period_list
        }
        return video_dict
