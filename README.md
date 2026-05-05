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
- Dissertation report.pdf &rarr; contains the written up explanation of every step taken and the purpose of this work.
- Segmentation results.pdf &rarr; is the appendix that goes together with the report and contains all the segmentation results achieved in this work (should be downloaded to see all the images).
- Sobel_Plus_Watershed.mlx &rarr; main file of the repository, which contains the MATLAB code of the pipeline.

## MATLAB toolboxes needed:
- Image Processing Toolbox (v25.2)
- Statistics and Machine Learning Toolbox (v25.2) (only for Segm_Metrics)

## To run the pipeline
This code was written in MATLAB R2025b and was not tested in other MATLAB versions. Install Image Processing Toolbox (v25.2). Download Sobel_Plus_Watershed.mlx file and run it. If you would like to use the GUI version of the pipeline, select the appropriate choice of a segmentation algorithm in [this MATLAB app ('Adding-S+W branch' unless it is already merged with the main brach)](https://github.com/USonixGroup/Multires-ML-Microscopy.git).  

### User inputs:
There are 6 parameters that can be configured before the code is run. They have to be manually changed in the code. These were set to the best values possible that worked best among all the images tested, and changing these did not produce a significant change in the quality of segmentation. The 3 additional parameters which influence segmentation the most have to be specified by a user before each run after you hit "Run" button. To choose the best combination of user input parameter follow these steps:
1. **Polarity:** easiest to decide on. There are only 2 options: brighter or darker. If the cell is brighter than the background indicate it with 'b', if not - hit 'd'. Usually, there is a very noticeable difference between segmentation results if the polarity chosen is wrong.

2. **Disk Size:** 4 options - 1, 2, 3 and 4. There was a correlation noticed between a single cell area in pixels and Disk Size which works best. This correlation is explained in the image below. Use it as a guide to decide on Disk Size.
<img width="2471" height="956" alt="Circle sizes and DiskSize" src="https://github.com/user-attachments/assets/f17d9ae1-c4d2-4be9-a1d2-203abb94e177" />

3. **Sigma:** indicates amount of Gaussian blur you want to apply to an image. The advice is to start at 0.1 (smallest value) and go up 1, 2, 3, 4. When you notice that the result becomes particularly better between sigma=3 and sigma=4 for example, go to 3.5 and continue choosing value of sigma from there. Having a value of sigma accurate to 1 decimal place is enough and being more accurate with the value will not generate change in segmentation quality.

If the image is particularly noisy, you might have to increase sigma all the way up to around 8 or 9, OR you can increase the Disk Size by 1 step up, but then Sigma value has be picked lower for optimal results. Read the dissertation report with examples of images analysed and best user inputs identified. 
