import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SERVER=ROOT/'chatgpt/een-pod-suite/scripts/reader_mcp.py'
spec=importlib.util.spec_from_file_location('reader',SERVER)
reader=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def call(name,arguments):
    return reader.rpc({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':name,'arguments':arguments}})['result']


class ReaderTests(unittest.TestCase):
    def test_initialization_and_read_only_discovery(self):
        response=reader.rpc({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26'}})
        self.assertEqual(response['result']['protocolVersion'],'2025-03-26')
        self.assertEqual(len(reader.TOOLS),3)
        for tool in reader.TOOLS:
            self.assertTrue(tool['annotations']['readOnlyHint'])
            self.assertFalse(tool['annotations']['destructiveHint'])

    def test_direct_profile_url_and_reference_are_forwarded(self):
        url='https://een.ec.europa.eu/partnering-opportunities/example'
        with patch.object(reader.public,'read_profile',return_value={'status':'FOUND EXACT','reference':'BOAL20261006010'}) as lookup:
            result=call('get_public_profile',{'url':url})
            lookup.assert_called_once_with(url,None)
            self.assertFalse(result['isError'])

    def test_access_failure_is_an_error_not_a_successful_audit(self):
        with patch.object(reader.public,'read_profile',return_value={'status':'ACCESS BLOCKED','reference':'BOAL20261006010'}):
            self.assertTrue(call('get_public_profile',{'url':'https://een.ec.europa.eu/partnering-opportunities/example'})['isError'])

    def test_reference_or_name_discovery_is_rejected(self):
        self.assertTrue(call('get_public_profile',{'reference':'BOAL20261006010'})['isError'])
        self.assertTrue(call('get_public_profile',{'name':'Tour operator'})['isError'])
        self.assertTrue(call('get_api_profile',{'reference':'BOAL20261006010'})['isError'])

    def test_arguments_cannot_supply_credentials_or_arbitrary_endpoints(self):
        self.assertTrue(call('get_live_labels',{'data_type':'market_keyword','api_key':'secret'})['isError'])
        self.assertTrue(call('get_public_profile',{'reference':'x','base_url':'https://example.com'})['isError'])
        self.assertTrue(call('delete_profile',{'reference':'x'})['isError'])

    def test_exception_redaction(self):
        with patch.dict(reader.os.environ,{'EEN_API_KEY':'test-sensitive','EEN_AGENT_TOKEN':'test-auth'}), patch.object(reader.public,'read_profile',side_effect=RuntimeError('test-sensitive test-auth')):
            result=call('get_public_profile',{'url':'https://een.ec.europa.eu/partnering-opportunities/example'})
            self.assertNotIn('test-sensitive',json.dumps(result))
            self.assertNotIn('test-auth',json.dumps(result))

    def test_form_count_does_not_claim_completeness(self):
        result=call('check_form_limits',{'profile_type':'BO','fields':{'title':'X'*257,'summary':''}})['structuredContent']
        self.assertEqual(result['fields']['title']['status'],'OVER LIMIT by 1')
        self.assertFalse(result['fields']['summary']['populated'])
        self.assertIn('mandatory content',result['scope'])

    def test_stdio_transport_end_to_end(self):
        messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26'}},{'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'},{'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'check_form_limits','arguments':{'profile_type':'TR','fields':{'technical':'X'*2001}}}}]
        result=subprocess.run([sys.executable,str(SERVER)],input='\n'.join(map(json.dumps,messages))+'\n',text=True,capture_output=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        responses=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([r['id'] for r in responses],[1,2,3])
        self.assertEqual(len(responses[1]['result']['tools']),3)
        self.assertEqual(responses[2]['result']['structuredContent']['fields']['technical']['status'],'OVER LIMIT by 1')

    def test_http_requires_authentication_secret(self):
        env=dict(reader.os.environ);env.pop('EEN_AGENT_TOKEN',None)
        result=subprocess.run([sys.executable,str(SERVER),'--http'],env=env,text=True,capture_output=True,timeout=5)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('requires EEN_AGENT_TOKEN',result.stderr)


if __name__=='__main__': unittest.main()
