#!/usr/bin/python

import sys, argparse, subprocess, auto_updater

################ Parser for command-line options, arguments ################

arg_parser = argparse.ArgumentParser(description='Updates rosa packages from file.', 
									 usage='upd-fromfile.py login packages [-v <version>] [-h]')

arg_parser.add_argument('login', metavar='login',   help='ABF login')
arg_parser.add_argument('file',   metavar='file', help='File with package names')
arg_parser.add_argument('-v', metavar='version', default='rosa2016.1', 
						help= 'Rosa version (default rosa2016.1)')

pargs =  arg_parser.parse_args()

################ Read package names ################

f = open(pargs.file, 'r+')
packages = f.read().splitlines()
f.close()

################ Update each package and print log ################
for package in packages:
	try:
		auto_updater.start(pargs.login, package, pargs.v)
	except subprocess.CalledProcessError, e:
		print e.output
		print '### Updating ' + package + 'is finished with error ' + str(e.returncode) + ' ###\n\n'



