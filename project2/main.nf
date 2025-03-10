workflow {
    // Define the metadata file and pdb files
    def metadataFile = file('data0/cath-names-v4_3_0_levels.txt')
    def data_path = 'data0/files'
    def pdbFiles = Channel.fromPath("${data_path}/*.pdb")
    
    // Create the metadata channel
    def metadata = Channel
        .fromPath(metadataFile)
        .splitCsv(sep: '\t', strip: true)

    // Filter out rows without corresponding files in the pdbFiles directory
    def validData = metadata
        .filter { row -> 
            def pdbFile = file("${data_path}/${row[0]}.pdb")
            pdbFile.exists()
        }

    // Mapping pdbFiles to create tuples of base name (without extension) and file path
    def pdbFilesWithNames = pdbFiles
        .map { file -> 
            def baseName = file.getBaseName()
            tuple(baseName, file)
        }

    // Debug: Print the first element of each channel
    validData
        .take(1)
        .view { println "First validData element: ${it}" }

    pdbFilesWithNames
        .take(1)
        .view { println "First pdbFilesWithNames element: ${it}" }

    // Join validDataWithNames and pdbFilesWithNames based on the base name
    def pairedData = validData
        .join(pdbFilesWithNames, by: 0)
        .map { _, meta1, meta2, meta3, meta4, file ->
            // Return a tuple of metadata and file path
            tuple(file, [meta1, meta2, meta3, meta4])
        }

    // Debug: Print the first paired data element
    pairedData
        .take(1)
        .view { println "First paired data: ${it}" }

    // Pass the paired data into the generateDistanceMap process
    generateDistanceMap(pairedData)
}

process generateDistanceMap {
    input:
    tuple path(pdbFile), val(metadataRow)  // Receive a tuple of pdbFile and metadata row
    errorStrategy 'retry'
    publishDir "results", mode: 'copy' 
    
    output:
    file "*.npy"

    script:
    """
    python3 ${baseDir}/extract_pdb_info.py ${pdbFile} ${metadataRow[0]} ${metadataRow[1]} ${metadataRow[2]} ${metadataRow[3]}
    """
}