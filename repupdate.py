#! /usr/bin/env python

import os, sys
from subprocess import call

gitpath = sys.argv[1] if len(sys.argv) > 1 else os.environ['HOME'] + '/git'

print gitpath
exit()

dirlist = []

def walkdir(rootpth, lvl = 1):
	""" Walk the directory tree; similar to os.walk but uses a 'lvl' variable for recursion level."""
	
	rootpth = rootpth.rstrip(os.path.sep)
	assert os.path.isdir(rootpth)
	num_sep = rootpth.count(os.path.sep)
	for root, dirs, files in os.walk(rootpth):
		yield root, dirs, files
		num_sep_this = root.count(os.path.sep)
		if num_sep + lvl <= num_sep_this:
			del dirs[:]

	
def verifyrepo(pth):
 	""" This function verifies if the current (single) directory is a git repository.
	
	Basically, what it checks for is the presence of the .git directory and if not found 
	it assumes the dir isn't a git repo. This is somewhat flawed as I could create an 
	empty .git repo and it thinks the repo is a git repo. """

	try:
		assert os.path.isdir(pth)
	except AssertionError:
		print "It seems the value specified is not a DIRECTORY\n\nExiting!"
	if not '.git' in os.listdir(pth):
		return False
	else:
		return True


def pullremote(gitrepo, myname):
	""" This function will be called on a directory and  to run the 'git pull' command to \
	pull down the latest updates from the remote git repo. """
	
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "\n%s is being updated\n" % myname
	pullcmd = "git --git-dir=%s/.git --work-tree=%s pull" % (gitrepo, gitrepo)
	call(pullcmd, shell=True)
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "\n"

if __name__ == '__main__':
	for rootdir, dirs, files in walkdir(gitpath):
		dirlist.append(rootdir)

	root = dirlist[0]		# A reference to the root directory
	repos = dirlist[1:]		# ..list reference to the subdirectories
	for repo in repos:
		try:
			assert verifyrepo( repo )
		except AssertionError:
			print "The Directory %s, is not a git repo" % repo
			continue

		reponame = repo.split('/')[-1]
		_name = reponame.title()
		pullremote(repo, _name)

