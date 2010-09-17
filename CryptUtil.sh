#!/bin/sh

## Crypto tool for symetric file encryption/decryption, using zenity and gpg.
## Supported Ciphers: CAST5, TWOFISH, BLOWFISH, 3DES, AES, AES192, AES256.

title="CryptUtil"
err_pass="<b>You MUST provide a passphrase.</b>"
err_unexp="<b>An unexpected error occured.</b>"
enc_success="<b>Your file has been successfully encrypted.</b>"
dec_success="<b>Your file has been successfully decrypted.</b>"

check(){
	if [ "$1" = "encrypt" ]
	then
		if [ -e "$selection.gpg" ]
		then
			zenity --info --title="$title" --text="$enc_success\n\nLocation of encrypted file:\n<i>$selection.gpg</i>"
			exit 0
		else
			zenity --error --title="Error" --text="$err_unexp\nEncryption failed."
			exit 0
		fi
	fi
	if [ "$1" = "decrypt" ]
	then
		if [ -e "$outfile" ]
		then
			zenity --info --title="$title" --text="$dec_success\n\nLocation of decrypted file:\n<i>$outfile</i>"
			exit 0
		else
			zenity --error --title="Error" --text="$err_unexp\nDecryption failed."
			exit 0
		fi
	fi
}

encrypt(){
	cipher=`zenity --list --radiolist --title="$title" --text="Choose the cipher:" --column="" --column="Type" --print-column="2" \
	TRUE "AES256" \
	FALSE "AES192" \
	FALSE "AES" \
	FALSE "3DES" \
	FALSE "BLOWFISH" \
	FALSE "TWOFISH" \
	FALSE "CAST5"`
	passphrase=`zenity --entry --hide-text --entry-text="$passphrase" --title="$title" --text="Passphrase for: ${selection##*/}" "" 2>&1`
	
	if [ "$passphrase" = "" ]
	then
		zenity -error --title="Error" --text="$err_pass"
		exit 0
	else
		echo "$passphrase" | gpg --batch --passphrase-fd 0 --cipher-algo "$cipher" -c "$selection"
	fi
}

decrypt(){
	passphrase=`zenity --entry --hide-text --entry-text="$passphrase" --title="$title" --text="Passphrase for: ${selection##*/}" "" 2>&1`
	
	if [ "$passphrase" = "" ]
	then
		zenity --error --title="Error" --text="$err_pass"
		exit 0
	else
		outfile=${selection%.*}
		echo "$passphrase" | gpg -o "$outfile" --batch --passphrase-fd 0 -d "$selection"
	fi
}

zenity --question --title="$title" --text="<i><b><tt><big>Symetric Crypting Utility</big></tt></b></i>\n\nSupported ciphers:\n- AES256\n- AES192\n- AES\n- 3DES\n- BLOWFISH\n- TWOFISH\n- CAST5 \n\n<i><small>--- Requires GPG ---</small></i>" && \
ok="True"

if [ "$ok" != "True" ]
then
	exit 0
else
	task=`zenity --list --radiolist --title="$title" --text="Choose a task to perform:" --column="" --column="Task" --column="" --print-column="3" --hide-column="3" \
	FALSE "Encrypt a file" "encrypt" \
	FALSE "Decrypt a file" "decrypt"`
	
	if [ "$task" = "" ]
	then
		exit 0
	else
		selection=`zenity  --file-selection --title="$title"`
		if [ "$task" = "encrypt" ]
		then
			encrypt
			check "encrypt"
		fi
		if [ "$task" = "decrypt" ]
		then
			decrypt
			check "decrypt"
		fi
	fi
fi
