from src.classes.snp_system import SnpSystem
from src.types.snp_system_dict import SnpSystemDict
from algorithms.modified_homogenize import modified_homogenize
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
    input_snp_system_xmp_str = input.get('snp_system')
    # print(f">>>>>> input_snp_system_xmp_str: {input_snp_system_xmp_str}")
    snp_system_dict = SnpSystemDict(xmltodict.parse(input_snp_system_xmp_str))
    # print(f">>>>>> snp_system_dict: {snp_system_dict}")
    snp_system = SnpSystem.from_dict(snp_system_dict)  #! O(n^2 + nk + nt)
    modified_homogenize(snp_system)  #! O(nk)
    print(f"Homogenized an SN P System")
    
    return {
        'snp_system': input_snp_system_xmp_str,
        'homogenized_snp_system': snp_system.to_xmp(),
        'errors': None,
    }


if __name__ == "__main__":
    app.run(debug=True)