from typing import OrderedDict, Any, Literal

NeuronDict = OrderedDict[Literal[
    'id',
    'position'
    'isInput',
    'isOutput',
    'spikes',
    'delay',
    'rules',
    'startingSpikes',
    'out',
    'outWeights',
    'bitstring',
    ], Any]
