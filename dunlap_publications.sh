#! /bin/csh -f
wget --no-cache --secure-protocol=auto -r https://www.dropbox.com/s/8hsswke8csv7q37/publication_list.html -O /web/httpd/users/bgaensler/public_html/dunlap_publications.html >& /dev/null
chmod 644 /web/httpd/users/bgaensler/public_html/dunlap_publications.html
