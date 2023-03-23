# simple-guestbook

A very simple Python/Flask guestbook example intended to work with
my [Rogue Portal](https://github.com/jerryryle/rogueportal) and act as a starting point for a friend's project.

## Rogue Portal Deployment Instructions

1. Prepare a Raspberry Pi SD card per
   the [Rogue Portal instructions](https://jerryryle.github.io/rogueportal/#create-a-raspberry-pi-os-sd-card), but don't
   deploy the rogue portal yet.
2. Install prerequisites.
    * `sudo apt install nginx python3-pip git`
3. Install pipenv, which will make working with virtual environments easier.
    * `sudo pip3 install pipenv`
4. Clone this repository (or, preferably, your own fork of it) to the "/var/www/simple-guestbook" folder.
    * `sudo git clone https://github.com/jerryryle/simple-guestbook.git /var/www/simple-guestbook`
5. Change the user/group permissions on the folder so that you don't need to sudo to modify it and so the web services
   can access it.
    * `sudo chown -R $USER:www-data /var/www/simple-guestbook`
6. Switch to the folder.
    * `cd /var/www/simple-guestbook`
7. Create and activate a Python virtual environment to contain our application and its dependencies.
    * `mkdir .venv && pipenv shell`
8. Install the needed dependencies into the virtual environment.
    * `pipenv install`
9. Exit the virtual environment.
    * `exit`
10. Create a writable location for the guestbook log file.
    * `sudo mkdir /var/log/guestbook && sudo chown $USER:www-data /var/log/guestbook && sudo chmod g+w /var/log/guestbook`
11. Link the systemd service config file into the systemd config folder. This file automatically starts the gunicorn
    service to run our Python app on startup.
    * `sudo ln -s /var/www/simple-guestbook/cfg/guestbook.service /etc/systemd/system/guestbook.service`
12. Start the systemd guestbook gunicorn service.
    * `sudo systemctl enable guestbook`
13. Deploy the Rogue Portal packages
    per [the documentation](https://jerryryle.github.io/rogueportal/#deploy-the-pre-built-debian-packages), but don't
    reboot yet.
14. Activate the guestbook site.
    * `sudo ln -s /var/www/simple-guestbook/cfg/guestbook.rogueportal /etc/nginx/sites-enabled/guestbook`
15. Deactivate the default Rogue Portal content site.
    * `sudo rm -f /etc/nginx/sites-enabled/roguecontent`
16. Reboot.
    * `sudo reboot`

You should now be able to access the guestbook at your computer's IP address. Don't for get to test signing the
guestbook to ensure that the file permissions on the guestbook file are correct.

## Viewing the guestbook

Assuming you did not edit the configuration files to change the guestbook's location, then you can view it with the
following command:
`cat /var/log/guestbook/guestbook.txt`

## Editing the website after deployment

Once deployed per the above instructions, the HTML files for the guestbook website are located here:

`/var/www/simple-guestbook/simple_guestbook/templates`

Static resources such as CSS and images are here:

`/var/www/simple-guestbook/simple_guestbook/static`

You can edit/add/remove files in place; however, to see your changes, you will need to restart the guestbook gunicorn
service:

`sudo systemctl restart guestbook`

If you're doing a lot of active development on the website, this might get tedious. A faster approach is to switch the
service into debug mode, which will automatically detect changes to the application and reload it. To do this,
edit `/var/www/simple-guestbook/wsgi.py` and change `app.run(debug=False)` to `app.run(debug=True)`. Save the file and
run `sudo systemctl restart guestbook`. After this, your changes to HTML/CSS and even Python should automatically apply.
Be sure to turn off debug mode before using your app in a production environment.  
