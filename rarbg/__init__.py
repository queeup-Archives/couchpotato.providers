from .main import Rarbg


def autoload():
    return Rarbg()

config = [{
    'name': 'rarbg',
    'groups': [
        {
            'tab': 'searcher',
            'list': 'torrent_providers',
            'name': 'Rarbg',
            'description': '<a href="https://www.rarbg.com/">Rarbg</a>',
            'wizard': False,
            'icon': 'AAABAAEAEBAAAAAAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAQAQAAAAAAAAAAAAAAAAAAAAAAAD///8B////L////5n///+l////o////6H///83////Af///wv///+B////p////6P///+l////n////zf///8D////Rf///8n06en/1MnJ/9TJv//p39//////0f///wH///+N/////9TUyf/Uycn/1Mm//9/U1P/////Z////Vf///3H////vv6qf/z8KAP8/CgD/impV/////+v///97////+bSflP8/FQD/PwoA/0oVAP/Jv7T/////4f///13///9x////77+0qv9VHwD/VRUA/5R0X//////7////99/Uyf9fKhX/VR8K/1UVAP+0n5T//////////1////8F////cf///+/JtKr/aioK/18fCv+fdGr///////T09P9/SjX/aioK/18fCv+qf2r//////////4X///8B////Af///3H////v1LSq/3QqCv90Kgr/qn9q//////+qf2r/dCoK/3Q1Ff+fakr//////////7X///8H////Af///wH///9x////79+/tP+USir/ij8f/5RVNf+fX0r/ij8f/4o/H/+USir/9N/f//////H///8l////Af///wH///8B////cf///+/pyb//tHRV/7R0Vf+qakr/n1Uq/59VKv+fSir/n0oq/8mUf///////////hf///wH///8B////Af///3H////v6cm//790Vf+/f1X/yZR//+nJv//fv7T/yYp0/7R0Vf+0Xz//1LSf//////H///8h////Af///wH///9x////7+nJv/+/dFX/v3RV/9SqlP///////////fTf3/+/f1//v3RV/8mKav////T/////X////wH///8B////cf///+/pyb//v3RK/790Sv/UqpT///////////3/6en/yX9V/790Sv/Jf1X//+np/////4H///8B////Af///3H////v6cm//79qP/+/akr/1Ip0/+nJv//pyb//1JR0/79qSv+/aj//yX9f////9P////9n////Af///wH///9x////7+nJtP+/XzX/v2o//79fNf+/XzX/v181/79fNf+/XzX/v181/+m/qv/////3////Kf///wH///8B////cf///+/p1L//yXRV/8l/Vf/Jf1X/yX9V/8l/Vf/Jf1//1JR0/+nUv///////////jf///wH///8B////Af///zn///+7///////////////////////////////////////////////x////ff///wX///8B////Af///wH///8B////H////3v///+H////hf///4X///+F////hf///4X///9n////Jf///wH///8B////Af///wH///8BAAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//w==',
            'options': [
                {
                    'name': 'enabled',
                    'type': 'enabler',
                    'default': False
                },
                {
                    'name': 'seed_ratio',
                    'label': 'Seed ratio',
                    'type': 'float',
                    'default': 1,
                    'description': 'Will not be (re)moved until this seed ratio is met.',
                },
                {
                    'name': 'seed_time',
                    'label': 'Seed time',
                    'type': 'int',
                    'default': 40,
                    'description': 'Will not be (re)moved until this seed time (in hours) is met.',
                },
                {
                    'name': 'extra_score',
                    'advanced': True,
                    'label': 'Extra Score',
                    'type': 'int',
                    'default': 0,
                    'description': 'Starting score for each release found via this provider.',
                }
            ],
        }
    ]
}]
