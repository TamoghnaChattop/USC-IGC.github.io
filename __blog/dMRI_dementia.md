Title: Multimodal Parkinson's Diseases Detection
summary: Fusing anatomical and diffusion MRIs for detecting Parkinson’s disease
js:
css:
exts:
    -markdown.extensions.meta
    -markdown.extensions.headerid
    -markdown.extensions.tables
    markdown.extensions.toc
    -markdown.extensions.fenced_code
    -markdown.extensions.codehilite

# Fusing anatomical and diffusion MRIs for detecting Parkinson’s disease

## Introduction
Deep learning models based on convolutional neural networks (CNNs) effectively extract meaningful features from raw MRI scans. However, these models have predominantly been tested using T1-weighted brain MRI data. This study investigates the added value of diffusion-weighted MRI (dMRI), which captures microstructural tissue properties, as an additional input for CNN-based models; we illustrate their use there for a Parkinson's Disease (PD) classification task.


## Model
We propose a Y-shaped architecture for dual-modality training that uses separate 3D CNNs to distill predictive features from the anatomical MRI and diffusion MRIs. These are then merged/concatenated for PD classification.

<figure class="image">
  <img src="../blogimages/fusion_gif.gif" alt="">
  <figcaption></figcaption>
</figure>


## Results
Our evaluation involves data from three cohorts: Chang Gung University, the University of Pennsylvania (UPenn), and the Parkinson's Progression Markers Initiative (PPMI). In our dual-modality experiments, we found that combining T1-weighted images (T1w) with diffusion-weighted imaging mean diffusivity (DWI-MD) and axial diffusivity (DWI-AD) yielded some promising results compared to the other combinations tested. In most cases, using a combination of T1w and dMRI improved the balanced accuracy compared to using T1w alone. However, these models should benefit from more training data, considering the large dimension of the input data and the limited amount of training samples available. Surprisingly, despite the expectation that the fused model, which incorporates more information, would outperform the models using only DWIs, we found that the fused model's balanced accuracy was still lower than the case where DWIs were the sole input. We may require a larger dataset to leverage the fused model's advantages effectively.


We also discovered an intriguing finding regarding classifying the Parkinson's Progression Markers Initiative (PPMI) dataset. PPMI proved more challenging to classify than the other two datasets we examined. One possible explanation for this discrepancy is the mean Hoehn and Yahr (H&Y) stage distribution among the patients in each dataset. Specifically, the average H&Y stage follows the order: UPenn (2.64) > Taiwan (2.24) > PPMI (1.59), indicating that patients in the PPMI dataset may generally exhibit milder brain abnormalities compared to those in the other datasets.


These findings underscore the potential of combining T1-weighted and diffusion-weighted imaging modalities for improved accuracy in Parkinson's disease classification. However, further research with larger datasets is necessary to fully harness the benefits of these combined models and enhance our understanding of the unique characteristics of different datasets.