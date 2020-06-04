# Slicing and dicing soccer


This project presents code for detecting a wide range of complex events in soccer videos starting from positional data, which were introduced with the paper "Slicing and dicing soccer: automatic detection of complex events from spatio-temporal data".

The detector can be trained and tested on synthetic positional data extracted from the Game Football engine.  We include in this repository our implementation, which is adapted from the original implementation by Bastiaan Konings Schuiling, 
which is available here: http://properlydecent.com/data/gameplayfootball/. 

The game engine is very similar but we modified the code to extract spatio-temporal information about the players and the ball, as well as annotations from a wide range of common and not-so-common events including goals, fouls, passes, crosses, shots, saved shorts, and so forth. 

# Repository Overview
This repository contains:

1. EventDetector Atomic (with Genetic Optimizer and Evaluation code)
2. EventDetector Complex
3. Visualization System (to visualize annotated and detected events super-imposed on the video)
4. Gameplay Football 
5. Minor utilities


# Dataset
The generated dataset is available online: https://www.dropbox.com/sh/m1x3zi30q63lscq/AAA4iow3CjnR_yG3QuZiDimza
A description of the dataset, how it is structured and the content of each file is available in the file SoccER_DatasetDescription.pdf

If you make use of the dataset in your research, please cite our paper:

Morra Lia, Manigrasso Francesco, Canto Giuseppe, Gianfrate Claudio, Guarino Enrico, Lamberti Fabrizio, 
"Slicing and dicing soccer: automatic detection of complex events from spatio-temporal data", 
Proc. 17th International Conference on Image Analysis and Recognition (ICIAR 2020). 

@inproceedings{

title={ Slicing and dicing soccer: automatic detection of complex events from spatio-temporal data},

  author={Morra, Lia and Manigrasso, Francesco and Canto, Giuseppe and Gianfrate, Claudio and Guarino, Enrico and Lamberti, Fabrizio},
  
  booktitle={Proc. 17th International Conference on Image Analysis and Recognition (ICIAR 2020)},
  
  year={2020},
  
  publisher={Springer}
  
}

@article{morra2020slicing,

  title={Slicing and dicing soccer: automatic detection ofcomplex events from spatio-temporal data},
  
  author={Morra, Lia and Manigrasso, Francesco and Canto, Giuseppe and Gianfrate, Claudio and Guarino, Enrico and Lamberti, Fabrizio},
  
  journal={arXiv preprint arXiv:2004.04147},
  
  year={2020}
}



# Contributors & Maintainers
Lia Morra, Francesco Manigrasso, Giuseppe Canto, Claudio Gianfrate, Enrico Guarino, and Fabrizio Lamberti