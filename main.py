from Website import create_app

app = create_app()

if __name__=='__main__':
    print("Starting server...")
    app.debug = True
    app.run(host="0.0.0.0", port=5000, threaded=True)
