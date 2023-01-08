______ présentation ______

les journées sont stoquées dans journal.json (à créer vous-même).

le nouvel article est enregistré dans journal-new.json. je ne touche pas à journal.json par sécurité, afin que les données ne soient pas corrompues par erreur.

______ lancement ______

lire les articles en lançant journal-show.html.
entrer un nouvel article en lançant journal-new.html et un serveur python 3.

lancer le serveur:
cd /var/www/
python -m http.server --cgi 1407

http://localhost:1407/cgi-bin/journal/journal-show.html

______ installation ______

ce projet utilise python 3 comme back-end, avec apache2.

dépendences:
	debbyPlay, le js et le css
	structure.css

dans /var/www/cgi-bin/ placer le dossier journal

créer /var/www/cgi-bin/.htacces contenant
AddHandler cgi-script .py

dans /etc/apache2/apache2.conf
ScriptAlias /cgi-bin/ /var/www/cgi-bin/
<Directory /var/www/cgi-bin/>
	Options FollowSymLinks Indexes ExecCGI
	AllowOverride All
	Order deny,allow
	Allow from all
	Require all granted
</Directory>

dans la console
sudo chmod -R 777 /var/www/cgi-bin
sudo a2enmod cgi
systemctl restart apache2
