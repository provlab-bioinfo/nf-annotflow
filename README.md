# nf-annotflow: Comprehensive Genome Annotation and Typing Pipeline (Nextflow)

**nf-annotflow** is a modular and reproducible **Nextflow pipeline** for bacterial genome annotation, antimicrobial resistance (AMR) detection, plasmid typing, and sequence typing (MLST).  
It integrates several widely used bioinformatics tools — Bakta, AMRFinderPlus, Abricate, MobSuite, and MLST — to produce high-quality and reproducible bacterial genome annotation outputs.

---

## Features

- Annotates bacterial genomes or contigs from any assembler (e.g., from **[nf-assemflow](https://github.com/xiaoli-dong/nf-assemflow)**)
- Performs:
  - 🧠 **Functional annotation** with [Bakta](https://github.com/oschwengers/bakta)  
  - 💊 **AMR gene detection** with [AMRFinderPlus](https://github.com/ncbi/amr)  
  - 🧫 **Resistance & virulence screening** with [Abricate](https://github.com/tseemann/abricate)  
  - 🔬 **Plasmid typing** with [MobSuite](https://github.com/phac-nml/mob-suite)  
  - 🧩 **Sequence typing (MLST)** with [MLST](https://github.com/tseemann/mlst)  
- Consolidates results into summary tables and QC reports
- Supports **batch processing** of multiple samples
- Fully containerized (Docker / Singularity) for reproducibility
- Compatible with HPC, cloud, and local execution environments

---

## Usage

> [!NOTE]
> If you are new to Nextflow and nf-core, please refer to [this page](https://nf-co.re/docs/usage/installation) on how to set-up Nextflow. Make sure to [test your setup](https://nf-co.re/docs/usage/introduction#how-to-run-a-pipeline) with `-profile test` before running the workflow on actual data.

<!-- TODO nf-core: Describe the minimum required steps to execute the pipeline, e.g. how to prepare samplesheets.
     Explain what rows and columns represent. For instance (please edit as appropriate):

First, prepare a samplesheet with your input data that looks as follows:

`samplesheet.csv`:

```csv
sample,fastq_1,fastq_2
CONTROL_REP1,AEG588A1_S1_L002_R1_001.fastq.gz,AEG588A1_S1_L002_R2_001.fastq.gz
```

Each row represents a fastq file (single-end) or a pair of fastq files (paired end).

-->

Now, you can run the pipeline using:

<!-- TODO nf-core: update the following command to include all required parameters for a minimal example -->

```bash
nextflow run xiaoli-dong/nf-annotflow \
   -profile <docker/singularity/.../institute> \
   --input samplesheet.csv \
   --outdir <OUTDIR>
```

> [!WARNING]
> Please provide pipeline parameters via the CLI or Nextflow `-params-file` option. Custom config files including those provided by the `-c` Nextflow option can be used to provide any configuration _**except for parameters**_; see [docs](https://nf-co.re/docs/usage/getting_started/configuration#custom-configuration-files).

## Credits

xiaoli-dong/annotflow was originally written by Xiaoli Dong.
