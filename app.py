from flask import Flask
from routes.vm_routes import vm_bp

app = Flask(__name__)
app.register_blueprint(vm_bp, url_prefix="/vm")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
