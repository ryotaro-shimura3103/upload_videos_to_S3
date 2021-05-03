import os
import sys
import glob
import shutil
import time
from send_mail import *

# set variables
one_drive_path = os.environ["one_drive_path"]

def get_videos_from_one_drive(video_files_path):
    # if there is not a temp folder, create a temp folder
    if not (os.path.exists('./tmp')):
        os.makedirs('./tmp')   
    # get files whose extensions match with '.MOV' from One Drive
    video_files = glob.glob(video_files_path)
    print(video_files)
    # copy(move) video files from One Drive to ./tmp
    for video_file in video_files:
        shutil.move(video_file,'./tmp')
    
def main():
    start = time.time()
    ### download videos from One Drive and store in ./tmp
    get_videos_from_one_drive(one_drive_path)
    ### upload videos to S3 ###

    ### send an email to notify the result of the job ###
    success = False
    if success:
        job_result = 'completed!'
        mail_body = 'The job worked without problems.\n\nVideo files have been successfully uploaded to S3.'
    else:
        job_result = 'failed'
        mail_body = 'The job does not seem to have worked well.\n\nThere should be something wrong with it.'
    # send_email(job_result, mail_body)
    ### delete ./tmp

    elapsed_time = time.time() - start
    print(elapsed_time)

if __name__ == '__main__':
    main()