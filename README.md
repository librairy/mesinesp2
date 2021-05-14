# Supervised Graph-based Topic Model for Medical Semantic Indexing in Spanish

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![GitHub Issues](https://img.shields.io/github/issues/librairy/mesinesp2.svg)](https://github.com/librairy/mesinesp2/issues)
[![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Data-DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4701973.svg)](https://doi.org/10.5281/zenodo.4701973)



## Task
The [MESINESP2](https://temu.bsc.es/mesinesp2/) task of the [9th BioASQ Workshop](http://www.bioasq.org/workshop2021) aims to create an automatic semantic indexing system for Spanish medical documents based on structured vocabularies. In particular, texts have to be annotated with [DeCS headings](https://temu.bsc.es/mesinesp2/decs-headings/). These *health sciences descriptors* are a trilingual and structured vocabulary created by BIREME to serve as a unique language in indexing articles from scientific journals, books, conference proceedings, technical reports, and other types of materials, as well as for searching and retrieving subjects from scientific literature from information sources available on the Virtual Health Library (VHL) such as LILACS, MEDLINE, among others. 

Three types of [documents](https://temu.bsc.es/mesinesp2/datasets/) are proposed for the task: [scientific literature](https://temu.bsc.es/mesinesp2/sub-track-1-scientific-literature/), [clinical trails](https://temu.bsc.es/mesinesp2/sub-track-2-clinical-trials/) and [patents](https://temu.bsc.es/mesinesp2/sub-track-3-patents/). They are **not long texts** and usually have assigned **several categories**. On average, scientific articles contain 1,332 characters and 10 categories, clinical trails contain 7,283 characters and 15 categories, and patents contain 1,640 characters and 10 categories.  

## Proposal

A probabilistic topic-based representation of DeCS categories created from previously annotated texts. Each category is described by a density distribution over the vocabulary used in the training texts. The generated topic model allows inferring the presence of DeCS categories in texts not used during training. 

## Challenges
The characteristics of the documents proposed for the taks and the assumptions of the probabilistic topic models lead to several challenges: (1) Since texts are not long, word frequency may not be adequate to measure relevance, and topic models are based on bags of words (i.e., word order does not matter, but word repetition does); (2) short text-oriented topic models assume the presence of only one topic in the text, however the documents proposed for the task may have more than one category; (3) the topic creation must be supervised to force each topic to map to a DeCS category since categories must match the DeCS headers;  and finally (4) topic inference should consider only the most relevant ones, i.e. one or several, since each text may have several categories.

## Corpora
A [Solr index](http://librairy.linkeddata.es/data/#/mesinesp/core-overview) has been created to process and annotate the texts proposed for the task. The structure of the documents is as follows:
* **id**: unique identifier 
* **title_s**: document name (*string*)
* **abstract_t**: text paragraph (*terms*)
* **journal_s**: publication journal (*string*)
* **size_i**: number of characters (*integer*)
* **year_i**: publication date (*integer*)
* **db_s**: document database (*string*)
* **codes**: list of DeCS categories (*list-of-string*)
* **scope_s**: training, development or test (*string*)
* **diseases**: list of diseases retrieved from the abstract (*list-of-string*)
* **medications**: list of medications retrieved from the abstract (*list-of-string*)
* **procedures**: list of procedures retrieved from the abstract (*list-of-string*)
* **symptoms**: list of symptoms retrieved from the abstract (*list-of-string*)
* **sentences**: list of list of words after pre-processing the abstract (*list-of-string*)
* **tokens_t_**: base text for creating word-bags (*terms*)

This is an example of document:

````json
{
        "id":"ibc-ET1-3794",
        "title_s":"Caso clínico: Manejo clínico de la hiperprolactinemia secundaria al tratamiento de un episodio maníaco con características psicóticas y mixtas en una paciente con un inicio posparto de trastorno bipolar tipo I",
        "abstract_t":"Se presenta el caso de una paciente que ingresa por un primer episodio maníaco con sintomatología psicótica y mixta. El tratamiento inicial instaurado permitió un control parcial de los síntomas agudos y ocasionó una intensa elevación de los niveles séricos de prolactina. Ante esta situación, se planteó una solución terapéutica basada en la evidencia",
        "journal_s":"Psiquiatr. biol. (Internet)",
        "size_i":352,
        "year_i":2015,
        "db_s":"IBECS",
        "codes":["D006966",
          "D001714",
          "D005260",
          "D000068105",
          "D011388",
          "D006801",
          "D011570",
          "D011618",
          "D049590"],
        "scope_s":"Development",
        "diseases":["maníaco_con_sintomatología_psicótica"],
        "medications":["prolactina"],
        "sentences":["presentar",
          "casar",
          "paciente",
          "...."],
        "tokens_t":" ingresar ingresar ..",
        "_version_":1699080371235192832}
````
## Algorithms
*more details coming soon*. 


## Results

Our models are publicly available as Web REST services through [Docker](https://www.docker.com/) images. The service can be started by `docker run -p 8080:7777 <model-as-a-service name>` and a Swagger-based interface is available at [http://localhost:8080](http://localhost:8080).

| Algorithm | Reference           | Bag-of-Words                     |   Model-as-a-Service               | Precision | Recall | F-Measure |
| --------- | :------------------:| :-------------------------------:|:------------------------------------:|:---------:|:------:|:---------:|
| LabeledLDA| Ramage et. al (2009)| Frequency                        |  librairy/llda-mesinesp:latest\*     |   TBD     |  TBD   |    TBD    |
| TR-LLDA   | novel               | TextRank + lineal normalization  |  librairy/tr-llda-mesinesp:latest\*  |   TBD     |  TBD   |    TBD    |
| TR?-LLDA  |  novel              | TextRank + ? normalization       |  librairy/tr?-llda-mesinesp:latest\* |   TBD     |  TBD   |    TBD    |
| R-LLDA    |  novel              | Rake + lineal normalization      |  librairy/r-llda-mesinesp:latest\*   |   TBD     |  TBD   |    TBD    |
| R?-LLDA   |  novel              | Rake + ? normalization           |  librairy/r?-llda-mesinesp:latest\*  |   TBD     |  TBD   |    TBD    |


\* *not available yet*