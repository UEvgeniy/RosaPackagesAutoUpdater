#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, argparse
import subprocess as sub
import report, parser

def execute(args, sh = False):
	return sub.check_output(args, stderr=sub.STDOUT, shell=sh)
	

def start(login, package, vers):
	
	################ extract items from mib-report ################
	
	print 'Searching for package ' + package + '...'
	
	out = execute(('mib-report', '--search', package))
	

	
	items = parser.extractItems(out)
	
	if len(items) == 0:
		print '### No packages found. Check package name and mib-report for operability ###\n\n'
		return 1
	
	print 'Packages from ' + str(len(items)) + ' distros found, comparing versions...'
	
	################ compare versions ################
	oldVersion = parser.getRosaVersion(items)
	if oldVersion == None:
		print '### Rosa package not found. Updating is impossible ###\n\n'
		return 0
	maxItem = max(items)
	if 'rosa' in maxItem.distro.lower():
		print '### Rosa has the latest version of package ###\n\n'
		return 0
		
	################ download the latest package ################
	print maxItem.distro[:-1] + ' with latest version ('+ maxItem.version + ') detected...'
	
	fileName = maxItem.url.split('/')[-1]
	pack = urllib.urlopen(maxItem.url).read()
	file = open(fileName, 'wb')
	file.write(pack)
	file.close()
	
	print fileName + ' is downloaded...'
	
	################ fork and get ABF project ################
	
	out = execute(('abf', 'fork', 'import/'+ package, login +'/' + package))
	print 'Forking was successful...'
	
	execute(('abf', 'get', login + '/' + package, '-b', vers))
	print 'Project cloned to machine...'
	
	################ Extract files from RPM archive and move them to Rosa project dir ################
	
	out = execute('rpm2cpio ' + fileName + ' | cpio -idmv', True).split()
	extFileNames = list(filter(lambda x: x.endswith(('gz', 'bz2', 'xz')), out))
	
	print 'Unzipped files replaced to Rosa project:'
	for file in extFileNames:
		execute(('mv', file, package))
		print file
	
	################ Delete archive and its extracted spec file ################
	
	execute(('rm', '-f', fileName))
	execute(('rm', '-f', package + '.spec'))
	print 'Unnecessary files was removed...'
		
	
	################ Read spec file and change version tag ################
	parser.replaceInFile(
		open(package + '/' + package + '.spec', "r+"), 
		oldVersion, 
		maxItem.version)
		
	
	################ Build project ################
	spec = package + '/' + package + '.spec'
	
	execute(('sudo', 'urpmi', spec))
	print 'Installing necessary packages finished (urpmi)...'
	
	execute(('sudo', 'rpmbuild', '-bb', spec))
	print 'Installing necessary packages finished (rpmbuild).'
	
	print '### Package ' + package + ' updated successfully! ###\n\n'
	
	return 0

	
# main method
if __name__ == '__main__':
	
	################ Parser for command-line options, arguments ################
	arg_parser = argparse.ArgumentParser(description='Updates rosa packages.', 
									 usage='auto-updater.py login package [-v <version>] [-h]')
	arg_parser.add_argument('login', metavar='login',   help='ABF login')
	arg_parser.add_argument('package',   metavar='package', help='Package name')
	arg_parser.add_argument('-v', metavar='version', default='rosa2016.1', 
							help= 'Rosa version (default rosa2016.1)')
	pargs =  arg_parser.parse_args()
	
	start(pargs.login, pargs.package, pargs.v)
	
	