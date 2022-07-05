"""
Read assembly and evaluation for metagenomics data
"""

import subprocess
from pathlib import Path

from latch import message, small_task, workflow
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
        section_title="MEGAHIT",
    ),
    "sample_name": LatchParameter(
        display_name="Sample name",
        description="Sample name (will define output file names)",
        section_title="MEGAHIT",
    ),
    "k_min": LatchParameter(
        display_name="Minimum kmer size",
        description="Must be odd and <=255",
        section_title="MEGAHIT",
    ),
    "k_max": LatchParameter(
        display_name="Maximum kmer size",
        description="Must be odd and <=255",
        section_title="MEGAHIT",
    ),
    "k_step": LatchParameter(
        display_name="Increment of kmer size of each iteration",
        section_title="MEGAHIT",
        description="Must be even and <=28",
    ),
    "min_count": LatchParameter(
        display_name="Minimum multiplicity for filtering (k_min+1)-mers",
        section_title="MEGAHIT",
    ),
    "min_contig_len": LatchParameter(
        display_name="Minimum length of contigs to output",
        section_title="MEGAHIT",
    ),
}


@small_task
def megahit(
    read_1: LatchFile,
    read_2: LatchFile,
    sample_name: str,
    min_count: int,
    k_min: int,
    k_max: int,
    k_step: int,
    min_contig_len: int,
) -> LatchDir:

    # Check input values are as expected for MEGAHit
    if all([k_min % 2 != 0, k_max % 2 != 0, k_step % 2 == 0]) != True:
        title = "Invalid K list selected"
        body = "Both k min and k max have to be odd numbers, while k step must be even."
        message(typ="error", data={"title": title, "body": body})

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
def metagenomic_assembly(
    read_1: LatchFile,
    read_2: LatchFile,
    sample_name: str = "assembly_sample",
    min_count: int = 2,
    k_min: int = 21,
    k_max: int = 141,
    k_step: int = 12,
    min_contig_len: int = 200,
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
