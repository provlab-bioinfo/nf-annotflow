#!/usr/bin/env python3

import argparse
from Bio import SeqIO
import gzip
import re
import os


def open_fasta(file_path, mode='rt'):
    """Open FASTA or FASTA.GZ files seamlessly."""
    if file_path.endswith(".gz"):
        return gzip.open(file_path, mode)
    else:
        return open(file_path, mode)


def normalize_contig_id(raw_id):
    """
    Normalize contig IDs for consistent matching between report and FASTA headers.
    Example:
      '25PS-151M00028|Contig_28' -> 'Contig_28'
      'Contig_36_74.9631 [topology=circular]' -> 'Contig_36_74.9631'
    """
    raw_id = raw_id.split()[0]
    raw_id = raw_id.replace('[', '').replace(']', '')
    raw_id = re.sub(r'.*\|', '', raw_id)  # remove runid| prefix if present
    raw_id = re.sub(r'_Circ$', '', raw_id)
    return raw_id.strip()


def parse_contig_report(report_file):
    """
    Parse the contig report (TSV/CSV) and return a dict mapping contig_id → annotation info.
    """
    plasmid_info = {}

    with open(report_file, 'r') as infile:
        header = infile.readline().strip().split('\t')

        required_cols = [
            "sample_id", "molecule_type", "primary_cluster_id", "secondary_cluster_id",
            "contig_id", "size", "gc", "md5", "circularity_status",
            "rep_type(s)", "rep_type_accession(s)", "relaxase_type(s)", "relaxase_type_accession(s)",
            "mpf_type", "mpf_type_accession(s)", "orit_type(s)", "orit_accession(s)",
            "predicted_mobility", "mash_nearest_neighbor", "mash_neighbor_distance",
            "mash_neighbor_identification", "repetitive_dna_id", "repetitive_dna_type", "filtering_reason"
        ]

        col_idx = {col: header.index(col) for col in required_cols if col in header}

        for line in infile:
            if not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) < len(header):
                continue

            molecule_type = parts[col_idx["molecule_type"]].strip().lower()
            if molecule_type != "plasmid":
                continue

            raw_contig_id = parts[col_idx["contig_id"]].strip()
            contig_id = normalize_contig_id(raw_contig_id)

            plasmid_info[contig_id] = {
                col: parts[col_idx[col]].strip() if col in col_idx else "-"
                for col in required_cols
            }

    print(f"✅ Parsed {len(plasmid_info)} plasmid entries from {report_file}")
    return plasmid_info


def annotate_and_concat_fasta(report_file, fasta_files, output_file):
    """
    Annotate FASTA headers using contig_report and merge into one output file.
    Keeps the full original FASTA header, appending annotation info.
    """
    plasmid_info = parse_contig_report(report_file)

    count = 0
    with open(output_file, "w") as out_f:
        for fpath in fasta_files:
            if not os.path.exists(fpath):
                print(f"⚠️  Skipping missing file: {fpath}")
                continue

            with open_fasta(fpath, 'rt') as in_f:
                for record in SeqIO.parse(in_f, "fasta"):
                    base_id = normalize_contig_id(record.id)
                    if base_id not in plasmid_info:
                        print(f"⚠️  No annotation found for {record.id} in {fpath}")
                        continue

                    info = plasmid_info[base_id]
                    annotations = (
                        f'/primary_cluster_id="{info["primary_cluster_id"]}" '
                        f'/secondary_cluster_id="{info["secondary_cluster_id"]}" '
                        f'/circularity_status="{info["circularity_status"]}" '
                        f'/rep_type(s)="{info["rep_type(s)"]}" '
                        f'/rep_type_accession(s)="{info["rep_type_accession(s)"]}" '
                        f'/relaxase_type(s)="{info["relaxase_type(s)"]}" '
                        f'/relaxase_type_accession(s)="{info["relaxase_type_accession(s)"]}" '
                        f'/mpf_type="{info["mpf_type"]}" '
                        f'/mpf_type_accession(s)="{info["mpf_type_accession(s)"]}" '
                        f'/orit_type(s)="{info["orit_type(s)"]}" '
                        f'/orit_accession(s)="{info["orit_accession(s)"]}" '
                        f'/predicted_mobility="{info["predicted_mobility"]}" '
                        f'/mash_nearest_neighbor="{info["mash_nearest_neighbor"]}" '
                        f'/mash_neighbor_distance="{info["mash_neighbor_distance"]}" '
                        f'/mash_neighbor_identification="{info["mash_neighbor_identification"]}" '
                        f'/repetitive_dna_id="{info["repetitive_dna_id"]}" '
                        f'/repetitive_dna_type="{info["repetitive_dna_type"]}" '
                        f'/filtering_reason="{info["filtering_reason"]}"'
                    )

                    # ✅ Keep the full original header and append annotations
                    original_desc = record.description
                    record.description = f"{original_desc} {annotations}"

                    SeqIO.write(record, out_f, "fasta")
                    count += 1

    print(f"✅ Annotated {count} plasmid contigs.")
    print(f"💾 Output written to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Annotate plasmid FASTA headers using contig_report and merge into one FASTA file."
    )
    parser.add_argument(
        "-r", "--report", required=True,
        help="Path to contig_report.plasmid.csv (TSV format)"
    )
    parser.add_argument(
        "-f", "--fastas", nargs="+", required=True,
        help="List of plasmid FASTA files (.fasta or .fasta.gz)"
    )
    parser.add_argument(
        "-o", "--output", default="plasmid_all.fasta",
        help="Output merged annotated FASTA file"
    )

    args = parser.parse_args()
    annotate_and_concat_fasta(args.report, args.fastas, args.output)
