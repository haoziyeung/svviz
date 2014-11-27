import os
import urllib
from flask import Flask, render_template, request, jsonify

RESULTS = {}
READ_INFO = None
SAMPLES = []

# Initialize the Flask application
app = Flask(__name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
    )


def getport():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@app.route('/')
def index():
    print "INDEX"
    return render_template('index.html', samples=SAMPLES)
    # print t
    # return t

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


ALPHA = """<?xml version="1.0" encoding="utf-8" ?><svg baseProfile="full" height="100%" version="1.1" width="100%" viewBox="0 0 15000 4998" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><g class="svg_viewport"><text x="250" y="150" 
        font-size="55">ALPHA</text></g></svg>"""
BETA = """<?xml version="1.0" encoding="utf-8" ?><svg baseProfile="full" height="100%" version="1.1" width="100%" viewBox="0 0 15000 4998" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><g class="svg_viewport"><text x="250" y="150" 
        font-size="55">BETA</text></g></svg>"""
GAMMA = """<?xml version="1.0" encoding="utf-8" ?><svg baseProfile="full" height="100%" version="1.1" width="100%" viewBox="0 0 15000 4998" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><g class="svg_viewport"><text x="250" y="150" 
        font-size="55">GAMMA</text></g></svg>"""        
@app.route('/_disp')
def display():
    req = request.args.get('req', 0)

    if req == "progress":
        return jsonify(result="done")

    if req in ["ref", "amb"]:
        svg = open("{}.svg".format(req)).read()
        return jsonify(result=svg)
    if req == "alt":
        svg = open("alt.svg").read()
        return jsonify(results=[{"svg":ALPHA, "name":"ALPHA"}, {"svg":BETA, "name":"BETA"}, {"svg":GAMMA, "name":"GAMMA"}, ])


    if req == "counts":
        return jsonify(result=RESULTS)

    return jsonify(result="unknown request: {}".format(req))

@app.route('/_info')
def info():
    import Alignment
    readid = urllib.unquote(request.args.get('readid', 0))

    if readid in READ_INFO:
        reads = READ_INFO[readid].getAlignments()
        result = []
        for read in reads:
            html = "{}<br/>".format(Alignment.getBlastRepresentation(read).replace("\n", "<br/>"))
            html = html.replace(" ", ".")
            result.append(html)

        result.append("<br/>Total length={}".format(len(READ_INFO[readid])))
        result.append(" &nbsp; Log odds={:.3g}".format(float(READ_INFO[readid].prob)))
        result = "".join(result)
        result = "<div style='font-family:Courier;'>" + result + "</div>"
        result = jsonify(result=result)
        return result
    else:
        print "NOT FOUND:", readid


# def load():
#     import remap
#     global RESULTS, READ_INFO

#     results, refalns, altalns, ambalns = remap.main()
#     RESULTS.update(results)

#     READ_INFO = {}

#     for readset in refalns + altalns + ambalns:
#         READ_INFO[readset.getAlignments()[0].name] = readset

#     # RESULTS = {"AltCount":523345, "RefCount":23522, "AmbCount":9999}



def run():
    import webbrowser
    port = getport()

    # load()
    webbrowser.open_new("http://127.0.0.1:{}".format(port))

    app.run(
        port=port#,
        # debug=True
    )

if __name__ == '__main__':
    pass