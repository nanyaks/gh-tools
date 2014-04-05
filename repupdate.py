#! /usr/bin/env python

import os, sys
from subprocess import call

# The code expects me to type the full path to the git repo.
# Note to self: refactor this code to accept all direcrories relative to the 'home' directory

gitpath = sys.argv[1] if len(sys.argv) > 1 else os.environ['HOME'] + '/git'
dirlist = []

def walkdir(rootpth, lvl = 1):
	""" Walk the directory tree.
	
	Similar to os.walk but uses a 'lvl' variable for recursion level.
	"""

	rootpth = rootpth.rstrip(os.path.sep)
	try:
		assert os.path.isdir(rootpth)
	except AssertionError:
		print "'%s' is not a directory.\nExiting!" % rootpth
		sys.exit()
	#
	num_sep = rootpth.count(os.path.sep)
	gitfound = []
	for root, dirs, files in os.walk(rootpth):
		yield root, dirs, files

		if '.git' in dirs:
			gitfound.append(root)
			del dirs[:]


def pullremote(gitrepo, dirname):
	""" This function will be called on a directory and  to run the 'git pull' command to \
			pull down the latest updates from the remote git repo. """
	print "==================================================================="
	print "\n%s is being updated\n" % dirname
	pullcmd = "git --git-dir=%s/.git --work-tree=%s pull" % (gitrepo, gitrepo)
	call(pullcmd, shell=True)
	print "==================================================================="
	print "\n"


if __name__ == '__main__':
	for rootdir, dirs, files in walkdir(gitpath):
		dirlist.append(rootdir)

		# A reference to the root directory
		root = dirlist[0]
		# ..reference subdirectories -- in a list
		repos = dirlist[1:]

	# now lets do the update for all in (list)repos
	for repo in repos:
		_dirname = os.path.basename(repo)
		pullremote(repo, _dirname)
		#print(repo)
