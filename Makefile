.PHONY: docs

gitrcommit:
	git config --global credential.helper store
	# git add -u
	-git add sumumo/*

	-git commit -a -m "`date`"
	git pull
	git push origin HEAD
gitrupdate:
	git config --global credential.helper store
	git pull
