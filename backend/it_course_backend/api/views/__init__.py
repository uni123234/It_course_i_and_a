from .home import HomePageView

from .learns import (
    FAQListView,
    FAQListCreateView,
    FAQDetailView,
    CourseListView,
    CourseCreateView,
    CourseEditView,
    CourseDeleteView,
    CourseDetailView,
    GroupCreateView,
    GroupDetailView,
    GroupListView,
    GroupEditView,
    LessonListView,
    LessonDetailView,
    HomeworkListView,
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
