import sys
import csv

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

scaleFactor = 0.5
cardHeight = int(1417 * scaleFactor)
cardWidth = int(827 * scaleFactor)

cardSideMargins = int(74 * scaleFactor)
lowerBorderInlay = int(20 * scaleFactor)
titleThickness = int(84 * scaleFactor)
bottomThickness = int(265 * scaleFactor)

smallFontSize = int(32 * scaleFactor)
mediumFontSize = int(36 * scaleFactor)
largeFontSize = int(48 * scaleFactor)

filename = 'Screenshot.jpg'
app = QApplication(sys.argv)

fontId = QFontDatabase.addApplicationFont("../fonts/Austie Bost Roman Holiday Sketch.ttf");
fontFamily = QFontDatabase.applicationFontFamilies(fontId)[0];

fontSmall = QFont(fontFamily, smallFontSize)
fontMedium = QFont(fontFamily, mediumFontSize)
fontLarge = QFont(fontFamily, largeFontSize)

player_card_csv = "../card_csvs/player_cards.csv"	
gm_card_csv = "../card_csvs/gm_cards.csv"	

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
		wholeCard.resize(cardWidth, cardHeight)
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
		skullPixmap.load("../card_templates/skull_icon.png")

		skullLabel = QLabel()
		skullLabel.setVisible(self.lethal)
		skullLabel.setPixmap(skullPixmap.scaled(titleThickness,titleThickness))
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

		wholeCard.layout().addWidget(titleLabel, 0, 0, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)
		wholeCard.layout().addWidget(descriptionLabel, 2, 0, 1, 5, Qt.AlignCenter | Qt.AlignVCenter)
		wholeCard.layout().addWidget(difficultyLabel, 3, 1, 1, 1, Qt.AlignLeft | Qt.AlignBottom)
		wholeCard.layout().addWidget(extraLabel, 3, 2, 1, 1, Qt.AlignRight | Qt.AlignBottom)
		wholeCard.layout().addWidget(skullLabel, 3, 3, 1, 1, Qt.AlignLeft | Qt.AlignVCenter)

		wholeCard.layout().setColumnMinimumWidth(0, lowerBorderInlay)
		wholeCard.layout().setColumnMinimumWidth(4, lowerBorderInlay)

		wholeCard.show()

		app.exec_()
		wholeCard.grab().save(self.saveLocation + "/" + self.title + ".png")

def makeGateCard(cardInfo, app):
	card = Card()

	card.background = "../card_templates/gm_cards/the_gate.png"
	card.saveLocation = "../produced_cards/gm_cards"

	card.draw(app)

def makeOpenCard(cardInfo, app):
	card = Card()

	card.background = "../card_templates/gm_cards/open.png"
	card.saveLocation = "../produced_cards/gm_cards/open"
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]
	card.difficulty = cardInfo["DIFFICULTY"]

	extra = cardInfo["REST/DAMAGE AMOUNT"]
	if extra.strip():
		card.extra = "restore "+extra

	card.draw(app)

def makeThreatCard(cardInfo, app):
	card = Card()

	card.background = "../card_templates/gm_cards/threat.png"
	card.saveLocation = "../produced_cards/gm_cards/threat"
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

def makeTowerCard(cardInfo, app):
	card = Card()

	card.background = "../card_templates/player_cards/the_tower.png"
	card.saveLocation = "../produced_cards/player_cards"

	card.draw(app)

def makeTraitCard(cardInfo, app):
	card = Card()

	subType = cardInfo["SUBTYPE"].lower()

	card.background = "../card_templates/player_cards/traits/"+subType+".png"
	card.saveLocation = "../produced_cards/player_cards/traits/"+ subType
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]

	card.draw(app)

def makeAdvancedTraitCard(cardInfo, app):
	card = Card()

	subType = cardInfo["SUBTYPE"].lower()

	card.background = "../card_templates/player_cards/skills/"+subType+".png"
	card.saveLocation = "../produced_cards/player_cards/skills/"+ subType
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]

	card.draw(app)

def makeWoundCard(cardInfo, app):
	card = Card()

	subType = cardInfo["SUBTYPE"].lower()

	card.background = "../card_templates/player_cards/minor_wounds/"+subType+".png"
	card.saveLocation = "../produced_cards/player_cards/"+subType+"/minor_wounds"
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]

	card.draw(app)

def makeMajorWoundCard(cardInfo, app):
	card = Card()

	subType = cardInfo["SUBTYPE"].lower()

	card.background = "../card_templates/player_cards/minor_wounds/"+subType+".png"
	card.saveLocation = "../produced_cards/player_cards/"+subType+"/major_wounds"
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]

	card.draw(app)

def makeBlessingCard(cardInfo, app):
	card = Card()

	subType = cardInfo["SUBTYPE"].lower()

	card.background = "../card_templates/player_cards/skills/"+subType+".png"
	card.saveLocation = "../produced_cards/player_cards/skills"
	card.title = cardInfo["NAME"]
	card.description = cardInfo["TEXT"]

	card.draw(app)

def makePlayerCard(cardInfo, app):
	typeText = cardInfo["TYPE"]

	if (typeText == "THE TOWER"):
		makeTowerCard(cardInfo, app)
		return

	if (typeText == "TRAIT"):
		makeTraitCard(cardInfo, app)
		return

	if (typeText == "ADVANCED TRAIT"):
		makeAdvancedTraitCard(cardInfo, app)
		return

	if (typeText == "WOUND"):
		makeWoundCard(cardInfo, app)
		return

	if (typeText == "MAJOR WOUND"):
		makeMajorWoundCard(cardInfo, app)
		return	

	if (typeText == "BLESSING"):
		makeBlessingCard(cardInfo, app)
		return	

with open(gm_card_csv, newline='') as csvItems:
    itemsReader = csv.DictReader(csvItems, delimiter=',', quotechar='"')
    for card in itemsReader:
        makeGMCard(card, app)

with open(player_card_csv, newline='') as csvItems:
    itemsReader = csv.DictReader(csvItems, delimiter=',', quotechar='"')
    for card in itemsReader:
        makePlayerCard(card, app)