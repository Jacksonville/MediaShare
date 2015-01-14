#!/usr/bin/env 
__version__ = '0.0.0.1'
import argparse, bottle, os, logging, datetime, sys, threading, zipfile
from PIL import Image

rootdir = os.path.split(os.path.abspath(__file__))[0]
if not os.path.exists(os.path.join(rootdir, 'logs')):
    try:
        os.mkdir(os.path.join(rootdir, 'logs'))
    except:
        raise

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    filename=os.path.join(rootdir, 'logs', '%s_%s.log' % (datetime.datetime.now().strftime("%Y-%m-%d"),os.path.splitext(os.path.split(sys.argv[0])[1])[0])),
                            filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

appPath = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(appPath, 'static', 'templates'))

def flip_horizontal(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
def flip_vertical(im): return im.transpose(Image.FLIP_TOP_BOTTOM)
def rotate_180(im): return im.transpose(Image.ROTATE_180)
def rotate_90(im): return im.transpose(Image.ROTATE_90)
def rotate_270(im): return im.transpose(Image.ROTATE_270)
def transpose(im): return rotate_90(flip_horizontal(im))
def transverse(im): return rotate_90(flip_vertical(im))
orientation_funcs = [None,
                 lambda x: x,
                 flip_horizontal,
                 rotate_180,
                 flip_vertical,
                 transpose,
                 rotate_270,
                 transverse,
                 rotate_90
                ]

class DirPrep(threading.Thread):
    """Create thumbnail images for the web preview"""
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.tempdir = args.tempdir
        self.sharedir = args.path
        self.size = 320, 320

    def apply_orientation(self, im):
        """
        Extract the oritentation EXIF tag from the image, which should be a PIL Image instance,
        and if there is an orientation tag that would rotate the image, apply that rotation to
        the Image instance given to do an in-place rotation.

        :param Image im: Image instance to inspect
        :return: A possibly transposed image instance
        """

        try:
            kOrientationEXIFTag = 0x0112
            if hasattr(im, '_getexif'): # only present in JPEGs
                e = im._getexif()       # returns None if no EXIF data
                if e is not None:
                    #log.info('EXIF data found: %r', e)
                    orientation = e[kOrientationEXIFTag]
                    f = orientation_funcs[orientation]
                    return f(im)
        except:
            # We'd be here with an invalid orientation value or some random error?
            pass # log.exception("Error applying EXIF Orientation tag")
        return im

    def create_thumb(self, imagepath, basename, size):
        """
        Create thumbnail / smaller images from image files.
        The output directory is self.tempdir that was set at initialisation.
         
        :param FilePath imagepath: Path to image file that you would like to process.
        :param String basename: Image output name.
        :param List size: Maximum width/height for the output image, aspect ratio is maintained.
        """
        try:
            outfile = os.path.join(self.tempdir, basename+'_'+os.path.split(imagepath)[1])
            im = Image.open(imagepath)
            im = self.apply_orientation(im)
            im.thumbnail((size), Image.ANTIALIAS)
            im.save(outfile, "JPEG")

        except IOError:
            logging.error('cannot create thumbnail for "%s"' % imagepath)
          
    def clear_temp_dir(self):
        """
        Clear contents of self.tempdir
        """
        for the_file in os.listdir(self.tempdir):
            file_path = os.path.join(self.tempdir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                logging.error(e)

    def process_dir(self):
        """
        Process self.sharedir. The first step run is to clear self.tempdir, then traverse self.sharedir
        creating thumbnails and smaller images for the webview
        """
        self.clear_temp_dir()
        for r, d, f in os.walk(self.sharedir):
            for file in f:
                filext = os.path.splitext(file)[1][1:]
                if filext.lower() in ['jpg', 'jpeg', 'bmp', 'png']:
                    basefilename = r.split(self.sharedir)[1].replace(os.sep, '_')
                    thumbsize = [320 , 320]
                    self.create_thumb(os.path.join(r, file),'thumb_'+basefilename, thumbsize)
                    gallerysize = [1200 , 1200]
                    self.create_thumb(os.path.join(r, file), basefilename, gallerysize)

    def run(self):
        self.process_dir()
    

class WebServer(object):
    def __init__(self, args, imgloader):
        self.directory = args.path
        self.imgloader = imgloader

    def __new__(cls, *args, **kwargs):
        obj = super(WebServer, cls).__new__(cls, *args, **kwargs)
        bottle.route('/static/:path/:file#.*#')(obj.get_static_files)
        bottle.route("/")(obj.render_directory)
        bottle.route("/dl")(obj.download_file)
        bottle.route("/load_images")(obj.load_images)
        return obj

    def load_images(self):
        self.imgloader.start()
        return "<html><meta http-equiv='refresh' content='5; url=/'><p>Image reload initiated</p></html>"

    def list_dir(self, directory):
        filelist = [x for x in os.listdir(directory) if os.path.isfile(os.path.join(directory, x))]
        dirlist = [x for x in os.listdir(directory) if os.path.isdir(os.path.join(directory, x))]
        return dirlist, filelist

    def get_static_files(self, file, path):
        return bottle.static_file(file, root=os.path.join(appPath,'static',path))

    def render_directory(self):
        ldir = os.path.join(self.directory, bottle.request.GET.get('dir','/')[1:])
        dirlist, filelist = self.list_dir(ldir)
        if ldir != self.directory:
            ldir = '/'+ldir.split(self.directory)[1]+'/'
        else:
            ldir = '/'
        return bottle.template('index',
                               curr_dir=ldir,
                               dirlist=dirlist,
                               filelist=filelist)

    def download_file(self):
        filename = bottle.request.GET.get('filename')
        return bottle.static_file(filename, root=self.directory, download=filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quickly share files via web browser')
    parser.add_argument('path',
                        help='directory that you would like to share')
    parser.add_argument('--tempdir',
                        help='directory where thumbs should be placed',
                        default=os.path.join(appPath,'static','images','temp'))
    parser.add_argument('--port',
                        help='TCP port that the webserver should listen on',
                        default=8084)
    parser.add_argument('--host',
                        help='IP address that the webserver should bind on',
                        default='127.0.0.1')
    args = parser.parse_args()
    prep = DirPrep(args)
    port = args.port
    host = args.host
    obj = WebServer(args, prep)
    app = bottle.app()
    bottle.run(app=app, host=host, port=int(port), server='tornado', reloader=True)
