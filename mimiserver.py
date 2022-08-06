from flask import *
dtd = b''''''
app= Flask('Miniserver')

def printall():
    print('- '*50)
    print(request.args)
    print(request.form)
    print(request.files)
    print('- '*50)
@app.route('/*', methods=['POST','GET'])
@app.route('//', methods=['POST','GET'])
def root():
    print("[ACC]")
    printall()
    return "ok"
@app.errorhandler(404)
@app.errorhandler(500)
def err(err):
    print("[ERR]")
    printall()
    return err,200

app.run("0.0.0.0",80,debug= False)

