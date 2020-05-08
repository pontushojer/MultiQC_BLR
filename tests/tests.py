from pathlib import Path
from shutil import copyfile
import subprocess

TESTDATA_STATS = Path("tests/data/example_stats.log")
TESTDATA_HAPCUT2_PHASING_STATS = Path("tests/data/example_hapcut2_phasing_stats.txt")
TESTDATA_HAPCUT2_PHASEBLOCK = Path("tests/data/example_hapcut2.phase")


EXPECTED_OUTPUT_STATS = Path("tests/expected_output/example_stats.txt")
EXPECTED_OUTPUT_HAPCUT2_PHASING_STATS = Path("tests/expected_output/hapcut2_phasing_stats.txt")
EXPECTED_OUTPUT_HAPCUT2_PHASEBLOCK_LEN = Path("tests/expected_output/hapcut2_phaseblock_lengths.txt")


def comp_files_linewise(file1: Path, file2: Path):
    with open(file1) as f1, open(file2) as f2:
        for l_f1, l_f2 in zip(f1, f2):
            assert l_f1 == l_f2


def test_stats(tmpdir):
    copyfile(TESTDATA_STATS, tmpdir / "example.log")

    subprocess.run(["multiqc", "-f", tmpdir, "-o", tmpdir])

    assert Path(tmpdir / "multiqc_report.html").exists()
    assert Path(tmpdir / "multiqc_data" / "example_stats.txt").exists()

    comp_files_linewise(Path(tmpdir / "multiqc_data" / "example_stats.txt"),
                        EXPECTED_OUTPUT_STATS)


def test_hapcut2(tmpdir):
    copyfile(TESTDATA_HAPCUT2_PHASING_STATS, tmpdir / "example.txt")
    copyfile(TESTDATA_HAPCUT2_PHASEBLOCK, tmpdir / "example.phase")

    subprocess.run(["multiqc", "-f", tmpdir, "-o", tmpdir])

    assert Path(tmpdir / "multiqc_report.html").exists()
    assert Path(tmpdir / "multiqc_data" / "hapcut2_phasing_stats.txt").exists()
    assert Path(tmpdir / "multiqc_data" / "hapcut2_phaseblock_lengths.txt").exists()

    comp_files_linewise(Path(tmpdir / "multiqc_data" / "hapcut2_phasing_stats.txt"),
                        EXPECTED_OUTPUT_HAPCUT2_PHASING_STATS)
    comp_files_linewise(Path(tmpdir / "multiqc_data" / "hapcut2_phaseblock_lengths.txt"),
                        EXPECTED_OUTPUT_HAPCUT2_PHASEBLOCK_LEN)

