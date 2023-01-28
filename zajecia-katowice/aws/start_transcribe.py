import os

import boto3

bucket_name = 'jakub-krzemien'
script_version = 6

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe', 'us-east-1')
response = s3.list_objects_v2(
    Bucket=bucket_name,
)


def get_video_name(path):
    path = os.path.splitext(path)[0]
    return path[path.rindex('/') + 1:]


for object_summary in response['Contents']:
    if object_summary['Key'].startswith('subt/') and object_summary['Size'] > 0:
        res_name = object_summary['Key']
        job_uri = "s3://{}/{}".format(bucket_name, res_name)
        video_name = get_video_name(res_name).replace(' ', '_').replace(',', '').replace('\'', '').replace('#', '')\
            .replace('&', '').replace('[', '').replace(']', '')
        job_name = '{}-{}'.format(video_name, script_version)
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={
                'MediaFileUri': job_uri
            },
            OutputBucketName='jakub-krzemien',
            OutputKey='subt-res/{}'.format(video_name),
            LanguageCode='en-US',
            Subtitles={
                'Formats': [
                    'vtt', 'srt',
                ],
                'OutputStartIndex': 1
            },
        )

# print(get_video_name('subt/Episode 12 - To Mar a Stall.mp3'))
