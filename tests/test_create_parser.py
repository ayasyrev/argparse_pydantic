import argparse

from argparse_pydantic.helpers import ArgumentParserCfg, create_parser
from argparse_pydantic.test_tools import parsers_actions_equal, parsers_args_equal


def test_create_parser_default():
    """test creation basic parser w/ default args"""
    parser_base = argparse.ArgumentParser()
    parser_cfg = ArgumentParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)
    assert parsers_args_equal(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)
    # create parser w/o args
    parser = create_parser()
    assert parsers_args_equal(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)


def test_create_parser():
    """test creation basic parser"""
    prog_name = "name"
    description = "Dummy prog."
    epilog = "nothing done..."
    parser_base = argparse.ArgumentParser(
        prog=prog_name, description=description, epilog=epilog
    )
    parser_cfg = ArgumentParserCfg(
        prog=prog_name,
        description=description,
        epilog=epilog,
    )
    parser = create_parser(parser_cfg=parser_cfg)
    assert parsers_args_equal(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)
