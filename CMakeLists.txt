cmake_minimum_required(VERSION 3.7)

set(VERSION 4.0)

project(deepin-screenshot)

#set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_CXX_FLAGS "-g -Wall -g -fPIE -pie")
set(CMAKE_EXE_LINKER_FLAGS "-fPIE -pie")
set(BIN_NAME deepin-screenshot)

# Sources files
set(SRCS
# main
        "src/eventcontainer.h"
        "src/mainwindow.h"
        "src/screenshot.h"
        "src/eventcontainer.cpp"
        "src/main.cpp"
        "src/mainwindow.cpp"
        "src/screenshot.cpp"

# utils
        "src/utils/baseutils.h"
        "src/utils/calculaterect.h"
        "src/utils/configsettings.h"
        "src/utils/screenutils.h"
        "src/utils/shapesutils.h"
        "src/utils/shortcut.h"
        "src/utils/tempfile.h"
        "src/utils/baseutils.cpp"
        "src/utils/calculaterect.cpp"
        "src/utils/screenutils.cpp"
        "src/utils/shapesutils.cpp"
        "src/utils/shortcut.cpp"
        "src/utils/configsettings.cpp"
        "src/utils/tempfile.cpp"

# widgets
        "src/widgets/bigcolorbutton.h"
        "src/widgets/colorbutton.h"
        "src/widgets/fontsizewidget.h"
        "src/widgets/majtoolbar.h"
        "src/widgets/savebutton.h"
        "src/widgets/savetips.h"
        "src/widgets/shapeswidget.h"
        "src/widgets/subtoolbar.h"
        "src/widgets/textbutton.h"
        "src/widgets/textedit.h"
        "src/widgets/toolbar.h"
        "src/widgets/toolbutton.h"
        "src/widgets/toptips.h"
        "src/widgets/zoomIndicator.h"
        "src/widgets/bigcolorbutton.cpp"
        "src/widgets/colorbutton.cpp"
        "src/widgets/fontsizewidget.cpp"
        "src/widgets/majtoolbar.cpp"
        "src/widgets/savebutton.cpp"
        "src/widgets/savetips.cpp"
        "src/widgets/subtoolbar.cpp"
        "src/widgets/textbutton.cpp"
        "src/widgets/textedit.cpp"
        "src/widgets/toolbar.cpp"
        "src/widgets/toptips.cpp"
        "src/widgets/shapeswidget.cpp"
        "src/widgets/zoomIndicator.cpp"

# controller
        "src/controller/menucontroller.h"
        "src/controller/menucontroller.cpp"

# dbus interface
        "src/dbusinterface/dbuscontrolcenter.h"
        "src/dbusinterface/dbusnotify.h"
        "src/dbusinterface/dbussoundeffect.h"
        "src/dbusinterface/dbuszone.h"
        "src/dbusservice/dbusscreenshot.h"
        "src/dbusservice/dbusscreenshotservice.h"
        "src/dbusinterface/dbuscontrolcenter.cpp"
        "src/dbusinterface/dbusnotify.cpp"
        "src/dbusinterface/dbussoundeffect.cpp"
        "src/dbusinterface/dbuszone.cpp"
        "src/dbusservice/dbusscreenshot.cpp"
        "src/dbusservice/dbusscreenshotservice.cpp"
)

# Find the library
find_package(PkgConfig REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Concurrent REQUIRED)
find_package(Qt5X11Extras REQUIRED)
find_package(Qt5DBus REQUIRED)
find_package(DtkWidget REQUIRED)
find_package(DtkWm REQUIRED)

add_executable(${BIN_NAME} ${SRCS} ${INTERFACES} src/res.qrc src/widgets/resources.qrc)
target_include_directories(${BIN_NAME} PUBLIC ${DtkWidget_INCLUDE_DIRS}
                                              ${DtkWm_INCLUDE_DIRS}
                                              ${XCB_EWMH_INCLUDE_DIRS}
                                              ${DFrameworkDBus_INCLUDE_DIRS}
                                              ${Qt5Gui_PRIVATE_INCLUDE_DIRS}
                                              ${PROJECT_BINARY_DIR})

target_link_libraries(${BIN_NAME} PRIVATE
    ${XCB_EWMH_LIBRARIES}
    ${DFrameworkDBus_LIBRARIES}
    ${DtkWidget_LIBRARIES}
    ${DtkWm_LIBRARIES}
    ${Qt5Widgets_LIBRARIES}
    ${Qt5Concurrent_LIBRARIES}
    ${Qt5X11Extras_LIBRARIES}
    ${Qt5DBus_LIBRARIES}
)

# Install settings
if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX /usr)
endif ()

if (NOT (${CMAKE_BUILD_TYPE} MATCHES "Debug"))
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast")

    # generate qm
    execute_process(COMMAND bash "generate_translations.sh"
                    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})
endif ()

## qm files
file(GLOB QM_FILES "translations/*.qm")
install(FILES ${QM_FILES} DESTINATION share/deepin-screenshot/translations)

## desktop file
file(GLOB DESKTOP_FILES "deepin-screenshot.desktop")
install(FILES ${DESKTOP_FILES} DESTINATION share/applications)

## dbus service
file(GLOB DBUS_SERVICE "src/dbusservice/com.deepin.Screenshot.service")
install(FILES ${DBUS_SERVICE} DESTINATION "share/dbus-1/services/")

# icon
file(GLOB ICON_FILE "deepin-screenshot.svg")
install(FILES ${ICON_FILE} DESTINATION "share/icons/hicolor/scalable/apps")

# bin
install(TARGETS ${BIN_NAME} DESTINATION bin)
