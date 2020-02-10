/* Module mainwindow: Mainwindow has all the functionalities of the program
 * right now. Creates a 2D Tower of Hanoi game that the user can play.
 * Instructions are located at instructions.txt file.
 *
 *
 * Name: Pauli Latva-Kokko
 * Student number: 276321
 * Email: pauli.latva-kokko@tuni.fi
 * Student repository:
 * https://course-gitlab.tuni.fi/tie-02201-ohj2_2019-SYKSY/latvakop
 * */

#ifndef MAINWINDOW_HH
#define MAINWINDOW_HH

#include <QMainWindow>
#include <QGraphicsScene>
#include <QGraphicsRectItem>
#include <QPushButton>
#include <QMessageBox>
#include <QTimer>
#include <QKeyEvent>
#include <map>
#include <vector>
#include <QDebug>
#include <QString>
#include <algorithm>

// Maximum and minimum number of discs. If there is more than 15 discs they
// don't really fit on the gameboard anymore and solving it would take more than
// 2^15 - 1 = 32 767 moves. No point in having that many discs in my opinion
const int MAX_NUMBER_OF_DISCS = 15;
const int MIN_NUMBER_OF_DICS = 1;

// Error text that is printed if the user gives a non integer value.
const QString DISCS_ERROR_TEXT = "Bad input! Number of discs must be an "
                                 "integer between 1-15!";

// Error text that is printed if the user gives a tower that doesn't exist in
// the game.
const QString TOWER_ERROR_TEXT = "Error! Starting tower can be either "
                                 "'A','B' or 'C'";

// Number of discs that is used if user gives no input.
const int STANDARD_NUMBER_OF_DISCS = 6;

// Starting tower that is used if user gives no input.
const QString STANDARD_STARTING_TOWER = "A";

// Data structure that stores all the information regarding all the towers.
// QString is either 'A','B' or 'C'(all the towers) and the vector has pairs
// where an integer represents the size of the disc and a pointer to the
// rectangle is used to move the rectangle in the gameboard.
using dataStructure = std::map<QString, std::vector<std::pair
<int, QGraphicsRectItem*>>>;
// Data structure of a single tower.
using towerData = std::vector<std::pair<int, QGraphicsRectItem*>>;
// Data structure of a single pair that has the rectangle and the size of it.
using rectangle = std::pair<int, QGraphicsRectItem*>;

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:

    // Starts a new game with the parameters the user inputted.
    void on_newGamePushButton_clicked();

    // Slots for all the buttons that move the discs.
    void on_AtoBpushButton_clicked();

    void on_AtoCpushButton_clicked();

    void on_BtoApushButton_clicked();

    void on_BtoCpushButton_clicked();

    void on_CtoApushButton_clicked();

    void on_CtoBpushButton_clicked();

    // A slot for updating the time.
    void timerSlot();

    // Slot that is connected to the animation timer, uses a simple iterative
    // algorithm to move the discs around.
    void animationSlot();

    // A slot that is called when the user presses a key
    void keyPressEvent(QKeyEvent* event);

    // Slot for starting the solving process.
    void on_solvePushButton_clicked();

    // Slot for ending the solving process.
    void on_stopSolvingPushButton_clicked();

private:

    // *** Course code
    // Graphics scene coordinates in pixels.
    const int BORDER_UP = 0;
    const int BORDER_DOWN = 260;
    const int BORDER_LEFT = 0;
    const int BORDER_RIGHT = 680;
    // Course code ends ***

    // The height of every disc in pixels.
    const int RECTANGLE_HEIGHT = 10;
    // The width of the smallest disc in pixels.
    const int RECTANGLE_STARTING_WIDTH = 18;
    // Step is the amount of pixels that the disc size widens for every
    // time there's a new bigger disc.
    const int STEP = 10;
    // X coordinate of the left-most tower.
    const int TOWER_LEFT = BORDER_RIGHT / 4;
    // X coordinate of the middle tower.
    const int TOWER_MIDDLE = BORDER_RIGHT / 2;
    // X coordinate of the right-most tower.
    const int TOWER_RIGHT = BORDER_RIGHT - (BORDER_RIGHT / 4);

    // All the tower coordinates in a map for quick search.
    const std::map<QString, const int> TOWER_COORDS =
    {{"A", TOWER_LEFT}, {"B", TOWER_MIDDLE}, {"C", TOWER_RIGHT}};

    // All the possible move combinations the user can input.
    const std::vector<std::pair<QString,QString>> USER_COMMANDS =
    {{"A","B"},{"A","C"}, {"B","A"},{"B","C"}, {"C","A"},{"C","B"}};

    // The moves of the simple iterative algorithm that is used for the
    // animation.
    const std::vector<std::pair<QString, QString>> ANIMATION_ALGORITHM =
    {{"AB","BA"},{"AC","CA"}, {"BC","CB"}};

    // The tower colors in a map.
    const std::map<QString, QBrush> TOWER_COLORS =
    {{"A", QBrush(Qt::green)}, {"B", QBrush(Qt::magenta)},
     {"C", QBrush(Qt::blue)}};

    // All the key combinations the user can use to move the discs in
    // alphabetical order.
    const std::vector<std::pair<int, int>> KEY_COMBINATIONS =
    {{Qt::Key_A, Qt::Key_B},{Qt::Key_A, Qt::Key_C},{Qt::Key_B, Qt::Key_A},
     {Qt::Key_B, Qt::Key_C},{Qt::Key_C, Qt::Key_A},{Qt::Key_C, Qt::Key_B}};

    // Graphical tower constants for it's size
    const int GRAPHICAL_TOWER_WIDTH = 6;
    const int GRAPHICAL_TOWER_HEIGHT = 200;

    // The time for how fast the animation is
    // 100 means the animation moves discs 10 times per second.
    const int ANIMATION_TIME = 100;

    // The starting point of the animation algorithm. This is so that the
    // algorithm also works if the game starts from the 'B' or 'C' tower.
    const std::map<QString, int> ANIMATION_ALGORITHM_STARTING_POINT =
    {{"A",0}, {"B",2},{"C",1}};

    // The ui
    Ui::MainWindow *ui_;
    // A graphics scene where the hanoi's towers are drawn to.
    QGraphicsScene* scene_;
    // Data structure that stores all the information regarding all the towers.
    dataStructure towers_;
    // Number of the discs in the game in int.
    int numberOfDiscs_;

    // Animation counter represents the phase of the iterative algorithm that is
    // happening next. 0 = A->B or B->A, 1 = A->C or C->A, 2 = B->C or C->B.
    // This is for drawing the animation.
    int animationCounter_;

    // Name of the starting tower in QString
    QString startingTower_;

    // Map for drawing the graphical towers
    std::map<QString, QGraphicsRectItem*> graphicalTowers_;

    // Qtimer for showing the gametime for user.
    QTimer* timer_;
    int sec_;
    int min_;

    // The animation timer, I decided to do a separate timer so I can adjust
    // speed of the animation without changing how the game's clock works.
    QTimer* animationTimer_;

    // Value of the previous key that the user pressed.
    int previousKeyPressed_;

    // The 'A->B' etc buttons that the user can use to move the discs around.
    std::vector<QPushButton*> buttons_;

    // Boolean for checking if animation is happening right now.
    bool animationIsOn_;

    // Buttons states in a map so we don't have to disable or enable them,
    // since that would cause bugs if it happens in the middle of the animation.
    std::map<QString, bool> buttonStates_;

    // Starting tower labels show the user where the game started from
    std::map<QString, QLabel*> startingTowerLabels_;

    // Function for testing if user input an acceptable input for the number
    // of discs. Returns true if input is ok, false if it's bad.
    bool isNumberOfDiscsAcceptable(int& numberOfDiscs);

    // Function that returns true if user inputted one of the three towers: 'A',
    // 'B' or 'C'. Returns false otherwise.
    bool isStartingTowerAcceptable(QString& startingTower);

    // Function that starts a new game with the parameters that the user
    // inputted.
    void startNewGame(int numberOfDiscs, QString startingTower);

    // Function that that takes a QString parameter and turns it to an integer
    // and returns that integer.
    int QStringtoInt(QString string);

    // Sets buttons state to disabled if the discs that would be moved by the
    // button are impossible to move next turn. Also sets other buttons to
    // enabled if it's possible to move the corresponding discs next turn.
    // If animation is goin on this function doesn't enable or disable the
    // buttons, instead it changes the information to a buttons states map.
    void setButtonsDisabledOrEnabled();

    // Moves the the top disc of one tower to the top of another tower.
    // Takes the name of the two towers as parameters. For example if user
    // want's to move a disc from 'A' tower to 'C', parameter will be a pair of
    // {"A","C"}.
    void moveDisc(std::pair<QString, QString> twoTowers);

    // Function that checks if the player has won the game. Returns true if
    // player won, false otherwise.
    bool isGameWon();

    // Function that draws the rectangles that are supposed to be the tall and
    // narrow wood sticks that support the discs in the realworld tower of hanoi
    // game. This function gets called after every turn because the height of
    // the towers changes every turn.
    void drawTowerGraphics();

    // Function that is called if the game is won. Stops the timer and asks
    // if the user wants to play again.
    void endGame();

    // Function that initialises the graphical towers in to the right positions
    // with the right colors.
    void initializeGraphicalTowers();

    // Function that initializes the 'A->B' etc buttons in to a vector in
    // alphabetical order and also the button states map.
    void initializeButtons();

    // Function that initializes all the needed private attributes at the start
    // of a new game.
    void initializeAttributes();

    // Function that is called after every turn to check if the game was won
    // and disable illegal moves for the next turn and draw tower graphics.
    // This funtion doesn't really do anything itself it just calls other
    // functions to do things.
    void changeTurn();

    // Disables all the buttons for when the animation is happening so the user
    // can't mess it up.
    void setAllButtonsDisabled();

    // Returns true if game is in the starting position. If the game is in
    // starting position the "solve" button is enabled and the user can use the
    // animation feature.
    bool isGameInStartingPosition();

    // Initializes the three tower labels that are used to show the user the
    // tower they started the game from.
    void initializeStartingTowerLabels();
};
#endif // MAINWINDOW_HH
