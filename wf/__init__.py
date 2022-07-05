"""
Read assembly and evaluation for metagenomics data
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchAuthor, LatchDir, LatchFile, LatchMetadata, LatchParameter

METASSEMBLY_DOCS = LatchMetadata(
    display_name="MetAssembly",
    author=LatchAuthor(
        name="jvfe",
        github="https://github.com/jvfe",
    ),
    repository="https://github.com/jvfe/metassembly_latch",
    license="MIT",
)

METASSEMBLY_DOCS.parameters = {
    "read_1": LatchParameter(
        display_name="Read 1",
        description="Paired-end read 1 file.",
        section_title="MEGAHIT",
    ),
    "read_2": LatchParameter(
        display_name="Read 2",
        description="Paired-end read 2 file.",
    ),
    "sample_name": LatchParameter(
        display_name="Sample name",
        description="Sample name (will define output file names)",
    ),
    "k_min": LatchParameter(
        display_name="Minimum kmer size",
        description="Must be odd and <=255",
    ),
    "k_max": LatchParameter(
        display_name="Maximum kmer size",
        description="Must be odd and <=255",
    ),
    "k_step": LatchParameter(
        display_name="Increment of kmer size of each iteration",
        description="Must be even and <=28",
    ),
    "min_count": LatchParameter(
        display_name="Minimum multiplicity for filtering (k_min+1)-mers",
    ),
    "min_contig_len": LatchParameter(
        display_name="Minimum length of contigs to output",
    ),
}


@small_task
def megahit(
    read_1: LatchFile,
    read_2: LatchFile,
    sample_name: str,
    min_count: str,
    k_min: str,
    k_max: str,
    k_step: str,
    min_contig_len: str,
) -> LatchDir:

    output_dir_name = f"MEGAHIT-{sample_name}"
    output_dir = Path(output_dir_name).resolve()
    _megahit_cmd = [
        "/root/megahit",
        "--min-count",
        min_count,
        "--k-min",
        k_min,
        "--k-max",
        k_max,
        "--k-step",
        k_step,
        "--out-dir",
        output_dir_name,
        "--out-prefix",
        sample_name,
        "--min-contig-len",
        min_contig_len,
        "-1",
        read_1.local_path,
        "-2",
        read_2.local_path,
    ]

    subprocess.run(_megahit_cmd)

    return LatchDir(str(output_dir), f"latch:///{output_dir_name}")


@workflow(METASSEMBLY_DOCS)
def metassembly(
    read_1: LatchFile,
    read_2: LatchFile,
    sample_name: str = "assembly_sample",
    min_count: str = "2",
    k_min: str = "21",
    k_max: str = "141",
    k_step: str = "12",
    min_contig_len: str = "200",
) -> LatchDir:
    return megahit(
        read_1=read_1,
        read_2=read_2,
        sample_name=sample_name,
        min_count=min_count,
        k_min=k_min,
        k_max=k_max,
        k_step=k_step,
        min_contig_len=min_contig_len,
    )
