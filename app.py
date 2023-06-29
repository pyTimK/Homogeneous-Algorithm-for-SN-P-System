from src.classes.snp_system import SnpSystem
from src.types.snp_system_dict import SnpSystemDict
from src.algorithms.homogenize_prime_released_spike_scaling import homogenize_prime_released_spike_scaling
from src.algorithms.homogenize_type_2_scaling import homogenize_type_2_scaling
from src.algorithms.auto_layout import auto_layout
from src.converter.converter import convert
from src.converter.src.globals import XML, JSON, YAML
from flask import Flask, request
from flask_cors import CORS
from typing import Dict
import xmltodict

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
    <html>
    <head>
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    .header {
        font-size: 24px;
        font-weight: bold;
        color: #3366cc;
        margin-bottom: 10px;
    }
    .section {
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 18px;
        font-weight: bold;
        color: #009933;
        margin-bottom: 5px;
    }
    .section-content {
        font-size: 14px;
        color: #333333;
        margin-left: 20px;
    }
    </style>
    </head>
    <body>
        <div class="header">WEBSNAPSE V2.0 WITH HOMOGENIZATION BUTTON</div>
        <div class="section">
            <div class="section-title">WEBSNAPSE V2.0:</div>
            <div class="section-content">
                <a href="https://websnapse-homogenize.netlify.app/">https://websnapse-homogenize.netlify.app/</a>
            </div>
        </div>
        <div class="section">
            <div class="section-title">HOMOGENIZATION API:</div>
            <div class="section-content">
                <a href="https://homogenize.fly.dev/">https://homogenize.fly.dev/</a>
            </div>
        </div>
        <div class="section">
            <div class="section-title">SAMPLE API REQUEST:</div>
            <div class="section-content">
                <div class="section-title">URL:</div>
                <div class="section-content">https://homogenize.fly.dev/homogenize</div>
                <div class="section-title">METHOD:</div>
                <div class="section-content">POST</div>
                <div class="section-title">BODY [json]:</div>
                <div class="section-content">
                    <pre>
{
    "scaling_type": 0,
    "snp_system": "&lt;content&gt;&lt;n1&gt;&lt;id&gt;n1&lt;/id&gt;&lt;position&gt;&lt;x&gt;66.5&lt;/x&gt;&lt;y&gt;200&lt;/y&gt;&lt;/position&gt;&lt;rules&gt;a/a-&gt;a;0 2a/a-&gt;a;0&lt;/rules&gt;&lt;startingSpikes&gt;2&lt;/startingSpikes&gt;&lt;delay&gt;0&lt;/delay&gt;&lt;spikes&gt;2&lt;/spikes&gt;&lt;isOutput&gt;false&lt;/isOutput&gt;&lt;isInput&gt;false&lt;/isInput&gt;&lt;out&gt;n2&lt;/out&gt;&lt;outWeights&gt;&lt;n2&gt;1&lt;/n2&gt;&lt;n3-nm2MDs9Nh&gt;1&lt;/n3-nm2MDs9Nh&gt;&lt;/outWeights&gt;&lt;/n1&gt;&lt;n2&gt;&lt;id&gt;n2&lt;/id&gt;&lt;position&gt;&lt;x&gt;282.5&lt;/x&gt;&lt;y&gt;197&lt;/y&gt;&lt;/position&gt;&lt;rules&gt;3a/2a-&gt;a;0&lt;/rules&gt;&lt;startingSpikes&gt;3&lt;/startingSpikes&gt;&lt;delay&gt;0&lt;/delay&gt;&lt;spikes&gt;3&lt;/spikes&gt;&lt;isOutput&gt;false&lt;/isOutput&gt;&lt;isInput&gt;false&lt;/isInput&gt;&lt;out&gt;n4&lt;/out&gt;&lt;outWeights&gt;&lt;n4&gt;1&lt;/n4&gt;&lt;/outWeights&gt;&lt;/n2&gt;&lt;n4&gt;&lt;id&gt;n4&lt;/id&gt;&lt;position&gt;&lt;x&gt;456.5&lt;/x&gt;&lt;y&gt;204&lt;/y&gt;&lt;/position&gt;&lt;isOutput&gt;true&lt;/isOutput&gt;&lt;isInput&gt;false&lt;/isInput&gt;&lt;spikes&gt;0&lt;/spikes&gt;&lt;bitstring/&gt;&lt;/n4&gt;&lt;/content&gt;"
}
                    </pre>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="section-title">Notes:</div>
            <div class="section-content">
                <ul>
                    <li>scaling_type: 0 => Type 2 Subsystem Scaling would be used.</li>
                    <li>scaling_type: 1 => Released Spike Scaling would be used.</li>
                    <li>snp_system is an SN P system with the same format as the xmp saved file of WebSnapse v2.0.</li>
                </ul>
            </div>
        </div>
        <div class="section">
            <div class="section-title">SAMPLE RESPONSE:</div>
            <div class="section-content">
                <div class="section-title">BODY [json]:</div>
                <div class="section-content">
                    <pre>
{
    "snp_system": "&lt;content&gt;&lt;n1&gt;&lt;id&gt;n1&lt;/id&gt;&lt;position&gt;&lt;x&gt;66.5&lt;/x&gt;&lt;y&gt;200&lt;/y&gt;&lt;/position&gt;&lt;rules&gt;a/a-&gt;a;0 2a/a-&gt;a;0&lt;/rules&gt;&lt;startingSpikes&gt;2&lt;/startingSpikes&gt;&lt;delay&gt;0&lt;/delay&gt;&lt;spikes&gt;2&lt;/spikes&gt;&lt;isOutput&gt;false&lt;/isOutput&gt;&lt;isInput&gt;false&lt;/isInput&gt;&lt;out&gt;n2&lt;/out&gt;&lt;outWeights&gt;&lt;n2&gt;1&lt;/n2&gt;&lt;n3-nm2MDs9Nh&gt;1&lt;/n3-nm2MDs9Nh&gt;&lt;/outWeights&gt;&lt;/n1&gt;&lt;n2&gt;&lt;id&gt;n2&lt;/id&gt;&lt;position&gt;&lt;x&gt;282.5&lt;/x&gt;&lt;y&gt;197&lt;/y&gt;&lt;/position&gt;&lt;rules&gt;3a/2a-&gt;a;0&lt;/rules&gt;&lt;startingSpikes&gt;3&lt;/startingSpikes&gt;&lt;delay&gt;0&lt;/delay&gt;&lt;spikes&gt;3&lt;/spikes&gt;&lt;isOutput&gt;false&lt;/isOutput&gt;&lt;isInput&gt;false&lt;/isInput&gt;&lt;out&gt;n4&lt;/out&gt;&lt;outWeights&gt;&lt;n4&gt;1&lt;/n4&gt;&lt;/outWeights&gt;&lt;/n2&gt;&lt;n4&gt;&lt;id&gt;n4&lt;/id&gt;&lt;position&gt;&lt;x&gt;456.5&lt;/x&gt;&lt;y&gt;204&lt;/y&gt;&lt;/position&gt;&lt;isOutput&gt;true&lt;/isOutput&gt;&lt;isInput&gt;false&lt;/isInput&gt;&lt;spikes&gt;0&lt;/spikes&gt;&lt;bitstring/&gt;&lt;/n4&gt;&lt;/content&gt;",
    "homogenized_snp_system": "&lt;content&gt;\n\t&lt;n1&gt;\n\t\t&lt;id&gt;n1&lt;/id&gt;\n\t\t&lt;position&gt;\n\t\t\t&lt;x&gt;66.5&lt;/x&gt;\n\t\t\t&lt;y&gt;200.0&lt;/y&gt;\n\t\t&lt;/position&gt;\n\t\t&lt;rules&gt;3a/2a-&gt;2a;0 5a/2a-&gt;2a;0 6a/4a-&gt;2a;0&lt;/rules&gt;\n\t\t&lt;startingSpikes&gt;2&lt;/startingSpikes&gt;\n\t\t&lt;delay&gt;0&lt;/delay&gt;\n\t\t&lt;spikes&gt;5&lt;/spikes&gt;\n\t\t&lt;isOutput&gt;false&lt;/isOutput&gt;\n\t\t&lt;isInput&gt;false&lt;/isInput&gt;\n\t\t&lt;out&gt;n2&lt;/out&gt;\n\t\t&lt;outWeights&gt;\n\t\t\t&lt;n2&gt;1&lt;/n2&gt;\n\t\t\t&lt;n3-nm2MDs9Nh&gt;1&lt;/n3-nm2MDs9Nh&gt;\n\t\t&lt;/outWeights&gt;\n\t&lt;/n1&gt;\n\t&lt;n2&gt;\n\t\t&lt;id&gt;n2&lt;/id&gt;\n\t\t&lt;position&gt;\n\t\t\t&lt;x&gt;282.5&lt;/x&gt;\n\t\t\t&lt;y&gt;197.0&lt;/y&gt;\n\t\t&lt;/position&gt;\n\t\t&lt;rules&gt;3a/2a-&gt;2a;0 5a/2a-&gt;2a;0 6a/4a-&gt;2a;0&lt;/rules&gt;\n\t\t&lt;startingSpikes&gt;3&lt;/startingSpikes&gt;\n\t\t&lt;delay&gt;0&lt;/delay&gt;\n\t\t&lt;spikes&gt;6&lt;/spikes&gt;\n\t\t&lt;isOutput&gt;false&lt;/isOutput&gt;\n\t\t&lt;isInput&gt;false&lt;/isInput&gt;\n\t\t&lt;out&gt;n4&lt;/out&gt;\n\t\t&lt;outWeights&gt;\n\t\t\t&lt;n4&gt;1&lt;/n4&gt;\n\t\t&lt;/outWeights&gt;\n\t&lt;/n2&gt;\n\t&lt;n4&gt;\n\t\t&lt;id&gt;n4&lt;/id&gt;\n\t\t&lt;position&gt;\n\t\t\t&lt;x&gt;456.5&lt;/x&gt;\n\t\t\t&lt;y&gt;204.0&lt;/y&gt;\n\t\t&lt;/position&gt;\n\t\t&lt;isOutput&gt;true&lt;/isOutput&gt;\n\t\t&lt;isInput&gt;false&lt;/isInput&gt;\n\t\t&lt;spikes&gt;0&lt;/spikes&gt;\n\t\t&lt;bitstring/&gt;\n\t&lt;/n4&gt;\n&lt;/content&gt;"
}
                    </pre>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/homogenize', methods = ['POST'])
def homogenize_input():

    # Get the JSON body of the request
    input: Dict[str, any] = request.json

    # Get the format of the input
    format_plain = input.get('format')
    format = JSON if format_plain == 'json' else YAML if format_plain == 'yaml' else XML

    # Get the SN P system from the body and convert it to an xmp format
    input_snp_system_xmp_str = input.get('snp_system')
    if format == JSON:
        input_snp_system_xmp_str = convert(input_snp_system_xmp_str, JSON, XML)
    elif format == YAML:
        input_snp_system_xmp_str = convert(input_snp_system_xmp_str, YAML, XML)
    


    # Get the scaling type to be used from the body
    scaling_type = input.get('scaling_type')

    # Parse the SN P system input and create an equivalent SNpSystem object
    snp_system_dict = SnpSystemDict(xmltodict.parse(input_snp_system_xmp_str))
    snp_system = SnpSystem.from_dict(snp_system_dict)  #! O(n^2 + nk + nt)

    # Homogenize the SN P system using the requested scaling type.
    if scaling_type == 0:
        homogenize_type_2_scaling(snp_system)
        auto_layout(snp_system)
    elif scaling_type == 1:
        homogenize_prime_released_spike_scaling(snp_system)  #! O(nk)
    else:
        raise ValueError("Invalid `scaling_type`. Please use 0 for Type-2 Subsystem Scaling or 1 for Released Spike Scaling")
    

    #!!print(f"Homogenized an SN P System")

    output_str = snp_system.to_xmp()
    if format == JSON:
        output_str = convert(output_str, XML, JSON)
    elif format == YAML:
        output_str = convert(output_str, XML, YAML)
    

    # Returns the original SN P system, its homogenized form, and if there are any errors encountered.
    return {
        'snp_system': input_snp_system_xmp_str,
        'homogenized_snp_system': output_str,
        'errors': None,
    }


if __name__ == "__main__":
    app.run(debug=True)