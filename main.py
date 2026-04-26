import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget

from ui.intro_page import IntroPage
from ui.auth_choice import AuthChoicePage
from ui.login_page import LoginPage
from ui.signup_page import SignUpPage
from ui.main_app import ImagineInkApp
from ui.history_page import HistoryPage
from ui.profile_page import UserProfilePage
from ui.forgot_password import ForgotPasswordPage

import database


app = QApplication(sys.argv)

database.create_tables()

stack = QStackedWidget()
stack.addWidget(IntroPage(stack))
stack.addWidget(AuthChoicePage(stack))
stack.addWidget(LoginPage(stack))
stack.addWidget(SignUpPage(stack))
stack.addWidget(ForgotPasswordPage(stack))  
main_app = ImagineInkApp(stack)
stack.addWidget(main_app)
stack.addWidget(HistoryPage(stack))
stack.addWidget(UserProfilePage(stack))

import os

# 🔥 AUTO LOGIN CHECK
if os.path.exists("session.txt"):
    with open("session.txt", "r") as f:
        saved_user_id = f.read().strip()
        if saved_user_id:
            main_app.current_user_id = int(saved_user_id)

            stack.setCurrentIndex(5)

            # 🔥 FORCE UI REFRESH (IMPORTANT)
            main_app.adjustSize()
            main_app.update()
        else:
            stack.setCurrentIndex(0)
else:
    stack.setCurrentIndex(0)

stack.show()
sys.exit(app.exec())