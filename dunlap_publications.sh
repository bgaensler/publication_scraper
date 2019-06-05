#! /bin/csh -f
wget --no-cache --secure-protocol=auto -r https://www.dropbox.com/s/aktinaypyepu689/dunlap_publications.html -O /web/httpd/users/bgaensler/public_html/dunlap_publications.html >& /dev/null
chmod 644 /web/httpd/users/bgaensler/public_html/dunlap_publications.html
