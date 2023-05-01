from typing import OrderedDict, Literal
from .content_dict import ContentDict


SnpSystemDict = OrderedDict[Literal['content'], ContentDict]


#!! SAMPLE
# a = OrderedDict([
#     ('content', OrderedDict([
#         ('n1', OrderedDict([
#             ('id', 'n1'),
#             ('position', OrderedDict([('x', '66.5'), ('y', '222')])),
#             ('rules', 'a/a->a;0 2a/a->a;0'),
#             ('startingSpikes', '1'),
#             ('delay', '0'),
#             ('spikes', '1'),
#             ('isOutput', 'false'),
#             ('isInput', 'false'),
#             ('out', 'n2'),
#             ('outWeights', OrderedDict([('n2', '1'), ('n3-nm2MDs9Nh', '1')]))
#         ])),
#         ('n2', OrderedDict([
#             ('id', 'n2'),
#             ('position', OrderedDict([('x', '282.5'), ('y', '197')])),
#             ('rules', '3a/2a->a;0'),
#             ('startingSpikes', '3'),
#             ('delay', '0'),
#             ('spikes', '3'),
#             ('isOutput', 'false'),
#             ('isInput', 'false'),
#             ('out', 'n4'),
#             ('outWeights', OrderedDict([('n4', '1')]))
#         ])),
#         ('n4', OrderedDict([
#             ('id', 'n4'),
#             ('position', OrderedDict([('x', '456.5'), ('y', '204')])),
#             ('isOutput', 'true'),
#             ('isInput', 'false'),
#             ('spikes', '0'),
#             ('bitstring', None)
#         ])),
#         ('n0-j5Lto5JHr', OrderedDict([
#             ('id', 'n0-j5Lto5JHr'),
#             ('position', OrderedDict([('x', '-125.5'), ('y', '188')])),
#             ('isInput', 'true'),
#             ('isOutput', 'false'),
#             ('spikes', '0'),
#             ('delay', '0'),
#             ('out', 'n1'),
#             ('bitstring', '0,0,1'),
#             ('outWeights', OrderedDict([('n1', '1')]))
#         ]))
#     ]))
# ])