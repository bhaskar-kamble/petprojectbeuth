# Animating the normal modes of a coupled oscillator system



As part of the Advanced Software Engineering course at the Beuth Hochschule fuer Technik, Berlin, students are required to write a project of their choice and apply the concepts of advanced software engineering taught in this course. As part of my submission, I wrote a Python program to generate animations of a coupled system of oscillators (identical masses coupled with identical springs) with either fixed or open boundary conditions.

**All details relating to the specific tasks of the project and my solutions can be found in the repo [Wiki](https://github.com/bhaskar-kamble/petprojectbeuth/wiki).**


Below is an example of the animations produced. Both show longitudinal oscillations (as opposed to transverse oscillations), but whereas the one on the left shows fixed boundary conditions (the masses at the ends being fixed to rigid walls), the second one shows open boundary conditions (the masses at the ends being free, or "open").

<img src="./FixedBCyoutube.gif" width="300">  <img src="./OpenBC.gif" width="300">

**How to use the code**

The main code is in the parent folder (`NormalModesAnimator.py`). For running the code download it into a folder and run it (for default parameters) by opening a terminal and typing `python3 NormalModesAnimator.py` and it will produce the animation.

The default parameters are:

1. `numberMasses = 6`. This is the number of masses in the spring-mass system and is an integer.
2. `relAmp = [1.0 , 0.8 , 0.6 , 0.4 , 0.4 , 0.3]`. These are the relative amplitudes of each of the masses and is a list. The length must be equal to `numberMasses`. Otherwise a runtime error is thrown.
3. `howLong = 4.0*np.pi*5.0` This is the duration for which you want the animation to run and is a float.
4. `howMany = 4000` This is the number of snapshots in the interval `howLong` and is an integer.

For non-default parameters you can do the following:

1. open a python terminal and import the code with `import NormalModesAnimator`.
2. if you want to animate a system with fixed boundary conditions, create an object of class `longFixed` with `osc1 = NormalModesAnimator.longFixed(numberMasses,relAmp,howLong,howMany)` with parameters of your choice and create the animation with `osc1.plotAnimationLF()`.
3. if you want to animate a system with open boundary conditions, create an object of class `longOpen` with `osc2 = NormalModesAnimator.longOpen(numberMasses,relAmp,howLong,howMany)` with parameters of your choice and create the animation with `osc1.plotAnimationLO()`.




