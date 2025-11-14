# nf-annotflow

A modular and reproducible Nextflow pipeline for comprehensive bacterial genome annotation, antimicrobial resistance (AMR) detection, plasmid typing, and sequence typing (MLST). nf-annotflow accepts assembled contigs in FASTA format and integrates multiple industry-standard bioinformatics tools to produce high-quality, reproducible bacterial genome annotations.

---

## Pipeline Summary

### Core Capabilities

- Annotates bacterial genomes or contigs from any assembler (e.g., **[nf-assemflow](https://github.com/xiaoli-dong/nf-assemflow)**)
- Comprehensive analysis suite:
  - 🧠 **Functional annotation** — [Bakta](https://github.com/oschwengers/bakta) for rapid and standardized bacterial genome annotation
  - 💊 **AMR gene detection** — [AMRFinderPlus](https://github.com/ncbi/amr) for identifying antimicrobial resistance genes
  - 🦠 **Virulence gene screening** — Comprehensive virulome analysis for pathogenicity assessment
  - 🔬 **Plasmid typing** — [MOB-suite](https://github.com/phac-nml/mob-suite) for plasmid reconstruction and typing
  - 🧩 **Sequence typing (MLST)** — [mlst](https://github.com/tseemann/mlst) for multi-locus sequence typing

### Key Features

- Consolidated summary tables and quality control reports
- Batch processing support for multiple samples
- Fully containerized (Docker/Singularity) for reproducibility
- Compatible with HPC, cloud, and local execution environments

---

## Quick Start

> [!NOTE]
> If you are new to Nextflow and nf-core, please refer to [this page](https://nf-co.re/docs/usage/installation) on how to set up Nextflow. Make sure to [test your setup](https://nf-co.re/docs/usage/introduction#how-to-run-a-pipeline) with `-profile test` before running the workflow on actual data.

### Check Workflow Options

You can clone or download nf-annotflow from GitHub to your local computer, or run the pipeline directly from GitHub. To check the pipeline command-line options:

```bash
# Running directly from GitHub without downloading or cloning
nextflow run xiaoli-dong/nf-annotflow -r <revision_number> --help

# Example with specific revision
nextflow run xiaoli-dong/nf-annotflow -r main --help
```

### Prepare Required Samplesheet Input

The nf-annotflow pipeline requires a CSV format samplesheet containing the assembled contig files for each sample. See below for what the samplesheet looks like:

**samplesheet.csv**

```csv
sample,contig_file
157M00046,157M00046.contigs_final.fasta
154M00027,154M00027.contigs_final.fasta
```

**Samplesheet Format Requirements:**

- The first row of the CSV file is the header describing the columns
- Each row represents a unique assembled genome
- `sample` — Unique sample identifier
- `contig_file` — Path to the assembled contigs in FASTA format

### Run the Pipeline

```bash
nextflow run xiaoli-dong/nf-annotflow \
  -profile singularity \
  --input samplesheet.csv \
  --outdir results \
  -resume
```

**Common profiles:** `docker`, `singularity`, `podman`, `conda`, or your institute-specific profile

> [!IMPORTANT]
> Please provide pipeline parameters via the CLI or Nextflow `-params-file` option. Custom config files including those provided by the `-c` Nextflow option can be used to provide any configuration **except for parameters**. See [documentation](https://nf-co.re/docs/usage/getting_started/configuration#custom-configuration-files) for more details.

---

## Command-Line Options

### Input/Output Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `--input` | string | Path to CSV samplesheet containing information about the samples |
| `--outdir` | string | Output directory where results will be saved (use absolute paths for cloud storage) |
| `--email` | string | Email address for completion summary |
| `--multiqc_title` | string | MultiQC report title (printed as page header, used for filename if not specified) |

### Analysis Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--skip_bakta` | boolean | `false` | Skip Bakta functional annotation |
| `--skip_mlst` | boolean | `false` | Skip MLST sequence typing |
| `--skip_mobsuite` | boolean | `false` | Skip MOB-suite plasmid analysis |
| `--skip_virulome` | boolean | `false` | Skip virulence gene screening |
| `--skip_amr` | boolean | `false` | Skip antimicrobial resistance gene detection |

### Database Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--bakta_db` | string | `/nfs/APL_Genomics/db/prod/bakta/v6` | Path to Bakta database |
| `--amrfinderplus_db` | string | `/nfs/Genomics_DEV/projects/xdong/deve/pathogenseq2/db/AMRFinderPlus/latest` | Path to AMRFinderPlus database |

### Generic Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `--multiqc_methods_description` | string | Custom MultiQC YAML file containing HTML with methods description |

### Help Options

| Parameter | Description |
|-----------|-------------|
| `--help` | Show help for all top-level parameters (can specify a parameter for detailed help) |
| `--help_full` | Show help for all non-hidden parameters |
| `--show_hidden` | Show hidden parameters (use with `--help` or `--help_full`) |

---

## Workflow Overview

```
Assembled Contigs (FASTA)
    ↓
Functional Annotation (Bakta)
    ↓
AMR Detection (AMRFinderPlus)
    ↓
Virulence Gene Screening (Virulome)
    ↓
Plasmid Typing (MOB-suite)
    ↓
Sequence Typing (MLST)
    ↓
Summary Reports & MultiQC
    ↓
Final Outputs
```

---
<!--
## Output Structure

```
results/
├── bakta/               # Functional annotations (GFF3, GenBank, etc.)
├── amrfinderplus/       # AMR gene predictions
├── virulome/            # Virulence gene screening results
├── mobsuite/            # Plasmid reconstruction and typing
├── mlst/                # Multi-locus sequence typing results
├── multiqc/             # MultiQC aggregated quality reports
├── summary/             # Consolidated summary tables
└── pipeline_info/       # Pipeline execution reports
```

---
-->
## Database Requirements

nf-annotflow requires several databases to be downloaded and configured:

### Bakta Database
```bash
# Download Bakta database (light or full version)
bakta_db download --output <bakta_db_path> --type full

# Or download directly from Zenodo
# Visit: https://zenodo.org/communities/bakta
# Choose the appropriate database version (light or full)
```

### AMRFinderPlus Database
```bash
# Download AMRFinderPlus database
amrfinder_update --database <amrfinderplus_db_path>
```

Provide database paths using the respective parameters (e.g., `--bakta_db`, `--amrfinderplus_db`).

---

## Tool References

This pipeline uses the following tools:

- [**Bakta**](https://github.com/oschwengers/bakta) — Rapid and standardized annotation of bacterial genomes
- [**AMRFinderPlus**](https://github.com/ncbi/amr) — Antimicrobial resistance gene detection
- [**MOB-suite**](https://github.com/phac-nml/mob-suite) — Software tools for clustering, reconstruction and typing of plasmids
- [**mlst**](https://github.com/tseemann/mlst) — Multi-locus sequence typing from assembled contigs
- [**MultiQC**](https://multiqc.info/) — Aggregate results from bioinformatics analyses

---

## Citations

If you use nf-annotflow in your research, please cite the appropriate tools:

- **Bakta** — Schwengers, O., et al. (2021). Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification. *Microbial Genomics*, 7(11).
- **AMRFinderPlus** — Feldgarden, M., et al. (2021). AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence. *Scientific Reports*, 11, 12728.
- **MOB-suite** — Robertson, J., & Nash, J. H. E. (2018). MOB-suite: software tools for clustering, reconstruction and typing of plasmids from draft assemblies. *Microbial Genomics*, 4(8).
- **mlst** — Seemann, T. mlst: scan contig files against PubMLST typing schemes. GitHub repository.
- **MultiQC** — Ewels, P., et al. (2016). MultiQC: summarize analysis results for multiple tools and samples in a single report. *Bioinformatics*, 32(19), 3047-3048.

---

## Credits

nf-annotflow was originally written by Xiaoli Dong.

## Support

For issues, questions, or feature requests, please [open an issue](https://github.com/xiaoli-dong/nf-annotflow/issues) on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
