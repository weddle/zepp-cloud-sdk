from zepp_cloud.cli import main as cli_main


def test_cli_version_flag(capsys):
    try:
        cli_main(["--version"])  # type: ignore[arg-type]
    except SystemExit as e:
        # Expect exit after printing version
        assert e.code == 0

    out = capsys.readouterr().out.strip()
    assert out
