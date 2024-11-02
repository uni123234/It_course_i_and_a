from .home import HomePageView

from .learns import (
    CourseListCreateView,
    CourseDetailView,
    CourseEditView,
    GroupCreateView,
    GroupEditView,
    LessonCreateView,
    StudentHomeworkListView,
    HomeworkDetailView,
    HomeworkSubmissionView,
    HomeworkGradeView,
    HomeworkListCreateView,
    HomeworkEditView,
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
