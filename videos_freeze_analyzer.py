
class VideosFreezeAnalyzer(object):

    def __init__(self,videos_list,sync_resultion=0.5):
        self.sync_resultion = sync_resultion
        self.videos_list = videos_list
    
    def analyze(self):
        all_videos_freeze_frame_synced = self._check_videos_sync()
        
        videos_output = {
        "all_videos_freeze_frame_synced":all_videos_freeze_frame_synced,
        "videos":self.videos_list,  
        }
        return videos_output

    def _check_videos_sync(self):
        if len(self.videos_list) < 2:
            return True
        valid_period_range_list = []
        #fill valid period range list
        for period_point in self.videos_list[0]["valid_periods"]:
            valid_period_range_list.append([[period_point[0]-self.sync_resultion,period_point[0]+self.sync_resultion],
                                            [period_point[1]-self.sync_resultion,period_point[1]+self.sync_resultion]])
        
        #run over list, check and update sync range 
        for video in self.videos_list[1:]:
            #check number of items
            if len(video["valid_periods"]) != len(valid_period_range_list):
                return False
            #iterate over each period an and range in lists
            for valid_period,valid_period_range in zip(video["valid_periods"],valid_period_range_list):
                #check low and high points in period
                for period_point, period_range_points in zip(valid_period,valid_period_range):
                    #check range
                    if period_point < period_range_points[0] or period_point > period_range_points[1]:
                        return False
                    #update min range
                    elif period_point > period_range_points[0] + self.sync_resultion:
                        period_range_points[0] = period_point -  self.sync_resultion;
                    #update max range
                    elif period_point < period_range_points[1] - self.sync_resultion:
                        period_range_points[1] = period_point +  self.sync_resultion;
        return True