from src.classes.snp_system import SnpSystem
from src.types.snp_system_dict import SnpSystemDict
from algorithms.homogenize_prime_released_spike_scaling import homogenize_prime_released_spike_scaling
from algorithms.homogenize_type_2_scaling import homogenize_type_2_scaling
from flask import Flask, request
from flask_cors import CORS
from typing import Dict
import xmltodict

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
    WEBSNAPSE V2.0 WITH HOMOGENIZATION BUTTON
https://websnapse-homogenize.netlify.app/

HOMOGENIZATION API
https://homogenize.fly.dev/

SAMPLE API REQUEST
URL: https://homogenize.fly.dev/homogenize
METHOD: POST
BODY [json]: {
    scaling_type: 0,
    snp_system: "<content><n1><id>n1</id><position><x>66.5</x><y>200</y></position><rules>a/a-&gt;a;0 2a/a-&gt;a;0</rules><startingSpikes>2</startingSpikes><delay>0</delay><spikes>2</spikes><isOutput>false</isOutput><isInput>false</isInput><out>n2</out><outWeights><n2>1</n2><n3-nm2MDs9Nh>1</n3-nm2MDs9Nh></outWeights></n1><n2><id>n2</id><position><x>282.5</x><y>197</y></position><rules>3a/2a-&gt;a;0</rules><startingSpikes>3</startingSpikes><delay>0</delay><spikes>3</spikes><isOutput>false</isOutput><isInput>false</isInput><out>n4</out><outWeights><n4>1</n4></outWeights></n2><n4><id>n4</id><position><x>456.5</x><y>204</y></position><isOutput>true</isOutput><isInput>false</isInput><spikes>0</spikes><bitstring/></n4></content>"
}


Notes
* scaling_type: 0 => Type 2 Subsystem Scaling would be used.
* scaling_type: 1 => Released Spike Scaling would be used.
* snp_system is an SN P system with the same format as the xmp saved file of WebSnapse v2.0.



SAMPLE RESPONSE
BODY [json]: {
    snp_system: "<content><n1><id>n1</id><position><x>66.5</x><y>200</y></position><rules>a/a-&gt;a;0 2a/a-&gt;a;0</rules><startingSpikes>2</startingSpikes><delay>0</delay><spikes>2</spikes><isOutput>false</isOutput><isInput>false</isInput><out>n2</out><outWeights><n2>1</n2><n3-nm2MDs9Nh>1</n3-nm2MDs9Nh></outWeights></n1><n2><id>n2</id><position><x>282.5</x><y>197</y></position><rules>3a/2a-&gt;a;0</rules><startingSpikes>3</startingSpikes><delay>0</delay><spikes>3</spikes><isOutput>false</isOutput><isInput>false</isInput><out>n4</out><outWeights><n4>1</n4></outWeights></n2><n4><id>n4</id><position><x>456.5</x><y>204</y></position><isOutput>true</isOutput><isInput>false</isInput><spikes>0</spikes><bitstring/></n4></content>",
    errors: None,
    homogenized_snp_system: "<content>\n\t<n1>\n\t\t<id>n1</id>\n\t\t<position>\n\t\t\t<x>66.5</x>\n\t\t\t<y>200.0</y>\n\t\t</position>\n\t\t<rules>3a/2a-&gt;2a;0 5a/2a-&gt;2a;0 6a/4a-&gt;2a;0</rules>\n\t\t<startingSpikes>2</startingSpikes>\n\t\t<delay>0</delay>\n\t\t<spikes>5</spikes>\n\t\t<isOutput>false</isOutput>\n\t\t<isInput>false</isInput>\n\t\t<out>n2</out>\n\t\t<outWeights>\n\t\t\t<n2>1</n2>\n\t\t\t<n3-nm2MDs9Nh>1</n3-nm2MDs9Nh>\n\t\t</outWeights>\n\t</n1>\n\t<n2>\n\t\t<id>n2</id>\n\t\t<position>\n\t\t\t<x>282.5</x>\n\t\t\t<y>197.0</y>\n\t\t</position>\n\t\t<rules>3a/2a-&gt;2a;0 5a/2a-&gt;2a;0 6a/4a-&gt;2a;0</rules>\n\t\t<startingSpikes>3</startingSpikes>\n\t\t<delay>0</delay>\n\t\t<spikes>6</spikes>\n\t\t<isOutput>false</isOutput>\n\t\t<isInput>false</isInput>\n\t\t<out>n4</out>\n\t\t<outWeights>\n\t\t\t<n4>1</n4>\n\t\t</outWeights>\n\t</n2>\n\t<n4>\n\t\t<id>n4</id>\n\t\t<position>\n\t\t\t<x>456.5</x>\n\t\t\t<y>204.0</y>\n\t\t</position>\n\t\t<isOutput>true</isOutput>\n\t\t<isInput>false</isInput>\n\t\t<spikes>0</spikes>\n\t\t<bitstring></bitstring>\n\t</n4>\n</content>"
}
"""


@app.route('/homogenize', methods = ['POST'])
def homogenize_input():

    # Get the JSON body of the request
    input: Dict[str, any] = request.json

    # Get the SN P system from the body
    input_snp_system_xmp_str = input.get('snp_system')

    # Get the scaling type to be used from the body
    scaling_type = input.get('scaling_type')

    # Parse the SN P system input and create an equivalent SNpSystem object
    snp_system_dict = SnpSystemDict(xmltodict.parse(input_snp_system_xmp_str))
    snp_system = SnpSystem.from_dict(snp_system_dict)  #! O(n^2 + nk + nt)

    # Homogenize the SN P system using the requested scaling type.
    if scaling_type == 0:
        homogenize_type_2_scaling(snp_system)
    elif scaling_type == 1:
        homogenize_prime_released_spike_scaling(snp_system)  #! O(nk)
    else:
        raise ValueError("Invalid `scaling_type`. Please use 0 for Type-2 Subsystem Scaling or 1 for Released Spike Scaling")
    

    print(f"Homogenized an SN P System")
    

    # Returns the original SN P system, its homogenized form, and if there are any errors encountered.
    return {
        'snp_system': input_snp_system_xmp_str,
        'homogenized_snp_system': snp_system.to_xmp(),
        'errors': None,
    }


if __name__ == "__main__":
    app.run(debug=True)