make the folder useable by regular user  
```sudo chown -R $USER:$USER /tmp/device1```

make the folder readable  
```sudo chmod -R 755 /tmp/device1```


make a virtual-host configuration in apache  
```sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/device1.conf```


now update the configuration of device1.conf to the following:  
```
<VirtualHost *:80>

	ServerAdmin admin@device1
	ServerName device1.com
	ServerAlias www.device1.com
	DocumentRoot /tmp/device1
	LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>

```