import os
import sys
import glob
import shutil
import time
import subprocess
import boto3
from send_mail import *

# set variables
one_drive_path = os.environ["one_drive_path"]
bucket_name = os.environ["bucket_name"]
s3 = boto3.client('s3')

def get_videos_from_one_drive(video_files_path):
    # if there is not a temp folder, create a temp folder
    if not (os.path.exists('./tmp')):
        os.makedirs('./tmp')   
    # get files whose extensions match with '.MOV' from One Drive
    video_files = glob.glob(video_files_path)
    print(video_files)
    # move video files from One Drive to ./tmp
    for video_file in video_files:
        shutil.move(video_file,'./tmp')

def convert_mov_into_mp4():
    # get videos from ./tmp
    mov_videos = glob.glob('./tmp/*')
    # convert their extensions into .mp4
    for video in mov_videos:
        video_name = video[0:-4]
        cmd = f"ffmpeg -i {video} -strict -2 {video_name}.mp4"
        subprocess.call(cmd, shell=True)

def get_latest_modifed_file_fromS3(bucket_name):
    # retrieve the infromation of datetime when objects were updated last
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%Y%m%d'))
    objs = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    # put objects into list and sort them by updated time  
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][-1]

    return last_added

def count_S3objects_with_specific_prefix(bucket_name,last_updated_file):
    # get the latest folder name
    top_level_prefix = os.path.dirname(last_updated_file)
    objects = s3.list_objects(Bucket=bucket_name, Prefix=top_level_prefix)['Contents']
    # count the number of objects with top_level_prefix
    count = len(objects)

    return top_level_prefix, count

def upload_up_to_50objects(count, video_paths, videos, start_number, end_number, folder_name):
    for video_path,video in zip(video_paths,videos):
        if (count % 50) == 0:
            start_number = end_number + 1
            end_number = start_number + 49
            folder_name = f'{start_number}-{end_number}'
        else:
            pass
        file_prefix = f'{folder_name}/{video}'
        s3.upload_file(video_path, bucket_name, file_prefix)
        count += 1
        elapsed_time = time.time()-start_time

def upload_videos_to_S3(bucket_name):
    # get videos from ./tmp
    video_paths = glob.glob('./tmp/*.mp4')
    videos = []
    # retrieve file names from video_paths 
    for video_path in video_paths:
        videos.append(os.path.basename(video_path))
    # judge whether this program has been executed before 
    first_try = False
    try:  
        last_updated_file = get_latest_modifed_file_fromS3(bucket_name)
        top_level_prefix, count = count_S3objects_with_specific_prefix(bucket_name,last_updated_file)
        start_number, end_number = top_level_prefix.split('-')
    except Exception as e:
        first_try = True
        start_number = 33
        end_number = 50
        count = 33
    # set a floder name(top level prefix in S3 key)
    folder_name = f'{start_number}-{end_number}'
    # upload videos to AWS S3
    upload_up_to_50objects(count, video_paths, videos, start_number, end_number, folder_name)
    



def main():
    try:
        start = time.time()
        ### download videos from One Drive and store in ./tmp
        # get_videos_from_one_drive(one_drive_path)
        ### convert the extensions of video
        # convert_mov_into_mp4()
        ### upload videos to S3 ###
        upload_videos_to_S3(bucket_name)
        ### delete ./tmp ###
        print('続きはここから（別ブランチで！）')
        elapsed_time = (time.time() - start)/60
        print(elapsed_time)
        ### send an email to notify the result of the job ###
        job_result = 'completed!'
        mail_body = f'The job worked without problems.\nVideo files have been successfully uploaded to S3.\nprocessing time : {elapsed_time} min'
        # send_email(job_result, mail_body)  
    except Exception as e:
        ## send an email to notify the result of the job ###
        job_result = 'failed'
        mail_body = f'The job does not seem to have worked well.\nThere should be something wrong with it.\nThe error message is shown below\n{e}'
        # send_email(job_result, mail_body)
        sys.exit(1)


if __name__ == '__main__':
    main()