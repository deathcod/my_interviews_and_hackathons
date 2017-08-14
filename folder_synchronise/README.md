# INTRODUCTION

This is project aims make two folder synchronised. I have detailed the setup.

The over all idea is to create a third device which will act as a master and this will help to synchronize the two devices.

**FIRST IMPLEMENTATION**  

First I was creating three devices(device1, device2, device3) and using rsync and ssh to login into different devices and synchronize the data. Device3 was acting as a center and mantaining the sync between the two devices.

```
    Rsync from D3        Rsync from D3  
  - - - - - - -- - -    -  - - - - - - -  
  |                |    |              |  
DEVICE 1 ------>  DEVICE 3 <------ DEVICE 2  
	
```

But it had a faliure, if there is any change in device2 and syncs to device3 data in device3 gets lost and when device3 broadcasts the change to device2 and device3 and thus data on device1 also changes.

[![Watch the video](https://i.ytimg.com/vi/gtf3ulAoaxU/sddefault.jpg)](https://youtu.be/gtf3ulAoaxU)


**SECOND IMPLEMENTATION**  

In the second implementation there is no interaction from device2 and device1. Both are online but are not initiating any synchronisation. Here Device3 is the master and device1 and device2 are slave. Device3 starts osync on Device2 and device1. And thus both are synchronised. 
Device3 is set to cron and every minute it is triggered and device1 and device2 are synced.

```
    Osync from D3        Osync from D3  
  - - - - - - -- - -    -  - - - - - - -  
  |                |    |              |  
DEVICE 1          DEVICE 3          DEVICE 2  
	      triggered every minute
```

[![Watch the video](https://i.ytimg.com/vi/oRugu0CG9is/sddefault.jpg)](https://youtu.be/oRugu0CG9is)


**Challenges**

* How to manage the conflicts when both the uses are offline
* Whom to give the priority on conflict

Now solved this using osync.  

**Why not git**

I had a thought to use git but had confusion on merge conflict. But came to know there is (our-their) in git on merge to prioritize at the time of conflict.  And this would have been focused giving one the priority (if I write a script). So do this trade off I resolved to rsync.

___

# INSTALLATION GUIDE

[![Watch the video](https://i.ytimg.com/vi/DVY4HxqvZu8/sddefault.jpg)](https://youtu.be/DVY4HxqvZu8)



## Installation of rsync on windows

* Download "mingw-get-setup.exe"
* Install
* When the MinGW Installation Manager starts up navigate the left side options and select "MSYS". Then locate and select only the "msys-rsync" bin package.
* On successful installation
* Open Git-bash and run as admin
* Add the commad below.  
```sh  
 echo '/c/MinGW/msys/1.0/bin/rsync "$@"' >/usr/bin/rsync  
 chmod +x /usr/bin/rsync
```

## Setting up apache virtual-host in ubuntu

first install apache 

```  
sudo apt-get update  
sudo apt-get install apache2  
```  

### root-login

* fist be in root ```sudo -i```
* now ssh-server is needed to be installed. By default only ssh client is available in ubuntu ```apt-get install open-ssh```
* type ```passwd``` to set root password
* get access to the server as a root ```root@127.0.0.1```
* password : the password typed in passwd
* now logged in root user.

As root is of high importance we shouldnot use it directly. Instead create a new user with only required set of previlages.  

### create a new user with certain root previlage

* ```adduser device1```
* adding the new user to sudo group ```gpasswd -a device1 sudo```
* add the new user to the sudo privilege.
```
sudo visudo
root    ALL=(ALL:ALL) ALL
device1 ALL=(ALL:ALL) ALL
```

LOCAL MACHINE 

* generate keygen in your local machine```ssh-keygen```
* put the key into 	```/root/.ssh/id_rsa```
* now check the id_rsa.pub in your local machine ``` cat ~/.ssh/id_rsa.pub ```
* copy the key
* ```nano /etc/ssh/sshd_config``` edit the permission of root login 
* ``` PermitRootLogin no ``` make it no


SERVER

``` sh
su - device1
mkdir .ssh
chmod 700 .ssh
nano .ssh/authorized_keys
```

paste the key in the file and save and exit

```chmod 600 .ssh/authorized_keys``` restrict the permission of the file
$ chown syncuser:root /home/syncuser/.ssh/authorized_keys
```exit```

Having done tell this.  

* restart the server
* check if you can login ```ssh device1@127.0.0.1```


delete a user  
```  
deluser --remove-home newuser 	#remove the newuser and the files
visudo
device1 ALL=(ALL:ALL) ALL   	#DELETE THIS LINE
```  
remove the sudo privilege.  


### disable user
sudo usermod --expiredate 1 device2

### enable user
sudo usermod --expiredate "" devcie2


### using inotifywait

* install inotifywait by ```sudo apt-get install inotify-tools```
* This helps the user to notify user any change in the file structure.
* ```inotifywait -m -r --format '%:e %f %T' /home/deathcoder007/D ``` 
* ```--timefmt '%d/%m/%y %H:%M:%S'``` time format
* ```-d -o '/home/deathcoder007/l.txt'``` output format
* ```-e MODIFY,DELETE,CREATE``` triggers when these happens

## SSH Login without using password

local server: ssh-keygen  
ssh-copy-id -i ~/.ssh/id_rsa.pub device1@127.0.0.1  
enter the password  
ssh device@127.0.0.1  
and logged in without password  


### using osync
./osync.sh --initiator=/path/to/dir1 --target=ssh://remoteuser@remotehost.com//path/to/dir2

CREATE_DIRS=yes|no  [default no]  
REMOTE_HOST_PING=yes|no [check if the remote host is pinging]  
INSTANCE_ID=name_of_your_sync  [name of the sync]  
INITIATOR_SYNC_DIR="/some/path"  
TARGET_SYNC_DIR="/some/other/path"  
SSH_RSA_PRIVATE_KEY=~/.ssh/id_rsa  
LOGFILE=""  
CONFLICT_BACKUP=yes|no  
CONFLICT_BACKUP_MULTIPLE=yes|no  
CONFLICT_BACKUP_DAYS=30  
SOFT_DELETE=yes  

___

## Things to know

* to create a symlink: ```ln -s <path>file_name <path>file_link_name```


-a: This is a an alias to lot of other flags  **-rltpgoD**

r – Recursive
l – Transfer any symlinks encountered
t – Preserve time stamps
p – Preserve permissions
g – Preserve groups
o – Preserve ownership
D – Preserve block and character devices

h – Human-readable format of file sizes
v - verbos to give more about the state of transfer

* chmod is used to provide permission to the users on a file.
Let's say you are the owner of a file named myfile, and you want to set its permissions so that:

    * the user can **r**ead, **w**rite, ande **x**ecute it;
    * members of your group can **r**ead ande **x**ecute it; and
    * others may only **r**ead it.

This command will do the trick:

chmod u=rwx,g=rx,o=r myfile

Here the digits 7, 5, and 4 each individually represent the permissions for the user, group, and others, in that order. Each digit is a combination of the numbers 4, 2, 1, and 0:  

	* 4 stands for "read",
    * 2 stands for "write",
    * 1 stands for "execute", and
    * 0 stands for "no permission."

So 7 is the combination of permissions 4+2+1 (read, write, and execute), 5 is 4+0+1 (read, no write, and execute), and 4 is 4+0+0 (read, no write, and no execute).

### Cron job   

```
 +---------------- minute (0 - 59)
 |  +------------- hour (0 - 23)
 |  |  +---------- day of month (1 - 31)
 |  |  |  +------- month (1 - 12)
 |  |  |  |  +---- day of week (0 - 6) (Sunday=0)
 |  |  |  |  |
 *  *  *  *  *  command to be executed

 ```