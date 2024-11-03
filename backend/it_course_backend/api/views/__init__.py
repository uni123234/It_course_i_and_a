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
    HomeworkEditView,
    LessonCalendarView,
    ReminderView,
    LessonListView,
    LessonEditView,
    JoinCourseView,
    CourseStudentsView,
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
