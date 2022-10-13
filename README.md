### Execute a basic 2-d principal component analysis

This repository contains a WebMeV-compatible analysis tool for performing a 2-d PCA analysis. 
It creates a tab-delimited file with the reduced/projected coordinates.

After pulling the Docker image (see "packages" under this repo), the PCA analysis can be run as follows:

```
docker run -v $PWD:/work ghcr.io/web-mev/pca:<tag> \
    -i <path to matrix> \
    [-s <comma-delimited column names>]
```
where the required `-i` argument gives the path to the matrix you wish to perform PCA upon. Note that we expect that the matrix is arranged with observations in the columns
and features in the rows, which might be the transpose of how scipy or other machine learning toolkits handle PCA. In the genomics context 
(e.g. a RNA-seq experiment), 
the canonical orientation has samples in columns and genes in rows. Thus, observations<==>samples and features<==>genes in our treatment.

The optional `-s` flag is a comma-delimited string of the sample/column names you wish to use in the PCA. That is, it will subset the matrix to only
those samples. Without this flag, all columns/samples will be considered. An example is `-s sampleA,sampleB,sampleC`

Note that the `-v` flag provided to the Docker `run` command is used to mount the current directory in the Docker container. 
This allows the container to read/open your input matrix and also write results to that same directory.

Thus, if you have a file `matrix.tsv` in your current directory, the command would look like:
```
docker run -v $PWD:/work ghcr.io/web-mev/pca:<tag> \
    -i /work/matrix.tsv
```
The output file (`pca_output.tsv`) will be written to `/work/pca_output.tsv` *inside* the container, which will be your current working directory
on the host machine.
