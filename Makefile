.PHONY: docs build

gitrcommit:
	git config --global credential.helper store
	# git add -u
	-git add src/*
	-git add src/*/*
	-git add src/*/*/*
	-git add src/*/*/*/*
	-git add doc Makefile
	-git commit -a -m "`date`"
	git pull
	git push origin HEAD
gitrupdate:
	git config --global credential.helper store
	git pull
build:
	colcon build

rosbridge:
	ros2 launch rosbridge_server rosbridge_websocket_launch.xml

