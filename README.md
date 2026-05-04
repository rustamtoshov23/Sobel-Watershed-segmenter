# Sobel + Watershed segmentation pipeline
Microscopy image segmentation pipeline, which utilises a Sobel edge detector in frequency domain combined with a marker-controlled watershed transform to segment images of cells with complex morphologies. The pipeline was developed to segment any type of morphologies without the need for training. It generated very comparable results to the best segmentation pipeline available online - [Cellpose-SAM](https://github.com/MouseLand/cellpose.git) - on most images tested (can be found in Demo Images) and managed to outperform this Deep Learning + Transformer architecture on Microglial cells morphology (images M1 and M2). 
More details can be found in the dissertation report. 

## Getting help
Enquiries about the pipeline should be asked on the discussion page of the GitHub or directed to the developer (Rustam Toshov) on GitHub or via email: 88.rustam.toshov@gmail.com

## Contents of the repo:
- Demo Images folder &rarr; contains all images that were used to develop this pipeline.
- Post-Processing folder &rarr; contains small MATLAB codes (files have to be loaded in manually in the code):
  - For Cellpose folder &rarr; contains a .txt file with all packages required to create a .venv to run Cellpose segmentation pipeline AND run PNGMask_to_TIFF file, which converts Cellpose output into a .tiff mask. 
  - JSON_to_TIFF.mlx &rarr; can be used to convert a JSON segmentation mask into a more useful .tiff version. Applicable when using the GUI version of this pipeline. 
  - Image_Character.mlx &rarr; calculates the RMS contrast (the higher the value, the higher the contrast is in the image) and Laplacian Variance of an image (the higher the value, the sharper is the image). Be careful as there is no set definitive value for a high contrast or high sharpness image. These metrics are used to compare image quality within the same dataset.
  - Segm_Metrics.mlx &rarr; if a ground truth of an image is present, can be used to calculate the segmentation metrics: F1 score, Boundary F1 score, 95% Hausdorff Distance, ASSD.
  - Overlay.mlx &rarr; allows the user to overlay the segmentation mask over the original image (segmentation will be overlaid in red).
- Sobel_Plus_Watershed.mlx is the main file of the repository, which contains the MATLAB code of the pipeline.

## MATLAB toolboxes needed:
- Image Processing Toolbox (v25.2)
- Statistics and Machine Learning Toolbox (v25.2) (only for Segm_Metrics)

## To run the pipeline
This code was written in MATLAB R2025b and was not tested in other MATLAB versions. Install Image Processing Toolbox (v25.2). Download Sobel_Plus_Watershed.mlx file and run it. If you would like to use the GUI version of the pipeline, select the appropriate choice of a segmentation algorithm in [this MATLAB app (Adding-S+W branch unless it is already merged with the main brach)](https://github.com/USonixGroup/Multires-ML-Microscopy.git).  
