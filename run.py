from app import create_app

app = create_app()

if __name__ == "__main__":
    # use_reloader=False para evitar reinicio por cambios en pickles
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False, threaded=True)
