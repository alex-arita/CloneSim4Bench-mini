# SIF Images Required

As noted in the [Getting Started Guide](../docs/Getting_Started.md), **CloneSim4Bench** requires both **SomatoSim** and **GATK 4.5.0.0** to function. This design ensures seamless integration and avoids installation or dependency issues that were previously reported.

## Prerequisites
To obtain the required images, **Singularity** must be installed. This can be done in two ways:

### Option 1: HPC Module Installation
If you are using an HPC cluster, check if Singularity is available as a module and request assistance from your system administrator to install or load it.

### Option 2: Conda Environment Installation
Alternatively, you can install Singularity in a Conda environment using the following steps:

```bash
conda create -n singularity
conda activate singularity
conda install -c conda-forge singularity
```

## Downloading the Images
Once Singularity is installed, you can download the required SIF files using the commands below. Ensure that the downloaded SIF files are stored in CloneSim4Bench/tools.

### GATK 4.5.0.0
```bash
singularity pull docker://broadinstitute/gatk:4.5.0.0 gatk_4.5.0.0.sif
```

### SomatoSim
```bash
singularity pull docker://marwanhawari/somatosim somatosim_latest.sif
```