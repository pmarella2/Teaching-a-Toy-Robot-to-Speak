# Teaching a robot to speak
## **Description:**
The goal of this project is to teach robots how to learn and speak simple words. We will use the Anki Cozmo robot as a platform. Cozmo has a Python SDK, which can be used to track the robot's internal state. The project will involve finding a way to "link" that internal state of the robot--what it perceives and experiences--to words that are uttered about the environment. For example, if the robot sees a red mug and someone says "that's a red mug" the robot should learn something about what "red" and what "mug" means.

## **Requirements for compiling and running Cozmo code:**

### **Operating System**:
Ubuntu 16.xx or higher (make sure to update your OS)
or
Windows

### **Packages**: 
Ubuntu:
1. Open a terminal (make sure you have permissions to download and install packages)
2. Go to the directory you want to download the repo into:
```bash
git clone https://github.com/pmarella2/Teaching-a-Toy-Robot-to-Speak.git CozmoCode
```
3. Run this command in terminal to download the requirements for compiling the code:
```bash
./req.sh
```

Windows:
1. Follow instructions at: http://cozmosdk.anki.com/docs/install-windows.html
2. Download freeglut.dll from: http://freeglut.sourceforge.net/ and place it in the directory with CozmoCode

### **Steps to compile and run the code on Cozmo**:
1. Connect your mobile device to your computer
2. Change into CozmoCode directory
```bash
cd CozmoCode
```
3. Open a terminal
4. In terminal, run this command to compile and run a program on Cozmo
```bash
python3 {program.py}
```

## **Troubleshooting:**
Open an issue if there are any problems with compiling and running the code
