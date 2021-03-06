#!/usr/bin/python3
#encoding : utf8

import os
import time
import sys
import subprocess
import pwd

print("                 						 `/-          ")
print("                                     .oy-              ")
print("                                   -sd/  `-+o:         ")
print("                              -  -sds../sdh/`          ")
print("                             o+`+hh//shhy/`            ")
print("                            /y-syyoyyyy/`              ")
print("                           -ysyyyyyyy+`                ")
print("                          `syyyyyyyo.                  ")
print("                          /yyyyyys:                    ")
print("                         `syyyyy+`                     ")
print("                      .` :yyyys-                       ")
print("                     `.dhyysso.                        ")
print("                      `+MMmymy. `                      ")
print("                       `NMmhNN- `                      ")
print("                      ``mMmhhNs `                      ")
print("                      `yMMmyhhms.``                    ")
print("                    `/dMMmmyNyhmdo-``                  ")
print("               ` `-smNMMNmmsNNssddhs:.                 ")
print("              `-odNMMMMNhNmsdMNo+hhhhys/. `            ")
print("           `-odNMMMNNNmsdNdhsNNN+/yyyyyyyo-`           ")
print("         `:hNMMNNNNmhsymNNdydoNNN:/yyyyyyyyo-` `       ")
print("      ` -hNMNNNNmhsshmNNNNdyNhomNm.osssssssss+. `      ")
print("     ` +NNNNNNdsshmNNNNNNhdoNNh+mNs-ooooooooooo- `     ")
print("    ` sNNNNNdsydNNNNmmmmhhh/hmmh+mm.+ooooooooooo- `    ")
print("   ` +NNNNNssmNNNmmmmmdhhmhs+dmmssm:-++++++++++++. `   ")
print("    `NNNNN/yNNNmmmmdyyhmmmhsh+dmm/m/`////////+//// `   ")
print("  ` /NNNNo+NNmmmmyoydmddddhsdd/dmoy+ /////////////`    ")
print("    +NNNN.dNmmmd+sdmddddddy+ddy/dyo+ :////////////` `  ")
print("  ` /NNNN.mmmmh/dmddddddyoy+sdd:yy// :::::::::::::`    ")
print("    `mNNN/hmmm:hmddddddo+hys-hdoos+: ::::::::::::-     ")
print("   ` +NNNh:mmd.mmddddds/hhys:sdo++o``------------` `   ")
print("    ` sNNNo+mm.dmddddd-hhhyo+/hoo:s `-----------.      ")
print("     ` omNm+omoodddddd-ddhyso:d/o-/ ...........` `     ")
print("      ` -hmmo/d/oddddd.hddys//d./o` ..........` `      ")
print("       ```/dmy:y+/hdddo/ddys.so::: `.......`` ``       ")
print("          ``:ydo+s:/hddo/hh/.h:.- ````````  ``         ")
print("             ``:+/+o///so//`/-`  ``````   `            ")
print("                `  ``.-. ``        `                   ")
print("                          `  `     				      ")
print("		OnionPi v1.1\n 	by Tom ESCOLANO - www.tomescolano.com\n")

if(os.geteuid() != 0):
    sys.exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

if(len(sys.argv) > 1):

	if(sys.argv[1] == "-h" or sys.argv[1] == "--help"):
		sys.exit("Usage:\n-h --help	Print Help\n-b --bridge	Install a Tor Bridge\n-r --relay 	Install a Tor Relay\n-s --service	Install a Tor Hidden Service")

	elif(sys.argv[1] == "-b" or sys.argv[1] == "--bridge"):
		start()
		bridge()

	elif(sys.argv[1] == "-r" or sys.argv[1] == "--relay"):
		start()
		relay()

	elif(sys.argv[1] == "-s" or sys.argv[1] == "--service"):
		start()
		hidden()
	else:
		sys.exit("Usage:\n-h --help	Print Help\n-b --bridge	Install a Tor Bridge\n-r --relay 	Install a Tor Relay\n-s --service	Install a Tor Hidden Service")

else:
	sys.exit("Usage:\n-h --help	Print Help\n-b --bridge	Install a Tor Bridge\n-r --relay 	Install a Tor Relay\n-s --service	Install a Tor Hidden Service")


###############################################################################################


def start():
	print("-----| Welcome to OnionPi! |-----")
	print("[*] Updating your computer")
	os.system("apt-get update && apt-get upgrade")

	if(not os.path.exists("/etc/tor/")):

		print("[*] Installing Tor")

		os.system("apt-get install tor")

	try:

		pwd.getpwnam('tor')

	except KeyError:

		print("[*] Creating Tor user")
		os.system("adduser tor")
		os.system("echo 'tor ALL=(ALL) ALL' >> /etc/sudoers")

	print("[*] Stopping Tor")
	os.system("service tor stop")
	print("[*] Creating a backup of the torrc file")
	os.system("cp /etc/tor/torrc /etc/tor/torrc.bak")
	os.system("echo -n "" > /etc/tor/torrc")
	os.system("clear")


###################################################################################################


def relay():

	os.system("clear")
	print("-----| TOR RELAY SETUP |-----")
	if(str(os.system("cat /etc/tor/torrc | grep 'ORPort 9001'") != "" and os.system("cat /etc/tor/torrc | grep 'DirPort 9030'") != "")):

		sys.exit("[!] OnionPi detected that you already run a Tor Relay on your computer. Quitting.")
	
	elif(os.path.exists("/var/lib/tor/hidden_service/hostname")):
	
		sys.exit("[!] OnionPi detected that you already installed a Hidden Service on your machine. It's too dangerous to run a Hidden Service and a Relay on the same machine. Quitting.")
	else:
		name = ""
		while(name == ""):
			name = input("[?] What name do you want to give to your relay?: ")
		os.system("echo 'Nickname " + name + "' >> /etc/tor/torrc")
		
		band = 0
		while(band <= 0 or band > 10000):
			band = int(input("[?] How much do you want allocate bandwith to your relay? (in Kb/s): "))
		
		print("[*] Setting up default values for the relay")
		os.system("RelayBandwidthRate " + band + " KB' >> /etc/tor/torrc")
		os.system("RelayBandwidthBurst " + band + " KB' >> /etc/tor/torrc")
		os.system("echo 'SocksPort 0' >> /etc/tor/torrc")
		os.system("echo 'Log notice file /var/log/tor/notices.log' >> /etc/tor/torrc")
		os.system("echo 'RunAsDaemon 1' >> /etc/tor/torrc")
		os.system("echo 'ORPort 9001' >> /etc/tor/torrc")
		os.system("echo 'DirPort 9030' >> /etc/tor/torrc")
				
		ex = ""
		while(ex == ""):
		
			ex = input("[?] Do you want to run your relay as an exit relay? (Dangerous for personnal devices and domestic networks) (Y/N): ")
		
		if(ex == "Y" or ex == "y"):
		
			print("[*] Setting up as an exit relay")
			os.system("echo 'ExitPolicy accept *:20-23     # FTP, SSH, telnet' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:43        # WHOIS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:53        # DNS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:79-81     # finger, HTTP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:88        # kerberos' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:110       # POP3' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:143       # IMAP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:194       # IRC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:220       # IMAP3' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:389       # LDAP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:443       # HTTPS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:464       # kpasswd' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:531       # IRC/AIM' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:543-544   # Kerberos' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:554       # RTSP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:563       # NNTP over SSL' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:636       # LDAP over SSL' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:706       # SILC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:749       # kerberos ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:873       # rsync' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:902-904   # VMware' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:981       # Remote HTTPS management for firewall' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:989-995   # FTP over SSL, telnets, IMAP over SSL, etc' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1194      # OpenVPN' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1220      # QT Server Admin' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1293      # PKT-KRB-IPSec' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1500      # VLSI License Manager' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1533      # Sametime' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1677      # GroupWise' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1723      # PPTP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1755      # RTSP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1863      # MSNP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2082      # Infowave Mobility Server' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2083      # Secure Radius Service (radsec)' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2086-2087 # GNUnet, ELI' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2095-2096 # NBX' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2102-2104 # Zephyr' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:3128      # SQUID' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:3389      # MS WBT' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:3690      # SVN' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:4321      # RWHOIS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:4643      # Virtuozzo' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5050      # MMCC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5190      # ICQ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5222-5223 # XMPP, XMPP over SSL' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5228      # Android Market' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5900      # VNC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:6660-6669 # IRC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:6679      # IRC SSL  ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:6697      # IRC SSL  ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8000      # iRDMI' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8008      # HTTP alternate' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8074      # Gadu-Gadu' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8080      # HTTP Proxies' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8087-8088 # Simplify Media SPP Protocol, Radan HTTP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8332-8333 # BitCoin' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8443      # PCsync HTTPS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8888      # HTTP Proxies, NewsEDGE' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:9418      # git' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:9999      # distinct' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:10000     # Network Data Management Protocol' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:11371     # OpenPGP hkp (http keyserver protocol)' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:12350     # Skype' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:19294     # Google Voice TCP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:19638     # Ensim control panel' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:23456     # Skype' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:33033     # SkypeExitPolicy accept *:20-23     # FTP, SSH, telnet' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:43        # WHOIS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:53        # DNS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:79-81     # finger, HTTP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:88        # kerberos' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:110       # POP3' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:143       # IMAP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:194       # IRC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:220       # IMAP3' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:389       # LDAP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:443       # HTTPS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:464       # kpasswd' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:531       # IRC/AIM' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:543-544   # Kerberos' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:554       # RTSP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:563       # NNTP over SSL' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:636       # LDAP over SSL' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:706       # SILC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:749       # kerberos ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:873       # rsync' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:902-904   # VMware' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:981       # Remote HTTPS management for firewall' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:989-995   # FTP over SSL, telnets, IMAP over SSL, etc' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1194      # OpenVPN' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1220      # QT Server Admin' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1293      # PKT-KRB-IPSec' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1500      # VLSI License Manager' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1533      # Sametime' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1677      # GroupWise' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1723      # PPTP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1755      # RTSP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:1863      # MSNP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2082      # Infowave Mobility Server' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2083      # Secure Radius Service (radsec)' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2086-2087 # GNUnet, ELI' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2095-2096 # NBX' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:2102-2104 # Zephyr' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:3128      # SQUID' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:3389      # MS WBT' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:3690      # SVN' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:4321      # RWHOIS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:4643      # Virtuozzo' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5050      # MMCC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5190      # ICQ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5222-5223 # XMPP, XMPP over SSL' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5228      # Android Market' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:5900      # VNC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:6660-6669 # IRC' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:6679      # IRC SSL  ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:6697      # IRC SSL  ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8000      # iRDMI' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8008      # HTTP alternate' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8074      # Gadu-Gadu' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8080      # HTTP Proxies' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8087-8088 # Simplify Media SPP Protocol, Radan HTTP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8332-8333 # BitCoin' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8443      # PCsync HTTPS' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:8888      # HTTP Proxies, NewsEDGE' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:9418      # git' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:9999      # distinct' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:10000     # Network Data Management Protocol' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:11371     # OpenPGP hkp (http keyserver protocol)' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:12350     # Skype' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:19294     # Google Voice TCP' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:19638     # Ensim control panel' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:23456     # Skype' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy accept *:33033     # Skype ' >> /etc/tor/torrc")
			os.system("echo 'ExitPolicy reject *:*' >> /etc/tor/torrc")
			
		else:
		
			os.system("ExitPolicy reject *:*' >> /etc/tor/torrc")
			
		arm = ""
		while(arm != "Y" && arm != "y" && arm != "N" && arm != "n"):
			
			arm = input("[?] Do you want to install Tor-Arm to monitor you relay? (Y/N)\n")
		
		if(arm == "Y" or arm == "y"):

			print("[*] Installing Tor-arm")
			os.system("apt-get install tor-arm")
			
		print("[*] Restarting Tor")
		os.system("service tor restart")		
		print("[!] Done! Your Tor Relay is up and running!")
		
		if(arm == "Y" or arm == "y"):
		
			print("[!] You can check the status of your Relay by running this command:\nsudo -u debian-tor arm\n")

		sys.exit("[!] OnionPi finished his job. Quitting.")



###################################################################################################


def bridge():

	os.system("clear")
	print("-----| TOR BRIDGE SETUP |-----")
	if(str(os.system("cat /etc/tor/torrc | grep 'BridgeRelay 1' ")) != ""):

		sys.exit("[!] OnionPi detected that your Tor service is already running as a Bridge. Quitting.")

	elif(os.path.exists("/var/lib/tor/hidden_service/hostname")):
	
		sys.exit("[!] OnionPi detected that you already installed a Hidden Service on your machine. It's too dangerous to run a Bridge and a Hidden Service on the same machine. Quitting.")

	else:

		pub = ""
		while(pub != "Y" && pub != "y" && pub != "N" && pub != "n"):

			pub = input("[?] Do you want torproject.org to know your bridge? (Y/N): ")

		if(pub == "y" or pub == "Y"):

			os.system("echo 'PublishServerDescriptor 1' >> /etc/tor/torrc")
		
		else:
		
			os.system("echo 'PublishServerDescriptor 0' >> /etc/tor/torrc")
		
		print("[*] Setting up Tor as a Bridge")
		os.system("echo 'SocksPort 0' >> /etc/tor/torrc")
		os.system("echo 'BridgeRelay 1' >> /etc/tor/torrc")
		os.system("echo 'Exitpolicy reject *:*' >> /etc/tor/torrc")

		sys.exit("[!] OnionPi finished his job. Quitting.")



###################################################################################################


def hidden():
	
	os.system("clear")
	print("-----| TOR HIDDEN SERVICE SETUP |-----")
	if(os.path.exists("/var/lib/tor/hidden_service/hostname")):
	
		sys.exit("[!] OnionPi detected that you already installed a Hidden Service on your machine.\nIf you want to reinstall a Hidden Service, simply delete those folders:\n/var/lib/tor/hidden_service/\n/var/www/hidden_service/\nQuitting.")

	elif(str(os.system("cat /etc/tor/torrc | grep 'BridgeRelay 1' ")) != ""):

		sys.exit("[!] OnionPi detected that your Tor service is running as a Bridge. It's too dangerous to run a Hidden Service and a Bridge on the same machine. Quitting.")

	elif(str(os.system("cat /etc/tor/torrc | grep 'ORPort 9001'") != "" and os.system("cat /etc/tor/torrc | grep 'DirPort 9030'") != "")):

		sys.exit("[!] OnionPi detected that you already run a Tor Relay on your computer. It's too dangerous to run a Hidden Service and a Relay on the same machine. Quitting.")
	
	else:
	
		while(custom != "Y" && custom != "y" && custom != "N" && custom != "n"):
	
			custom = str(input("[?] Do you want to generate a custom .onion address? (Can take some hours) (Y/N):\n"))
	
		if(custom == "Y" or custom == "y"):
			
			try:
			
				if(not os.path.exists("/usr/bin/git")):
			
					print("[*] Installing Git")
					os.system("apt-get install git -y")
				
				print("[*] Installing Build-essential to compile Shallot")
				os.system("apt-get install build-essential -y")
				print("[*] Installing Shallot")
				os.system("git clone https://github.com/katmagic/Shallot.git")
				os.system("rm Shallot/CHANGELOG")
				os.system("rm Shallot/LICENSE")
				os.system("rm Shallot/README.asciidoc")
				os.system("cd Shallot && ./configure && make")
				os.system("cd ..")
				print("[*] Shallot successfully installed!")
			
				domain = ""
				while(domain == "" or len(domain) > 5):
			
					domain = str(input("[*] Please enter your desired domain (5 caracters max., calculation time will be too long if it exceed 5 car.):\n"))
			
				print("[*] Beggining generation. It can take several hours.")
				os.system('./Shallot -m ^' + domain + ' > key')
				os.system("cat key | grep -v 'Found' | grep -v '\----------------------------------------------------------------' > ~/private_key")
				os.system("cat key | grep .onion  | awk -vn=22 '{print substr($0,length($0)-n+1)}' > ~/hostname")
				print("[*] Generation finished!")

			except:
			
				print("[*] OnionPi encountered an error during the name generation. Please check the logs and retry.")

		else:

			print("[*] Ok. You saved some time.")

		if(os.path.exists("/usr/sbin/apache2")):

			print("[!] OnionPi need to stop Apache2 to let nginx work properly")
			print("[!] Stopping Apache2")
			os.system("service apache2 stop")

		if(not os.path.exists("/usr/sbin/nginx")):
		
			print("[*] Installing Nginx")
			os.system("apt-get install nginx")
			
			if(os.path.exists("/etc/nginx/sites-available/default")):
				
				os.system("cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak")
				print("[*] Nginx default config file saved under '/etc/nginx/sites-available/default.bak'")
				
		print("[*] Stopping Nginx")
		os.system("service nginx stop")
		os.system("mkdir /var/lib/tor/hidden_service/")
		os.system("mkdir /var/www/hidden_service/")
		
		if(custom == "y" or custom == "Y"):
		
			os.system("rm /var/lib/tor/hidden_service/hostname && mv ~/hostname /var/lib/tor/hidden_service/")
			os.system("rm /var/lib/tor/hidden_service/private_key && mv ~/private_key /var/lib/tor/hidden_service/")
		
		os.system("chown debian-tor:debian-tor -R /var/lib/tor/hidden_service/")
		os.system("chown debian-tor:debian-tor -R /var/www/hidden_service/")
		os.system("echo 'HiddenServiceDir /var/lib/tor/hidden_service/' >> /etc/tor/torrc")
		os.system("echo 'HiddenServicePort 80 127.0.0.1:44480' >> /etc/tor/torrc")
		print("[*] Starting Tor")
		os.system("service tor start")
		
		if(custom != "y" or custom != "Y"):
		
			print("[*] Generating Hostname and Keys")
			time.sleep(4)
		
		else:
		
			time.sleep(2)
		
		os.system("echo '<h1>Your Hidden Service is working!</h1><p>- OnionPi</p>' > /var/www/hidden_service/index.html")
		addr = str(os.popen('cat /var/lib/tor/hidden_service/hostname').read()).rstrip()
		os.system("echo 'server {' > /etc/nginx/sites-available/default")
		os.system("echo '	listen	127.0.0.1:44480;' >> /etc/nginx/sites-available/default")
		os.system("echo '	server_name	" + addr + ";' >> /etc/nginx/sites-available/default")
		os.system("echo '	root	/var/www/hidden_service/;' >> /etc/nginx/sites-available/default ")
		os.system("echo '	allow	127.0.0.1;' >> /etc/nginx/sites-available/default")
		os.system("echo '	deny	all;' >> /etc/nginx/sites-available/default")
		os.system("echo '	server_tokens	off;' >> /etc/nginx/sites-available/default")			
		os.system("echo '}' >> /etc/nginx/sites-available/default")
		print("[*] Starting Nginx")
		os.system("service nginx start")
		
		
		print("[!] Done! Your Tor Hidden Service is up and running!")
		print("[!] You Hidden Service is located in : /var/www/hidden_service/")
		print("[!] You can access it by this URL: " + addr)

	sys.exit("[!] OnionPi finished his job. Quitting.")