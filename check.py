#!/usr/bin/env python3
import importlib.util,tempfile,unittest,ipaddress
from pathlib import Path
def mod(name,file):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
dns=mod("dns","dns-rules.py");media=mod("media","prepare-media.py")
class Tests(unittest.TestCase):
    def test_client_scope(self):
        out=dns.render("192.0.2.10",["example.com","example.org"])
        self.assertEqual(out.count("$client=192.0.2.10"),2)
        self.assertNotIn("*",out)
    def test_reject_nonclient(self):
        for target in ["0.0.0.0","127.0.0.1","224.0.0.1","not-an-ip"]:
            with self.assertRaises(ValueError):dns.render(target,["example.com"])
    def test_loop(self):
        graph,cycle=media.graph(15,1,1)
        self.assertEqual(cycle,14)
        self.assertIn("trim=duration=2",graph)
        self.assertIn("xfade=",graph)
        self.assertIn("fps=24",graph)
    def test_invalid_loop(self):
        for values in [(1,1,1),(15,0,1),(15,1,100),(15,float("nan"),1)]:
            with self.assertRaises(ValueError):media.graph(*values)
if __name__=="__main__":unittest.main()
