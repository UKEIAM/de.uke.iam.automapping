# de.uke.iam.automapping
Automatic mapping of German medical-related terms into SNOMED-CT.

## About

This repository contains the source code used in the development of our mapping approach between German medical phrases and The Observational Medical Outcomes Partnership (OMOP) concepts. 

Compared to the current standard (USAGI) our approach performs slightly better. Its main advantage lies in the automatic processing of German phrases to English OMOP concept suggestions, operating without the need for human intervention.  

-------
Currently, this repository is under development for code quality improvement.


## Getting Started
1. Download OMOP CDM files from [Athena] (https://athena.ohdsi.org/search-terms/start) with SNOMED CT vocabulary
2.  

### Prerequesties
This project utilize Docker for providing an OS-independent development and integration experience. We highly recommend using Visual Studio Code and the associated "Development Container" which allows direct access to a environment and shell with pre-installed Python, corresponding packages, and a specialized IDE experience. However, running Docker standalone is also possible by using the `Dockerfile` in the `devcontainer` folder. 

### Usage

## License 

This project is licensed under the **GPL-3.0 license**.  Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

See [LICENSE](/workspaces/de.uke.iam.automapping/LICENSE) for more information.