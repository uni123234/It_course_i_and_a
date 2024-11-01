from .home import HomePageView

from .learns import (
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
    LessonListView,
    LessonEditView,
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
    GoogleLoginView,
)
