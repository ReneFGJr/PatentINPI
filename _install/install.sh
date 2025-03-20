echo "Copiando arquivo"
cp fastapi.service /etc/systemd/system/fastapi.service

echo "Ativando o serviço"

sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
sudo systemctl status fastapi