## <div align="center">Documentation</div>

What I've worked on while making this project from [here]() <br>

## <div align="center">Quick Start Examples</div>

<details open>
<summary>Install</summary>

Clone repo and run the following commands

```bash
git clone https://github.com/ultralytics/yolov5  # clone
cd Playing-Cards-Detection-with-Tarneeb.
pip install -r requirements.txt  # install
```

Then open [detect_trnb.py](https://github.com/baselhusam/Playing-Cards-Detection-with-Tarneeb./blob/master/detect_trnb.py) and open the terminal and run the following command
```bash
python detect_trnb.py --weights best_weights.pt --img 640 --conf 0.75 --source 0 # Terminal
```

Or you can open [detect_trnb.ipynb](https://github.com/baselhusam/Playing-Cards-Detection-with-Tarneeb./blob/master/detect.ipynb) and the the following cell
```python
!python detect_trnb.py --weights best_weights.pt --img 640 --conf 0.25 --source 0 #Tune the confidance hypterparameter
```

</details>
<br>

## <div align="center"> Information about this project </div> <hr>

This Project has 2 main features:
   1. Playing Card Detection  --> You can try this by using the [detect.py](https://github.com/baselhusam/Playing-Cards-Detection-with-Tarneeb./blob/master/detect.py)
   2. Tarneeb Game --> You can try it by using the [detect_trnb.py](https://github.com/baselhusam/Playing-Cards-Detection-with-Tarneeb./blob/master/detect_trnb.py) or [detect.ipynb](https://github.com/baselhusam/Playing-Cards-Detection-with-Tarneeb./blob/master/detect.ipynb)


This project is a Computer Vision Project, it is aim to detect the playing cards and do some application with the detection (like the traneeb game). <br>
The model for this project has been trained using YOLOv5 on 25K of image labeled data from the playing cards. <br>

## <div>  Phase 1: Playing Card Detection </div> <hr>

The Output of this phase by using the [detect.py](https://github.com/baselhusam/Playing-Cards-Detection-with-Tarneeb./blob/master/detect.py) is the number of cards, and the card for each type in the deck, at the top left of the screen/image/video/etc. <br>

### For example:

No. Cards: 7 <br>

Club: KC, 2C <br>
Spade: 6S, JS, AS <br>
Heart: QH, 4H <br>
Diamond: _ <br>


## <div> Phase 2: Tarneeb Game </div> <hr>

This project helps you to detect the winner for one round from the tarneeb game. <br>
you can try the game locally on your device by using the [detect_trnb.py]() in the detection command.

The Rules for the game: <br>
Every one will through a card the program wiill determine the winner. <br>
this project is programmed that the model should see the card for at least 2 seconds. if didn't, then it will not count this card ( maybe the player changed his mind the take the card back). <br>

At the top left of the screen you wil see the winner for evey step (every new card came to the model) and you will see each player whats his card.


