# -----------------------------------------------------------
# Driver of apllication for flask server
#
# 2021  Garrett O'Hara, Nick Kokenis, Matt Schuiteman
# email garrettohara2018@gmail.com
#       nkokenisXXXX@sdsu.edu
#       mschuitemanXXX@sdsu.edu
# -----------------------------------------------------------

from Website import create_app

app = create_app()

if __name__=='__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000, threaded=True)
