## Start project 

clone project_name to /var/www/html

```
server {
    listen 80 ;
    server_name localhost;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
}
}

```

install requirement: 
```
pip3 install flask googletrans wsgiref pyyaml
```

change api_key use following command:
```
sed -i "s/api_key =.*/api_key = {key}/g" /var/www/html/back_end.py

python3 /var/www/html/back_end.py
```