include { BAKTA_BAKTA } from '../../modules/local/bakta/bakta/main'
include { ABRITAMR_RUN } from '../../modules/local/abritamr/run/main'
include { MLST } from '../../modules/local/mlst/main'
include { ABRICATE_RUN as ABRICATE_RUN_VF } from '../../modules/local//abricate/run/main'
include { ABRICATE_SUMMARY as ABRICATE_SUMMARY_VF } from '../../modules/local/abricate/summary/main'
include { GFF2FEATURES as GFF2FEATURES_BAKTA } from '../../modules/local/gff2features'
include { AMRFINDERPLUS_RUN } from '../../modules/local/amrfinderplus/run/main'
include { MOBSUITE_RECON } from '../../modules/local/mobsuite/recon/main'
include { CSVTK_FILTER2 } from '../../modules/local/csvtk/filter2/main'
include {
    CSVTK_CONCAT as CSVTK_CONCAT_STATS_BAKTA ;
    CSVTK_CONCAT as CSVTK_CONCAT_MOBTYPER_RESULTS ;
    CSVTK_CONCAT as CSVTK_CONCAT_CONTIG_REPORT ;
    CSVTK_CONCAT as CSVTK_CONCAT_AMR ;
    CSVTK_CONCAT as CSVTK_CONCAT_MLST
} from '../../modules/local/csvtk/concat/main'

include { MOBSUITE_ANNOTATEPLASMID } from '../../modules/local/mobsuite/annotateplasmid'
/*
    https://www.ncbi.nlm.nih.gov/pathogens/
 */
workflow ANNOTATION {
    take:
    contigs
    bakta_db //channel: path to bakta_db
    amrfinderplus_db //channel: path to amrfinderplus_db

    main:

    ch_software_versions = channel.empty()

    if (!params.skip_bakta) {
        BAKTA_BAKTA(contigs, bakta_db, [], [])
        GFF2FEATURES_BAKTA(BAKTA_BAKTA.out.gff)
        ch_software_versions = ch_software_versions.mix(BAKTA_BAKTA.out.versions)
        CSVTK_CONCAT_STATS_BAKTA(
            GFF2FEATURES_BAKTA.out.tsv.map { cfg, stats -> stats }.collect().map { files -> tuple([id: "annotation.bakta"], files) },
            'tsv',
            'tsv',
        )
    }
    //metaerg:  metaerg --contig_file 25PS-157M00046.contigs_final.fasta  --database_dir /nfs/APL_Genomics/db/prod/metaerg --file_extension .fasta --skip_step antismash,padloc --output_dir 25PS-157M00046 --cpus 8 --force all --delimiter '|'

    //ARG(contigs, ffn, faa)

    if (!params.skip_amr) {

        AMRFINDERPLUS_RUN(contigs, amrfinderplus_db)
        ch_software_versions = ch_software_versions.mix(AMRFINDERPLUS_RUN.out.versions)
        CSVTK_CONCAT_AMR(
            AMRFINDERPLUS_RUN.out.report.map { cfg, amr -> amr }.collect().map { files -> tuple([id: "amr.amrfinderplus"], files) },
            'tsv',
            'tsv',
        )
    }
    if (!params.skip_virulome) {
        //virulome
        ABRICATE_RUN_VF(contigs)
        ch_software_versions = ch_software_versions.mix(ABRICATE_RUN_VF.out.versions)
        ABRICATE_SUMMARY_VF(
            ABRICATE_RUN_VF.out.report.collect { meta, report -> report }.map { report -> [[id: "virulome"], report] }
        )
    }
    if (!params.skip_mlst) {
        MLST(contigs)
        ch_software_versions = ch_software_versions.mix(MLST.out.versions)
        MLST.out.tsv.map { cfg, mlst -> mlst }.collect()
        //.view()
        CSVTK_CONCAT_MLST(
            MLST.out.tsv.map { cfg, mlst -> mlst }.collect().map { files -> tuple([id: "mlst.mlst"], files) },
            'tsv',
            'tsv',
        )
    }
    if (!params.skip_mobsuite) {
        MOBSUITE_RECON(contigs)
        ch_software_versions = ch_software_versions.mix(MOBSUITE_RECON.out.versions)

        ch_mobtyper_results = MOBSUITE_RECON.out.mobtyper_results
            .map { cfg, plasmid -> plasmid }
            .collect()
            .map { files -> tuple([id: "plasmid.mobtyper_results"], files) }

        ch_mobtyper_results.view()

        CSVTK_CONCAT_MOBTYPER_RESULTS(
            ch_mobtyper_results,
            'tsv',
            'tsv',
        )

        //only keep plasmid
        CSVTK_FILTER2(MOBSUITE_RECON.out.contig_report)
        CSVTK_CONCAT_CONTIG_REPORT(
            CSVTK_FILTER2.out.csv.filter { cfg, pcsv -> pcsv.countLines() > 1 }
            .map { cfg, pcsv -> pcsv }.collect()
            .map { files -> tuple([id: "plasmid.contig_report.plasmid"], files) },
            'tsv',
            'tsv',
        )

        //get all the plasmid
        MOBSUITE_RECON.out.plasmids.view()
        MOBSUITE_ANNOTATEPLASMID (MOBSUITE_RECON.out.contig_report.join(MOBSUITE_RECON.out.plasmids))
    }




    emit:
    versions = ch_software_versions
}
