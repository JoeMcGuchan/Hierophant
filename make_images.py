import sys
import csv

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

cardSideMargins = 18
titleThickness = 24
bottomThickness = 48

smallFontSize = 16
mediumFontSize = 12
largeFontSize = 24

filename = 'Screenshot.jpg'
app = QApplication(sys.argv)

fontId = QFontDatabase.addApplicationFont("fonts/Austie Bost Roman Holiday Sketch.ttf");
fontFamily = QFontDatabase.applicationFontFamilies(fontId)[0];

fontSmall = QFont(fontFamily, smallFontSize)
fontMedium = QFont(fontFamily, mediumFontSize)
fontLarge = QFont(fontFamily, largeFontSize)

player_card_csv = "card_csvs/player_cards.csv"	
gm_card_csv = "card_csvs/gm_cards.csv"	

class Card:
	background = ""
	saveLocation = ""
	title = ""
	description = ""
	difficulty = ""
	extra = ""
	lethal = False

	def hasTopLine(self):
		return bool(self.title.strip())

	def hasBottomLine(self):
		return bool(self.difficulty.strip()) or bool(self.extra.strip()) or self.lethal 

	def hasMiddleLine(self):
		return bool(self.description.strip())

	def draw(self, app):
		backgroundPixmap = QPixmap()
		backgroundPixmap.load(self.background)

		wholeCard = QLabel()
		wholeCard.setPixmap(backgroundPixmap)
		wholeCard.resize(360, 661)
		wholeCard.setScaledContents(True)
		wholeCard.setLayout(QGridLayout())
		wholeCard.layout().setContentsMargins(cardSideMargins,cardSideMargins,cardSideMargins,cardSideMargins)

		titleLabel = QLabel()
		titleLabel.setText(self.title)
		titleLabel.setFont(fontLarge)

		descriptionLabel = QLabel()
		descriptionLabel.setText(self.description)
		descriptionLabel.setFont(fontMedium)
		descriptionLabel.setAlignment(Qt.AlignHCenter)
		descriptionLabel.setWordWrap(True)

		difficultyLabel = QLabel()
		difficultyLabel.setText(self.difficulty)
		difficultyLabel.setFont(fontLarge)

		extraLabel = QLabel()
		extraLabel.setText(self.extra)
		extraLabel.setFont(fontMedium)

		skullPixmap = QPixmap()
		skullPixmap.load("card_templates/skull_icon.png")

		skullLabel = QLabel()
		skullLabel.setVisible(self.lethal)
		skullLabel.setPixmap(skullPixmap)
		skullLabel.resize(52, 52)
		skullLabel.setScaledContents(True)

		if self.hasTopLine():
			wholeCard.layout().setRowMinimumHeight(0, titleThickness)

		if self.hasBottomLine():
			wholeCard.layout().setRowMinimumHeight(3, titleThickness)

			if self.hasMiddleLine():
				wholeCard.layout().setRowMinimumHeight(2, bottomThickness - titleThickness)
		else:
			if self.hasMiddleLine():
				wholeCard.layout().setRowMinimumHeight(2, bottomThickness)

		wholeCard.layout().setRowStretch(1,1)
		wholeCard.layout().setColumnStretch(1,1)

		wholeCard.layout().addWidget(titleLabel, 0, 0, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)
		wholeCard.layout().addWidget(descriptionLabel, 2, 0, 1, 3, Qt.AlignCenter | Qt.AlignVCenter)
		wholeCard.layout().addWidget(difficultyLabel, 3, 0, 1, 1, Qt.AlignLeft | Qt.AlignBottom)
		wholeCard.layout().addWidget(extraLabel, 3, 1, 1, 1, Qt.AlignRight | Qt.AlignBottom)
		wholeCard.layout().addWidget(skullLabel, 3, 2, 1, 1, Qt.AlignLeft | Qt.AlignBottom)

		wholeCard.setFrameShape(QFrame.Box)
		titleLabel.setFrameShape(QFrame.Box)
		descriptionLabel.setFrameShape(QFrame.Box)
		difficultyLabel.setFrameShape(QFrame.Box)
		extraLabel.setFrameShape(QFrame.Box)
		skullLabel.setFrameShape(QFrame.Box)

		wholeCard.show()

		app.exec_()
		wholeCard.grab().save(self.saveLocation + "/" + self.title + ".png")

def makePlayerCard(cardInfo):
	card = Card()
	return card

def makeGateCard(cardInfo, app):
	card = Card()

	card.background = "card_templates/gm_cards/the_gate.png"
	card.saveLocation = "produced_cards/gm_cards"

	card.draw(app)

def makeOpenCard(cardInfo, app):
	card = Card()

	card.background = "card_templates/gm_cards/open.png"
	card.saveLocation = "produced_cards/gm_cards/open"
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]
	card.difficulty = cardInfo["DIFFICULTY"]

	extra = cardInfo["REST/DAMAGE AMOUNT"]
	if extra.strip():
		card.extra = "restore "+extra

	card.draw(app)

def makeThreatCard(cardInfo, app):
	card = Card()

	card.background = "card_templates/gm_cards/threat.png"
	card.saveLocation = "produced_cards/gm_cards/threat"
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]
	card.difficulty = cardInfo["DIFFICULTY"]

	damage = cardInfo["REST/DAMAGE AMOUNT"]

	if (cardInfo["TO ALL?"] == "TRUE"):
		card.extra = damage + " damage to all"
	else:
		card.extra = damage + " damage"

	card.lethal = (cardInfo["LETHAL"] == "TRUE")

	card.draw(app)

def makeGMCard(cardInfo, app):
	typeText = cardInfo["TYPE"]

	if (typeText == "THE GATE"):
		makeGateCard(cardInfo, app)
		return

	if (typeText == "OPEN"):
		makeOpenCard(cardInfo, app)
		return

	if (typeText == "THREAT"):
		makeThreatCard(cardInfo, app)
		return

with open(gm_card_csv, newline='') as csvItems:
    itemsReader = csv.DictReader(csvItems, delimiter=',', quotechar='"')
    for card in itemsReader:
        makeGMCard(card, app)

with open(player_card_csv, newline='') as csvItems:
    itemsReader = csv.DictReader(csvItems, delimiter=',', quotechar='"')
    for card in itemsReader:
        makePlayerCard(card).draw(app)