import os
import shutil
import subprocess

# Set the current working directory
current_dir = os.getcwd()

# Define some variables
server_name = 'PubicTemplates'
qr_codes_dir = f'{current_dir}/QRImages'
user_template_dir = f'{current_dir}/UserTemplates'
nginx_conf_file = '/etc/nginx/nginx.conf'

# Create the directories and copy the files
if not os.path.exists(qr_codes_dir):
    os.makedirs(qr_codes_dir)
shutil.copytree('templates', templates_dir)

# Configure Nginx
with open(nginx_conf_file, 'a') as f:
    f.write(f'''
    server {{
        listen 80;
        server_name {server_name};

        root /var/www/html;
        index index.html;

        location /qrCodes {{
            types {{
                image/svg+xml svg;
            }}
        }}

        location /UserTemplates {{
            # Serve HTML files as text/html
            types {{
                text/html html;
            }}
        }}
    }}
    ''')

# Restart Nginx to apply the new configuration
subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])
