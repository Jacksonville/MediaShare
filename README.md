# MediaShare
I created this based on the WebShare repo that I published earlier.
At the moment it only shares images, but as the name suggests I would also like to extend this in the future to include other items of media.

To run, execute the following command:
`python mshare.py [path to rooot of images]`
There are some optional arguments as well:
- tempdir  : directory that you want to store the thumbnail versions of your images
- port     : TCP port that you would like your webserver to listen on.
- host     : IP address that you would like your webserver to bind to.
- password : Password to keep your data secure, is ommited no password is required to access your data.

Once the webserver is started up, navigate to [your_url]/load_images from your browser to initialise the image loading process.

##Deps:
You might need to install the following packages from the cheeseshop:
- pillow: https://pypi.python.org/pypi/Pillow/

Thanks to:
- Bottle for the awesome micro framework, rock solid: http://bottlepy.org
- Beaker for the amazing session management module: http://beaker.readthedocs.org/en/latest/
- Bootstrap for the theme, great work guys: http://www.getbootstrap.com
- Fancybox for the cool image gallery vibes: https://github.com/fancyapps/fancyBox
- LaxyLoad for the incredible lazy image loader: http://www.appelsiini.net/projects/lazyload

Please feel free to use as you see fit, hope that you get some use out of it.
