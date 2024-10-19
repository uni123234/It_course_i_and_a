from .home import HomePageView

from .learns import (
    FAQListView,
    FAQListCreateView,
    FAQDetailView,
    CourseListCreateView,
    CourseDetailView,
    CourseEditView,
    CourseDeleteView,
    GroupCreateView,
    GroupDetailView,
    GroupListView,
    GroupEditView,
    LessonListView,
    LessonCreateView,
    LessonDetailView,
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
    ChangeUsernameView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)
