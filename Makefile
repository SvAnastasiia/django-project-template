macos_setup:
	chmod +x setup/macos_setup/install_components.sh
	chmod +x setup/macos_setup/start_services.sh
	setup/macos_setup/install_components.sh
	setup/macos_setup/start_services.sh

ubuntu_setup:
	chmod +x setup/ubuntu_setup/install_components.sh
	chmod +x setup/ubuntu_setup/setup_db.sh
	chmod +x setup/ubuntu_setup/start_redis.sh
	setup/ubuntu_setup/install_components.sh
	setup/ubuntu_setup/setup_db.sh
	setup/ubuntu_setup/start_redis.sh

start_app:
	chmod +x setup/start_app.sh
	setup/start_app.sh
