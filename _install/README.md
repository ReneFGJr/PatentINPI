
Crie o arquivo
 sudo nano /etc/systemd/system/fastapi.service

Ajuste o caminho do aplicativo

    sudo systemctl daemon-reload
    sudo systemctl enable fastapi
    sudo systemctl start fastapi
    sudo systemctl status fastapi
