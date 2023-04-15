from src.classes.snp_system import Snp_system
from src.algorithms.homogenize import homogenize
from flask import Flask, request
from flask_cors import CORS
from typing import Dict
import xmltodict

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "helloss"


@app.route('/homogenize', methods = ['POST'])
def homogenize_input():
    input: Dict[str, any] = request.json
    input_snp_system_str = input.get('snp_system')
    # print(f">>>>>> input_snp_system_str: {input_snp_system_str}")
    input_json = xmltodict.parse(input_snp_system_str)
    # print(f">>>>>> input_json: {input_json}")
    snp_system = Snp_system(input_json)
    homogenize(snp_system)
    print(f"Homogenized an SN P System")
    return {
        'snp_system': input_snp_system_str,
        'homogenized_snp_system': snp_system.to_xmp(),
        'errors': None,
    }


if __name__ == "__main__":
    app.run(debug=True)