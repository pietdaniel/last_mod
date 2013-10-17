import shlex, subprocess, re, sys, csv, datetime
#takes a website
#writes a csv of format url, last-modified
def link_lmod(site):
	cmd = 'wget --recursive --force-html "'+site+'" --no-parent --delete-after -S -nv --accept html'
	args = shlex.split(cmd)
	output,error = subprocess.Popen(args,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
	date_list = []
	site_list = []
	for line in error.split("\n"):
		date = re.search('Last-Modified: (.*)', line)
		site = re.search('URL:(.\S*)', line)
		if date:
			d = datetime.datetime.strptime(date.group(1), '%a, %d %b %Y %H:%M:%S GMT')
			date_list.append(d.strftime('%x %X'))
		if site:
			site_list.append(site.group(1))
	with open('rasala_links.csv', 'wb') as f:
		if (len(date_list)==len(site_list)):
			for i in range(len(date_list)):
				f.write(site_list[i]+","+date_list[i]+"\n")
		else:
			f.write("Mismatched urls and timestamps\n")
