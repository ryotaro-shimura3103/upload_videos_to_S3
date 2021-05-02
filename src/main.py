from send_mail import *

def main():
    ### process to upload videos to S3 ###

    ### send an email to notify the result of the job ###
    success = False
    if success:
        job_result = 'completed!'
        mail_body = 'The job worked without problems.\n\nVideo files have been successfully uploaded to S3.'
    else:
        job_result = 'failed'
        mail_body = 'The job does not seem to have worked well.\n\nThere should be something wrong with it.'
    send_email(job_result, mail_body)



if __name__ == '__main__':
    main()