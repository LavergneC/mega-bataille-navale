import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

ListModel {
    id: modelBateaux

    ListElement {
        name : "Porte-container"
        nb : 1
        longueur : 5
        largeur : 2
    }
    ListElement {
        name : "Porte-avions"
        nb : 2
        longueur : 5
        largeur : 1
    }
    ListElement {
        name : "Destroyer"
        nb : 3
        longueur : 4
        largeur : 1
    }
    ListElement {
        name : "Torpilleur"
        nb : 3
        longueur : 3
        largeur : 2
    }
    ListElement {
        name : "Sous-marin nucléaire"
        nb : 2
        longueur : 6
        largeur : 1
    }
    ListElement {
        name : "Sous-marin de combat"
        nb : 5
        longueur : 3
        largeur : 1
    }
    ListElement {
        name : "Sous-marin de reconnaissance"
        nb : 2
        longueur : 2
        largeur : 1
    }
}
