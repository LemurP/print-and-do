from click.testing import CliRunner

from pado import cli


def test_no_args_command_line_shows_help():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_help_command_shows_message_and_exits():
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
