# coding: utf-8

# Python libs
from __future__ import absolute_import
import logging

# Salt testing libs
from tests.support.unit import skipIf, TestCase
from tests.support.mock import NO_MOCK, NO_MOCK_REASON, patch, MagicMock, mock_open
from tests.support.mixins import LoaderModuleMockMixin

# Salt libs
import salt.beacons.wtmp as wtmp
from salt.ext import six

raw = b'\x07\x00\x00\x00H\x18\x00\x00pts/14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00s/14gareth\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13I\xc5YZf\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
pack = (7, 6216, b'pts/14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b's/14', b'gareth\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'::1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0, 0, 0, 1506101523, 353882, 0, 0, 0, 16777216)

log = logging.getLogger(__name__)


@skipIf(NO_MOCK, NO_MOCK_REASON)
class WTMPBeaconTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test case for salt.beacons.[s]
    '''

    def setup_loader_modules(self):
        return {
            wtmp: {
                '__context__': {'wtmp.loc': 2},
                '__salt__': {},
            }
        }

    def test_non_list_config(self):
        config = {}
        ret = wtmp.validate(config)

        self.assertEqual(ret, (False, 'Configuration for wtmp beacon must'
                                      ' be a list.'))

    def test_empty_config(self):
        config = [{}]

        ret = wtmp.validate(config)

        self.assertEqual(ret, (True, 'Valid beacon configuration'))

    def test_no_match(self):
        config = [{'users': {'gareth': {'time': {'end': '5pm',
                                                 'start': '3pm'}}}}
                  ]

        ret = wtmp.validate(config)

        self.assertEqual(ret, (True, 'Valid beacon configuration'))

        with patch('salt.utils.files.fopen', mock_open(b'')) as m_open:
            ret = wtmp.beacon(config)
            call_args = next(six.itervalues(m_open.filehandles))[0].call.args
            assert call_args == (wtmp.WTMP, 'rb'), call_args
            assert ret == [], ret

    def test_match(self):
        with patch('salt.utils.files.fopen',
                   mock_open(read_data=raw)):
            with patch('struct.unpack',
                       MagicMock(return_value=pack)):
                config = [{'users': {'gareth': {}}}]

                ret = wtmp.validate(config)

                self.assertEqual(ret, (True, 'Valid beacon configuration'))

                _expected = [{'PID': 6216,
                              'line': 'pts/14',
                              'session': 0,
                              'time': 0,
                              'exit_status': 0,
                              'inittab': 's/14',
                              'type': 7,
                              'addr': 1506101523,
                              'hostname': '::1',
                              'user': 'gareth'}]

                ret = wtmp.beacon(config)
                log.debug('{}'.format(ret))
                self.assertEqual(ret, _expected)

    def test_match_time(self):
        with patch('salt.utils.files.fopen',
                   mock_open(read_data=raw)):
            with patch('time.time',
                       MagicMock(return_value=1506121200)):
                with patch('struct.unpack',
                           MagicMock(return_value=pack)):
                    config = [{'users': {'gareth': {'time': {'end': '5pm',
                                                             'start': '3pm'}}}}
                              ]

                    ret = wtmp.validate(config)

                    self.assertEqual(ret, (True, 'Valid beacon configuration'))

                    _expected = [{'PID': 6216,
                                  'line': 'pts/14',
                                  'session': 0,
                                  'time': 0,
                                  'exit_status': 0,
                                  'inittab': 's/14',
                                  'type': 7,
                                  'addr': 1506101523,
                                  'hostname': '::1',
                                  'user': 'gareth'}]

                    ret = wtmp.beacon(config)
                    self.assertEqual(ret, _expected)
