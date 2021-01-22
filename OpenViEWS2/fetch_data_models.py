import os
print('getting the data from s3. This will take maybe two hours')
os.system(f'mkdir $PWD/storage')
os.system(f'mkdir $PWD/storage/predictions')
os.system(f'wget -O data.zip https://world-modelers.s3.amazonaws.com/data/views2/storage/data.zip  && unzip $PWD/data.zip -d $PWD/storage/ && rm -rf $PWD/data.zip')
print('finished')

