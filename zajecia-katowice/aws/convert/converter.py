import os
from moviepy.editor import AudioFileClip

input_dir_path = r'C:\Users\jk\PycharmProjects\machine-learning_learning\zajecia-katowice\aws\resources\avi'
output_dir_path = r'C:\Users\jk\PycharmProjects\machine-learning_learning\zajecia-katowice\aws\resources\mp3\blizniaki'

for file_name in os.listdir(input_dir_path):
    input_file_path = r'{}\{}'.format(input_dir_path, file_name)
    audioclip = AudioFileClip(input_file_path)
    base_name = os.path.splitext(file_name)[0]
    output_file_path = r'{}\{}.mp3'.format(output_dir_path, base_name)
    audioclip.write_audiofile(output_file_path)
    audioclip.close()

print('koza')
