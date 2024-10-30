from .home import HomePageView

from .learns import (
    FAQListCreateView,
    FAQDetailView,
    CourseListCreateView,
    CourseDetailView,
    CourseEditView,
    GroupCreateView,
    GroupEditView,
    LessonCreateView,
    HomeworkDetailView,
    HomeworkSubmissionView,
    HomeworkListCreateView,
    LessonCalendarView,
    ReminderView,
)

from .user import (
    RegisterView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    ChangeEmailView,
    ConfirmEmailView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)
