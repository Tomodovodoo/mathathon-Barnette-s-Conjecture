"""Single-command lab test entry point; requires the repository's plantri setup."""
import argparse
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tier', choices=['quick','full'])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.discover(str(HERE/'tests'))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    from barnette_lab.campaign import main as campaign
    sys.argv = [sys.argv[0], '--tier', args.tier]
    if args.output:
        sys.argv += ['--output',str(args.output)]
    campaign()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
