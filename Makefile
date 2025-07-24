.PHONY: firewall copy_services enable_services start_services message all

UBUNTU_2204_SYSTEMD_DIR = /etc/systemd/system

all: firewall copy_services enable_services start_services message

firewall:
	@echo "Setting up firewall rules..."
	ufw enable
	ufw allow 5000
	ufw allow 8050
	ufw reload
	ufw status verbose
	@echo "Firewall rules set for ports 5000 and 8050."

copy_services:
	cp -v dash_app.service $(UBUNTU_2204_SYSTEMD_DIR)/dash_app.service
	cp -v quart_app.service $(UBUNTU_2204_SYSTEMD_DIR)/quart_app.service

start_services:
	systemctl daemon-reload
	systemctl start dash_app
	systemctl start quart_app

enable_services:
	systemctl enable dash_app
	systemctl enable quart_app

message:
	@echo "\n"
	@echo "Services copied to $(UBUNTU_2204_SYSTEMD_DIR) and enabled."
	@echo "Type 'sudo systemctl status dash_app' or 'sudo systemctl status quart_app' to check the status of the services."



