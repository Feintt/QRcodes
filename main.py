import csv
import os
import qrcode
import shutil
from time import sleep

# Set the current working directory
current_dir = os.getcwd()

print(f'# Current working directory: {current_dir}')
print(f'# Any directory called "UserTemplates" or "QRImages" will be deleted and recreated')
sleep(5)

# Set the path to the CSV file
csv_path = f'{current_dir}/InfoExcel.csv'

# Set the paths to the directories for templates and user templates
template_dir = f'{current_dir}/template'
user_template_dir = f'{current_dir}/UserTemplates'
qr_codes_dir = f'{current_dir}/QRImages'

# Delete the user templates directory if it exists and create it again
if os.path.exists(user_template_dir):
    shutil.rmtree(user_template_dir)
try:
    os.makedirs(user_template_dir)
except OSError:
    print (f'#! Creation of the directory {user_template_dir} failed')
else:
    print (f'# Successfully created the directory {user_template_dir}')


# Delete the QR codes directory if it exists and create it again
if os.path.exists(qr_codes_dir):
    shutil.rmtree(qr_codes_dir)
try:
    os.makedirs(qr_codes_dir)
except OSError:
    print (f'#! Creation of the directory {qr_codes_dir} failed')
else:
    print (f'# Successfully created the directory {qr_codes_dir}')

# Open the CSV file
with open(csv_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Extract the user information from the row
        user = row['Student']
        university = row['University']
        role = row['Role']
        qr_id = row['qrID']
        
        # Create the URL for the user template directory
        url = f'https://e47a-187-191-36-180.ngrok-free.app/UserTemplates/{qr_id}'
        
        # Generate the QR code image
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        
        # Save the QR code image
        qr_path = os.path.join(qr_codes_dir, f'{qr_id}.svg')
        with open(qr_path, 'wb') as qr_file:
            img.save(qr_file)
        
        # Copy the template directory for the user
        user_template_path = os.path.join(user_template_dir, qr_id)
        shutil.copytree(template_dir, user_template_path)
        
        # Update the template files with user information
        index_file = os.path.join(user_template_path, 'index.html')
        with open(index_file, 'r') as f:
            content = f.read()
        content = content.replace('{user}', user)
        content = content.replace('{university}', university)
        content = content.replace('{role}', role)
        with open(index_file, 'w') as f:
            f.write(content)
