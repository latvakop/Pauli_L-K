#include "mainwindow.hh"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      ui_(new Ui::MainWindow),
      towers_({{"A",{}},{"B",{}},{"C",{}}}),
      numberOfDiscs_(STANDARD_NUMBER_OF_DISCS),
      animationCounter_(0),
      startingTower_(STANDARD_STARTING_TOWER),
      graphicalTowers_({}),
      timer_(new QTimer(this)),
      sec_(0),
      min_(0),
      animationTimer_(new QTimer(this)),
      previousKeyPressed_(0),
      buttons_({}),
      animationIsOn_(false),
      buttonStates_({}),
      startingTowerLabels_({})
{
    ui_->setupUi(this);

    // *** Course code
    // We need a graphics scene in which to draw the hanoi's towers
    scene_ = new QGraphicsScene(this);

    // The graphicsView object is placed on the window
    // at the following coordinates:
    int leftMargin = 10; // x coordinate
    int topMargin = 270; // y coordinate

    // The width of the graphicsView is BORDER_RIGHT added by 2,
    // since the borders take one pixel on each side
    // (1 on the left, and 1 on the right).
    // Similarly, the height of the graphicsView is BORDER_DOWN added by 2.
    ui_->graphicsView->setGeometry(leftMargin, topMargin,
                                   BORDER_RIGHT + 2, BORDER_DOWN + 2);
    ui_->graphicsView->setScene(scene_);

    // The width of the scene_ is BORDER_RIGHT decreased by 1 and
    // the height of it is BORDER_DOWN decreased by 1,
    scene_->setSceneRect(0, 0, BORDER_RIGHT - 1, BORDER_DOWN - 1);
    // Course code ends ***

    // Set window title
    MainWindow::setWindowTitle("Tower of Hanoi");

    // Give lcd numbers some nice colors :)
    ui_->lcdNUmberMin->setStyleSheet("background-color: blue");
    ui_->lcdNumberSec->setStyleSheet("background-color: blue");

    // Connect timer to the timer slot.
    connect(timer_, SIGNAL(timeout()),this, SLOT(timerSlot()));

    // The animation timer connected to the slot that does the animation.
    connect(animationTimer_, SIGNAL(timeout()),this,SLOT(animationSlot()));

    // Button for closing the game
    connect(ui_->closeGamePushButton, SIGNAL(clicked()), this, SLOT(close()));

    // add the buttons to the button vector.
    initializeButtons();

    // Start a new game to present the user with a hanoi's tower
    startNewGame(numberOfDiscs_, startingTower_);
}

MainWindow::~MainWindow()
{
    delete ui_;
}

void MainWindow::on_newGamePushButton_clicked()
{
    int number = 0;
    QString startingTower = "";
    // Check if user input is acceptable
    isStartingTowerAcceptable(startingTower);
    if (not(isNumberOfDiscsAcceptable(number)) or
        not(isStartingTowerAcceptable(startingTower))) {
        return;
    }
    // If input was acceptable, start a new game.
    startNewGame(number, startingTower);
}

// 6 very interesting functions.
void MainWindow::on_AtoBpushButton_clicked()
{
    moveDisc(USER_COMMANDS.at(0));
}

void MainWindow::on_AtoCpushButton_clicked()
{
    moveDisc(USER_COMMANDS.at(1));
}

void MainWindow::on_BtoApushButton_clicked()
{
    moveDisc(USER_COMMANDS.at(2));
}

void MainWindow::on_BtoCpushButton_clicked()
{
    moveDisc(USER_COMMANDS.at(3));
}

void MainWindow::on_CtoApushButton_clicked()
{
    moveDisc(USER_COMMANDS.at(4));
}

void MainWindow::on_CtoBpushButton_clicked()
{
    moveDisc(USER_COMMANDS.at(5));
}

void MainWindow::timerSlot() {
    // change the time and display it
    ui_->lcdNUmberMin->display(min_);
    ui_->lcdNumberSec->display(sec_);
    if (sec_ == 59) {
        ++min_;
        sec_ = 0;
    } else {
        ++sec_;
    }
}

void MainWindow::animationSlot()
{
    // Uses a simple iterative algorithm: A->B or B->A then A->C or C->A then
    // B->C or C->B and repeat until the game is solved
    // (2^(number of discs)-1 moves)
    std::vector<std::pair<QString, QString>> algorithm;
    algorithm = ANIMATION_ALGORITHM;
    QString buttonName = "";
    unsigned vectorIndex = static_cast<unsigned>(animationCounter_);
    // If the first move out of the two is legal, move the disc. We are using a
    // simple map for the buttons states since we want to keep the actual
    // buttons disabled during the animation.
    if (buttonStates_.at(algorithm.at(vectorIndex).first)) {
        buttonName = algorithm.at(vectorIndex).first;
        moveDisc({buttonName.at(0), buttonName.at(1)});
    // if the second move is legal, move the disc
    } else if (buttonStates_.at(algorithm.at(vectorIndex).second)) {
        buttonName = algorithm.at(vectorIndex).second;
        moveDisc({buttonName.at(0), buttonName.at(1)});
    } else {
        if (animationCounter_ == 2) {
            animationCounter_ = 0;
        } else {
            ++animationCounter_;
        }
        animationSlot();
    }
    // Change the counter value so the next time this slot is called the next
    // move of the iterative algorithm will be executed.
    if (animationCounter_ == 2) {
        animationCounter_ = 0;
    } else {
        ++animationCounter_;
    }
}

void MainWindow::keyPressEvent(QKeyEvent* event) {

    for (unsigned i = 0; i < KEY_COMBINATIONS.size();++i) {
        if (previousKeyPressed_ == KEY_COMBINATIONS.at(i).first and
                event->key() == KEY_COMBINATIONS.at(i).second) {
            // If button is enabled it means that the move is legal. After
            // every move the buttons are set to the correct state so we can
            // use that information here.
            if (buttons_.at(i)->isEnabled()) {
                moveDisc(USER_COMMANDS.at(i));
                previousKeyPressed_ = 0;
                return;
            // Button is disabled so this move was against the rules.
            } else {
                previousKeyPressed_ = 0;
                return;
            }
        }
    }
    // Set the current key pressed to be the previous key.
    previousKeyPressed_ = event->key();
}

void MainWindow::on_solvePushButton_clicked()
{
    if (animationIsOn_) {
        return;
    }
    // Disable all buttons to prevent bugs.
    setAllButtonsDisabled();
    ui_->solvePushButton->setDisabled(true);
    animationIsOn_ = true;  
    // Value of the animation counter depends on the starting tower.
    animationCounter_ = ANIMATION_ALGORITHM_STARTING_POINT.at(startingTower_);
    setButtonsDisabledOrEnabled();
    // start the animation.
    animationTimer_->start(ANIMATION_TIME);
}

void MainWindow::on_stopSolvingPushButton_clicked()
{
    // Stop the animation
    animationIsOn_ = false;
    animationTimer_->stop();
    setButtonsDisabledOrEnabled();
}


bool MainWindow::isNumberOfDiscsAcceptable(int& numberOfDiscs)
{
    QString userInput = ui_->numberOfDiscsLineEdit->text();

    // If user gives no input, use a standard number for discs, which is 6.
    if (userInput.isEmpty()) {
        numberOfDiscs = STANDARD_NUMBER_OF_DISCS;
    }
    // If number is not int, show an error message
    else if (not(userInput.toInt())) {
        ui_->discsErrorLabel->setText(DISCS_ERROR_TEXT);
        return false;
    } else {
        numberOfDiscs = QStringtoInt(userInput);
    }
    // Negative number or too big of a number doesn't really make sense since it
    // doesn't fit on the game board and solving it would take thousands or
    // millions of moves. Solving a game with too many discs is only really
    // possible for computer algothithms.
    if (numberOfDiscs < MIN_NUMBER_OF_DICS or
            numberOfDiscs > MAX_NUMBER_OF_DISCS) {
        ui_->discsErrorLabel->setText(DISCS_ERROR_TEXT);
        return false;
    }
    ui_->discsErrorLabel->setText("");
    return true;
}

bool MainWindow::isStartingTowerAcceptable(QString &startingTower)
{
    QString userInput = ui_->startingTowerLineEdit->text();

    // capitalize user input so small letters can also be used.
    userInput = userInput.toUpper();
    // If the field is empty, use a standard tower which is 'A'
    if (userInput.isEmpty()) {
        startingTower = STANDARD_STARTING_TOWER;
    // User gave something else than 'A','B' or 'C'
    } else if (towers_.find(userInput) == towers_.end()) {
        ui_->towerErrorLabel->setText(TOWER_ERROR_TEXT);
        return false;
    } else {
        startingTower = userInput;
    }
    ui_->towerErrorLabel->setText("");
    return true;


}

void MainWindow::startNewGame(int numberOfDiscs, QString startingTower)
{
    // User input was acceptable so we can set the values as attributes
    startingTower_ = startingTower;
    numberOfDiscs_ = numberOfDiscs;

    initializeAttributes();
    int xCoord = TOWER_COORDS.at(startingTower);
    // Height multiplier for adding the rectangles at the right y coordinate.
    int heightMultiplier = 1;
    // The rectangles are added to the gameboard and to the data structure from
    // bottom to top, or biggest to smallest.
    for (int i = numberOfDiscs;i >= 1; --i) {
        QGraphicsRectItem* rect = scene_->addRect(
                    xCoord-(RECTANGLE_STARTING_WIDTH + STEP*i)/2,
                    BORDER_DOWN - RECTANGLE_HEIGHT* heightMultiplier,
                    RECTANGLE_STARTING_WIDTH + STEP*i,RECTANGLE_HEIGHT);
        // Setting the discs to be the right color
        rect->setBrush(TOWER_COLORS.at(startingTower));
        // Adding the towers to the data structure
        towers_.at(startingTower).push_back({i,rect});

        ++heightMultiplier;
    }
    initializeGraphicalTowers();

    changeTurn();
}

int MainWindow::QStringtoInt(QString string)
{
    // Turns QString input to int and returns it
    bool ok;
    int numberOfDiscs = string.toInt(&ok,10);
    return numberOfDiscs;
}

void MainWindow::setButtonsDisabledOrEnabled()
{
    // Going trough all the possible moves the user could input. Disabling all
    // the moves moves that would be against the game rules. The buttons and
    // all the possible user commands are in alphabetical order.
    for (unsigned i = 0;i < USER_COMMANDS.size();++i) {
        // Name of the two towers.
        QString moveFrom = USER_COMMANDS.at(i).first;
        QString moveTo = USER_COMMANDS.at(i).second;
        // data structures for the two towers.
        towerData towerToMoveFrom = towers_.at(moveFrom);
        towerData towerToMoveTo = towers_.at(moveTo);
        // Moving from non empty tower to empty tower so this is ok.
        if (towerToMoveTo.size() == 0 and towerToMoveFrom.size() != 0) {
            if (not(animationIsOn_)) {
                buttons_.at(i)->setEnabled(true);
                continue;
            }
            // If animation is going on we don't want to enable the buttons so
            // we just save the button status to a map.
            buttonStates_.at(moveFrom += moveTo) = true;
            continue;
        }
        // Can't move a disc if there is none.
        if (towerToMoveFrom.size() == 0) {
            if (not(animationIsOn_)) {
                buttons_.at(i)->setDisabled(true);
                continue;
            }
            buttonStates_.at(moveFrom += moveTo) = false;
            continue;

        }
        // Can't put a bigger disc on top of a smaller disc.
        if (towerToMoveFrom.at(towerToMoveFrom.size() - 1).first >
                towerToMoveTo.at(towerToMoveTo.size() - 1).first) {
            if (not(animationIsOn_)) {
                buttons_.at(i)->setDisabled(true);
                continue;
            }
            buttonStates_.at(moveFrom += moveTo) = false;
        } else {
            if (not(animationIsOn_)) {
                buttons_.at(i)->setEnabled(true);
                continue;
            }
            buttonStates_.at(moveFrom += moveTo) = true;
        }
    }
}

void MainWindow::moveDisc(std::pair<QString, QString> twoTowers)
{
    // Name's of the towers
    QString startTower = twoTowers.first;
    QString destinationTower = twoTowers.second;
    // Error check just in case there's an empty tower.
    if (towers_.at(startTower).size() == 0) {
        return;
    }
    // Starting and destionation tower data.
    towerData towerToMoveFrom = towers_.at(startTower);
    towerData towerToMoveTo = towers_.at(destinationTower);

    // The height of the destination tower for calculatin the new y-axis.
    int destinationTowerHeight = static_cast<int>(towerToMoveTo.size() + 1);
    // Disc size for calculating the new x-axis.
    int discSize = towerToMoveFrom.at(towerToMoveFrom.size() - 1).first;
    // x-coordinate also depends on the location of the destination tower.
    int xCoordinate = TOWER_COORDS.at(destinationTower);
    // The rectangle or disc that is going to move.
    rectangle rect = towerToMoveFrom.at(towerToMoveFrom.size() - 1);

    // Add the disc to the vector of the destination tower
    towers_.at(destinationTower).push_back(rect);
    // Remove the disc from the vector of the starting tower
    towers_.at(startTower).pop_back();
    // Change the location of the disc that moves. The calculations here are
    // a bit confusing but there's sort of an equation for it.
    // You need to know the destination tower height and the  disc size to
    // calculate both the x- and y-axis right. X-axis also depends from the
    // tower location, if the tower is on the left middle or right
    towers_.at(destinationTower).at(towers_.at(destinationTower).size() - 1).
            second->
            setRect(xCoordinate-(RECTANGLE_STARTING_WIDTH + STEP*discSize)/2,
            BORDER_DOWN - (RECTANGLE_HEIGHT*destinationTowerHeight),
            RECTANGLE_STARTING_WIDTH + STEP*discSize, RECTANGLE_HEIGHT);
    // Set the color of the disc to be the same as the tower.
    towers_.at(destinationTower).at(towers_.at(destinationTower).size() - 1).
            second->setBrush(TOWER_COLORS.at(destinationTower));

    changeTurn();
}

bool MainWindow::isGameWon()
{
    // Game is won if there is a tower that is the same size as the starting
    // tower, but on a different place than where the game started from.
    for (auto tower: towers_) {
        if (tower.first != startingTower_) {
            if (static_cast<int>(tower.second.size()) == numberOfDiscs_) {
                return true;
            }
        }
    }
    return false;
}

void MainWindow::drawTowerGraphics()
{
    // Sets the graphical towers to the right size after every turn.
    for (auto tower: towers_) {
        // Tower height depends on the size of the vector that is in the
        // datastructure.
        int height = static_cast<int>(tower.second.size());
        // Calculating the tower location with constants and the height of the
        // tower. X-coordinate depends if the tower name is A,B or C and y-
        // coordinate depends on the amount of discs in the tower currently.
        graphicalTowers_.at(tower.first)->
                setRect(TOWER_COORDS.at(tower.first) - GRAPHICAL_TOWER_WIDTH/2,
                        BORDER_DOWN - GRAPHICAL_TOWER_HEIGHT,
                        GRAPHICAL_TOWER_WIDTH,
                        GRAPHICAL_TOWER_HEIGHT - height*STEP);
    }
}

void MainWindow::endGame()
{
    // Stop the timers
    timer_->stop();
    animationTimer_->stop();
    // Ask user if they want to play again or stop playing.
    int messageBoxQuestion = 0;
    messageBoxQuestion = QMessageBox::question(nullptr, "You won the game!",
                         "Play again?",QMessageBox::Yes,QMessageBox::No);
    if (messageBoxQuestion == QMessageBox::Yes) {
        startNewGame(STANDARD_NUMBER_OF_DISCS,STANDARD_STARTING_TOWER);
    } else {
        MainWindow::close();
    }

}

void MainWindow::initializeGraphicalTowers()
{
    // Iniatialize the tower to the right coordinates with the help of the
    // coordinates vector.
    for (auto tower: TOWER_COORDS) {
        QGraphicsRectItem* rect = scene_->
                addRect(tower.second - GRAPHICAL_TOWER_WIDTH/2,
                        BORDER_DOWN - GRAPHICAL_TOWER_HEIGHT,
                        GRAPHICAL_TOWER_WIDTH, GRAPHICAL_TOWER_HEIGHT);
        // Set the right color for the tower, uses the color set in the
        // "TOWER_COLORS" constant.
        rect->setBrush(TOWER_COLORS.at(tower.first));
        // Add the graphical tower to the corresponding datastructure
        graphicalTowers_.insert({tower.first,rect});
    }
}

void MainWindow::initializeButtons()
{
    // All the buttons user can use to move the discs around in alphabetical
    // order are added to a vector
    buttons_ = {ui_->AtoBpushButton, ui_->AtoCpushButton, ui_->BtoApushButton,
                ui_->BtoCpushButton, ui_->CtoApushButton, ui_->CtoBpushButton};

    // Initialise the buttons states that are used for the animation
    buttonStates_ = {{"AB", false}, {"AC", false},{"BA", false},{"BC", false},
                     {"CA", false},{"CB", false}};
}

void MainWindow::initializeAttributes()
{
    // Clear the game board.
    scene_->clear();
    ui_->startingTowerLineEdit->clear();
    ui_->numberOfDiscsLineEdit->clear();
    // Start the clock
    sec_ = 0;
    min_ = 0;
    timerSlot();
    timer_->start(1000);
    // Initialize the data structures.
    graphicalTowers_ = {};
    towers_ = {{"A",{}},{"B",{}},{"C",{}}};
    // "Forget" the previous key pressed
    previousKeyPressed_ = 0;

    // Stop the animation
    animationTimer_->stop();
    animationIsOn_ = false;

    // Initialize the starting tower labels
    initializeStartingTowerLabels();
    startingTowerLabels_.at(startingTower_)->setText("Starting tower");

}

void MainWindow::changeTurn()
{
    // Set buttons disabled or enabled depending on the last move
    setButtonsDisabledOrEnabled();

    // Draw the towers
    drawTowerGraphics();

    // Check if the game is at the starting position.
    if (isGameInStartingPosition()) {
        // Enable "solve" button if game is in the starting position.
        ui_->solvePushButton->setEnabled(true);
    } else {
        ui_->solvePushButton->setDisabled(true);
    }
    // Check if the game was won
    if (isGameWon()) {
        endGame();
    }
}

void MainWindow::setAllButtonsDisabled()
{
    // Sets all the buttons disabled so user can't press them during the
    // animation.
    for (QPushButton* button:buttons_) {
        button->setDisabled(true);
    }
}

bool MainWindow::isGameInStartingPosition()
{
    if (static_cast<int>(towers_.at(startingTower_).size()) == numberOfDiscs_) {
        return true;
    }
    return false;
}

void MainWindow::initializeStartingTowerLabels()
{
    // Initializing the three labels to show the user the starting tower so
    // they can't forget it.
    startingTowerLabels_ = {{"A",ui_->startingTowerAlabel},
                            {"B",ui_->startingTowerBlabel},
                            {"C",ui_->startingTowerClabel}};
    for (std::pair<QString, QLabel*> label: startingTowerLabels_) {
        label.second->setText("");
    }
}
