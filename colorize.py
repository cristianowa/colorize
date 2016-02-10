#!/usr/bin/python
import sys
from opencvimage import CvImage
import math
import argparse
import flask
import tempfile

def distance(a, b):
    x = pow(a[0] - b[0], 2)
    y = pow(a[1] - b[1], 2)
    z = pow(a[2] - b[2], 2)
    return math.sqrt(x + y + z)


def replacement(im_colors, colors):
    rep = {}
    for ic in im_colors:
        rep[ic] = None
        for c in colors:
            if rep[ic] == None:
                rep[ic] = c
            elif distance(ic, c) < distance(ic, rep[ic]):
                rep[ic] = c
    return rep


def colorize(imageName, colors, new_name=None):
    k = len(colors)
    im = CvImage.from_file(imageName)
    im.KMeansQuantization(k)
    im_colors = im.Colors()
    rep = replacement(im_colors, colors)
    im.Replace(rep)
    if new_name is None:
        new_name = imageName[:imageName.rfind(".")]
        new_name += "_colorized.jpg"
    im.Write(new_name)


def serve(port):
    app = flask.Flask(__name__)
    @app.route('/', methods=["POST", "GET"])
    def root():
        if flask.request.method == 'POST':
            file = flask.request.files['file']
            if file:
                with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
                    file.save(temp.name)
                    colorize(temp.name, [(0, 0, 0), (100,100,100),(200, 200, 200)], temp.name)
                    return flask.send_file(temp.name)
        else:
            return '''
        <!doctype html>
        <title>Colorize</title>
        <h1>Image to Colorize:</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        ''', 201
    app.run(port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quantify images to a range of specific colors.")
    parser.add_argument("-i", "--input", help="Input file", dest="input", nargs="+")
    parser.add_argument("-o", "--output", help="Output file", dest="output", default=None)
    parser.add_argument("--overwrite", help="Overwrite file instead of creating a new one when no output is specified",
                        dest="overwrite", action="store_true")
    parser.add_argument("-w", help="Run webserver", dest="web", action="store_true")
    parser.add_argument("--port", help="Webserver port", dest="port", default=7000, type=int)
    parser.add_argument("-c", "--colors", help="Colors to be used in quatization in format 0,0,0 0,0,0", nargs="+",
                        dest="colors")
    args = parser.parse_args()
    if args.web:
        serve(args.port)

    else:
        colors = [eval(c) for c in args.colors]
        if len(args.input) > 1:
            assert(args.output is None, "Batch conversion don't allow ")
            for f in args.input:
                new_file = f if args.overwrite else None
                colorize(f, colors, new_file)
        else:
            output = None if args.output is None else args.output
            output = args.input[0] if args.overwrite else output
            colorize(args.input[0], colors, output)
