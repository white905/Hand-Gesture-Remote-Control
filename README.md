# Hand-Gesture-Remote-Control
This repository contains the source code, trained model, and project report for a hand gesture recognition system developed for the 56th Taipei City Elementary and Secondary School Science Fair. The system utilizes Python, MediaPipe, and a Deep Neural Network (DNN) to recognize distinct hand gestures and remotely control Android devices via Android Debug Bridge (ADB).

## Table of Contents
* [Abstract](#abstract)
* [Motivation](#motivation)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Setup and Installation](#setup-and-installation)
* [Usage](#usage)
* [Model Details and Results](#model-details-and-results)
* [Project Report](#project-report)
* [Future Work](#future-work)

## Abstract
This project addresses the challenge of operating mobile devices in situations where direct interaction is inconvenient or unsafe. We developed a system that uses MediaPipe for hand landmark detection, a custom-collected dataset for training a Deep Neural Network, and Android Debug Bridge (ADB) for command execution. This allows users to control Android devices remotely using hand gestures, offering a portable and cost-effective solution potentially deployable on a Raspberry Pi.

## Motivation
The primary motivation for this project was to develop a safer and more cost-effective method for interacting with mobile devices, particularly in scenarios like driving. Existing solutions like voice control can be unreliable in noisy environments, and specialized hardware like sensor gloves are often expensive and cumbersome. This project aimed to provide a flexible, vision-based alternative.

## Features
- Real-time hand gesture recognition using a standard webcam
- Remote control of Android devices, including swipe gestures, application launching, and text input.
- Supports recognition of **37 distinct hand gestures** (26 English alphabet characters, 10 digits, and 1 mode-switching gesture).
- Utilizes two separate Deep Neural Network models, one for English/tool commands and one for numeric input, selected based on the current operation mode.
- Designed with portability in mind, with potential for deployment on a Raspberry Pi.

## Tech Stack
- **Programming Language:** Python 3.10.7
- **Core Libraries (approximate versions used):**
    - OpenCV 4.6.0
    - MediaPipe 0.8.11
    - TensorFlow 2.9.2 (with Keras integrated)
    - NumPy 1.21.0
    - ppadb 0.3.0
- **Device Interaction:** Android Debug Bridge (ADB) 1.0.41
- **Development Environment:** Google Colab (for model training), VS Code (for development)

## Project Structure
An overview of the key directories and files:
Hand-Gesture-Remote-Control/
- .gitignore
- README.md
- report/
  - 利用手部辨識模型實現遠端遙控.pdf
- Model/
  - 0320_2+9+12+13+生物+物理-english_lr=0.5-2-100-40.h5
  - 0320_2+9+12+13+生物+物理-number_lr=0.3-2-100-40.h5
- Development Scripts/
  - 手勢收集程式.py
  - 歷代版本紀錄.py
  - 正式訓練_model.py
  - 訓練資料結合.py
- Python Control Android/
  - hg_function.py
  - hg_global.py
  - hg_main.py

## Setup and Installation
1.  **Download Necessary Files:**
    - From this GitHub repository, download the following files and place them together in a single project directory on your computer:
        - The entire `Python Control Android` folder (which includes `hg_function.py`, `hg_global.py`, `hg_main.py`).
        - The two model files from the `Model` folder:
            - `0320_2+9+12+13+生物+物理-english_lr=0.5-2-100-40.h5`
            - `0320_2+9+12+13+生物+物理-number_lr=0.3-2-100-40.h5`
    - **Notice:** The two `.h5` model files must be in the same folder as the other three files.

2.  **Python Environment:**
    - It is recommended to use Python version 3.10.7 (closest to the original development).

3.  **Install Dependencies:**
    You'll need to install the following libraries. It's best to try and install versions close to those mentioned in the "Tech Stack" section. You may need to install them one by one:
    ```bash
    pip install tensorflow==2.9.2
    pip install mediapipe==0.8.11
    pip install opencv-python==4.6.0.66
    pip install numpy==1.21.0
    pip install ppadb==0.3.0
    ```

4.  **Android Device Setup:**
    - Enable Developer Options and USB Debugging on your Android device.
    - Ensure your system can recognize the Android device via ADB (e.g., by running `adb devices` in your terminal).
    - For initial ADB setup guidance, refer to the official Android documentation or the project report ([利用手部辨識模型實現遠端遙控.pdf](./report/利用手部辨識模型實現遠端遙控.pdf)).

## Usage
1.  Ensure your Android device is connected to your computer via USB or via Wi-Fi ADB.
2.  Navigate to the `Python Control Android` directory in your terminal.
3.  Run the main script:
    ```bash
    python hg_main.py
    ```
4.  The application will start capturing video from your webcam. Perform one of the 37 pre-defined hand gestures. The system switches between 'tool/English mode' and 'number mode' using a specific gesture.
    - In 'English mode', gestures correspond to letters a-z.
    - In 'number mode', gestures correspond to digits 0-9.
    - In 'tool mode', gestures correspond to various tool commands.
    The specific mapping can be understood by examining the `tool_cmd`, `english_cmd`, and `number_cmd` functions within `hg_function.py`.

## Model Details and Results
- **Dataset:**
    - A custom dataset was collected for training, eventually expanded to approximately **222,000** hand gesture samples across **37** distinct classes (26 English alphabet/tool triggers, 10 digits, 1 mode switch).
    - Data preprocessing involved landmark normalization (mirroring based on the first point's quadrant relative to the zeroth point, and scaling based on the distance between landmarks 0 and 5) to ensure consistency.
- **Model Architecture (DNNs):**
    - Two separate Deep Neural Network models were trained using TensorFlow/Keras: one for "English/tool" gestures and one for "number" gestures.
    - Common Architecture: Input layer (42 dimensions: 21 landmarks * 2 coordinates [x,y]), three hidden Dense layers (1000 neurons each, ReLU activation).
    - Output layer: Dense layer with softmax activation.
        - The "English/tool" model (`0320_2+9+12+13+生物+物理-english_lr=0.5-2-100-40.h5`) has an output layer corresponding to **27** classes (26 for a-z/tools + 1 for mode switch).
        - The "number" model (`0320_2+9+12+13+生物+物理-number_lr=0.3-2-100-40.h5`) has an output layer corresponding to **11** classes (10 for digits 0-9 + 1 for mode switch).
- **Training Parameters:**
    - Activation Function (Hidden Layers): ReLU
    - Optimizer: SGD (Stochastic Gradient Descent)
    - Loss Function: mse (Mean Squared Error)
    - Learning Rate: 0.5 (for alphabet), 0.3 (for digit)
    - Batch Size: 100
    - Epochs: 40
- **Performance:**
    - The model achieved an accuracy of **89.17%** in recognizing the defined gestures.
    - This performance was reached after a series of experiments including the comparison of ReLU and Sigmoid activation functions (where ReLU effectively mitigated gradient vanishing issues) and optimization of parameters such as learning rate, batch size, and epochs.

## Project Report
The detailed project report (in Chinese) from the Science Fair, covering the initial motivation, methodology, data collection, model training experiments, results, discussion, and future work is available in the `/report` directory:

- **[利用手部辨識模型實現遠端遙控.pdf](./report/利用手部辨識模型實現遠端遙控.pdf)**

## Future Work
- Expand and further diversify the dataset for all 37 gestures to enhance model accuracy and robustness across different users and environments.
- Experiment with loss functions more suited for classification tasks instead of MSE, especially for the multi-class gesture models.
- Refine the parameters (optimizer, learning rate, network architecture) for each model (English and numbers).
- Integrate the system with low-cost microcomputers like Raspberry Pi for practical, portable applications.
